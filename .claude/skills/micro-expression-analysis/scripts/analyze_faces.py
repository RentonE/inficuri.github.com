#!/usr/bin/env python3
"""Face & expression timeline pipeline — 100% local.

Samples frames from a video, detects faces (YuNet), classifies apparent
emotion (FER+), and writes chips, CSVs, contact sheets and a motion curve
into an output directory for a human/model to interpret.

Nothing here talks to the network; setup_models.py is the only downloader.
"""
import argparse
import csv
import glob
import json
import os
import subprocess
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(SKILL_DIR, "models")

EMOTIONS = ["neutral", "happiness", "surprise", "sadness",
            "anger", "disgust", "fear", "contempt"]
EMOTIONS_ZH = ["中性", "高兴", "惊讶", "悲伤", "愤怒", "厌恶", "恐惧", "轻蔑"]


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def probe(video):
    r = run(["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_format", "-show_streams", video])
    return json.loads(r.stdout or "{}")


def extract_frames(video, outdir, interval, bursts):
    fdir = os.path.join(outdir, "frames")
    os.makedirs(fdir, exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-i", video,
         "-vf", f"fps=1/{interval}", "-q:v", "2",
         os.path.join(fdir, "u_%04d.jpg")])
    for i, (start, dur) in enumerate(bursts):
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(dur),
             "-i", video, "-vf", "fps=3", "-q:v", "2",
             os.path.join(fdir, f"b{i}_{start:07.2f}_%03d.jpg")])
    frames = []
    for p in sorted(glob.glob(os.path.join(fdir, "*.jpg"))):
        b = os.path.basename(p)
        if b.startswith("u_"):
            t = (int(b[2:6]) - 1) * interval + interval / 2
        else:
            start = float(b.split("_")[1])
            t = start + (int(b.split("_")[2][:3]) - 1) / 3.0
        frames.append((round(t, 2), p))
    return sorted(frames)


def detect_and_classify(frames, outdir, min_face):
    import cv2
    import numpy as np
    import onnxruntime as ort
    det = cv2.FaceDetectorYN_create(os.path.join(MODELS_DIR, "yunet.onnx"),
                                    "", (320, 320), 0.6, 0.3, 500)
    fer = ort.InferenceSession(os.path.join(MODELS_DIR, "ferplus.onnx"),
                               providers=["CPUExecutionProvider"])
    cdir = os.path.join(outdir, "chips")
    os.makedirs(cdir, exist_ok=True)
    rows = []
    for t, path in frames:
        img = cv2.imread(path)
        if img is None:
            continue
        det.setInputSize((img.shape[1], img.shape[0]))
        _, faces = det.detect(img)
        if faces is None:
            continue
        for face in faces:
            x, y, w, h = (int(v) for v in face[:4])
            if w < min_face:
                continue
            pad = int(w * 0.2)
            x0, y0 = max(0, x - pad), max(0, y - pad)
            x1 = min(img.shape[1], x + w + pad)
            y1 = min(img.shape[0], y + h + pad)
            chip = img[y0:y1, x0:x1]
            if chip.size == 0:
                continue
            g = cv2.resize(cv2.cvtColor(chip, cv2.COLOR_BGR2GRAY), (64, 64))
            score = fer.run(None, {"Input3": g.astype(np.float32)[None, None]})[0][0]
            p = np.exp(score - score.max())
            p /= p.sum()
            k = int(np.argmax(p))
            conf = int(p[k] * 100)
            cv2.imwrite(os.path.join(cdir, f"t{t:07.2f}_x{x:04d}_{EMOTIONS[k]}{conf}.jpg"),
                        cv2.resize(chip, (144, 144), interpolation=cv2.INTER_LANCZOS4))
            rows.append([t, x, y, w, h, EMOTIONS[k], EMOTIONS_ZH[k], conf])
    with open(os.path.join(outdir, "faces.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["t_sec", "x", "y", "w", "h", "emotion", "emotion_zh", "confidence_pct"])
        wr.writerows(sorted(rows))
    return rows


def motion_curve(video, outdir):
    import cv2
    import numpy as np
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    prev, out = None, []
    idx = 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(cv2.resize(fr, (320, 180)), cv2.COLOR_BGR2GRAY).astype(np.float32)
        if prev is not None:
            out.append((round(idx / fps, 3), round(float(np.abs(g - prev).mean()), 3)))
        prev = g
        idx += 1
    cap.release()
    with open(os.path.join(outdir, "motion.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["t_sec", "motion"])
        wr.writerows(out)
    return out


def montage(images, labels, cols, tile_w, tile_h, path, pad_bottom=26):
    from PIL import Image, ImageDraw
    if not images:
        return
    rows = (len(images) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tile_w, rows * (tile_h + pad_bottom)), "#111111")
    d = ImageDraw.Draw(sheet)
    for i, (im_path, label) in enumerate(zip(images, labels)):
        im = Image.open(im_path).resize((tile_w, tile_h), Image.LANCZOS)
        x, y = (i % cols) * tile_w, (i // cols) * (tile_h + pad_bottom)
        sheet.paste(im, (x, y))
        d.text((x + 4, y + tile_h + 4), label, fill="#ffffff")
    sheet.save(path, quality=88)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--interval", type=float, default=1.5)
    ap.add_argument("--burst", action="append", default=[],
                    help="start:duration seconds of dense 3fps sampling, repeatable")
    ap.add_argument("--min-face", type=int, default=28)
    args = ap.parse_args()

    if not os.path.isfile(args.video):
        sys.exit(f"video not found: {args.video}")
    for name in ("yunet.onnx", "ferplus.onnx"):
        if not os.path.isfile(os.path.join(MODELS_DIR, name)):
            sys.exit("models missing — run scripts/setup_models.py first")

    outdir = args.outdir or (os.path.splitext(os.path.basename(args.video))[0] + "-faces")
    os.makedirs(outdir, exist_ok=True)
    bursts = [tuple(float(v) for v in b.split(":")) for b in args.burst]

    with open(os.path.join(outdir, "metadata.json"), "w") as f:
        json.dump(probe(args.video), f, indent=1, ensure_ascii=False)

    frames = extract_frames(args.video, outdir, args.interval, bursts)
    rows = detect_and_classify(frames, outdir, args.min_face)
    motion = motion_curve(args.video, outdir)

    montage([p for _, p in frames], [f"{t:.1f}s" for t, _ in frames],
            cols=6, tile_w=320, tile_h=180,
            path=os.path.join(outdir, "contact_sheet.jpg"))
    chips = sorted(glob.glob(os.path.join(outdir, "chips", "*.jpg")))
    labels = [os.path.basename(c)[1:].rsplit(".", 1)[0].replace("_", " ") for c in chips]
    montage(chips, labels, cols=10, tile_w=144, tile_h=144,
            path=os.path.join(outdir, "chip_strip.jpg"))

    peak_t = max(motion, key=lambda r: r[1])[0] if motion else None
    print(json.dumps({
        "outdir": outdir,
        "frames": len(frames),
        "face_detections": len(rows),
        "motion_peak_t": peak_t,
        "next": "read contact_sheet.jpg and chip_strip.jpg, then re-run with --burst around key moments",
    }, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
