---
name: micro-expression-analysis
description: >
  Local-only face & expression analysis for video files: per-face emotion
  timelines (YuNet detector + FER+ classifier), time-sorted face-chip strips,
  frame contact sheets, motion curves, and a structured social-dynamics reading
  protocol. Use this skill whenever the user asks to analyze expressions,
  micro-expressions, emotions, faces, moods, body language, interpersonal
  dynamics, "who is who", relationships, or hidden tensions (微表情 / 表情分析 /
  人脸分析 / 人物关系 / 勾心斗角 / 气氛) in a local video file — even if they
  just say "analyze this video" and the video contains people interacting.
  All processing is local; nothing is ever uploaded.
---

# Micro-Expression & Face-Emotion Timeline Analysis

Turn a local video of people into evidence you can reason about: who appears,
when, with what (apparent) expression, and how attention and posture flow
between them. The pipeline is deterministic and local; the *interpretation* is
your job, governed by `references/reading-protocol.md`.

## Hard rules (why they exist)

- **Everything stays local.** Faces and voices are biometric data of real
  people. Never send the video, frames, chips, or audio to any external API or
  cloud service. The bundled models run on CPU via onnxruntime.
- **No identity claims.** The pipeline finds *faces*, not *persons*. You may
  group faces into anonymous roles (A/B/C…) using visual continuity, but never
  assert who someone really is, and never run face-recognition/identification.
- **Interpretation ≠ fact.** FER on small compressed faces mostly outputs
  "neutral"; treat model labels as weak corroboration only. Any psychological
  or relational claim must carry a confidence label and the observable evidence
  it rests on (gaze direction, posture, timing) — see the reading protocol.

## Workflow

### Step 0 — Setup (first use only)

```bash
python3 scripts/setup_models.py        # downloads YuNet (232KB) + FER+ (35MB) with sha256 verification
```

Requires `ffmpeg` on PATH and Python packages `onnxruntime opencv-python-headless pillow numpy`
(the script offers to pip-install missing ones). Models are cached in `models/`
inside the skill directory and never re-downloaded once verified.

### Step 1 — Run the pipeline

```bash
python3 scripts/analyze_faces.py /path/to/video.mp4 --outdir /path/to/workdir
```

Useful flags:

- `--interval 1.5` — uniform sampling step in seconds (default 1.5)
- `--burst 8.0:3.0 --burst 22.8:3.0` — extra dense (3 fps) windows around
  moments you care about (laughter, a whisper, a handshake). Add bursts on a
  second pass once Step 2 tells you where the interesting moments are.
- `--min-face 28` — ignore detections smaller than this many pixels.

Outputs in `--outdir`:

| File | What it is |
|---|---|
| `metadata.json` | container/stream info incl. creation timestamps (forensic chain) |
| `frames/f_*.jpg` | sampled full frames |
| `contact_sheet.jpg` | all frames tiled with timestamps — read this first |
| `chips/t*_x*_<emotion><conf>.jpg` | every detected face, 144px, named by time/position/FER label |
| `faces.csv` | one row per detection: `t,x,y,w,h,emotion,confidence` |
| `chip_strip.jpg` | all chips tiled in time order with labels |
| `motion.csv` | per-frame inter-frame motion (find peaks ≈ big gestures; quiet spans ≈ stillness) |

### Step 2 — Look, then aim

Read `contact_sheet.jpg` and `chip_strip.jpg` with your own eyes. Identify the
recurring faces and assign anonymous roles (A, B, C…) by clothing/hair/position
continuity — do NOT trust x-coordinate clustering, it breaks the moment the
camera moves. Use `motion.csv` peaks and audio events to pick 3–6 key moments,
then re-run Step 1 with `--burst` windows around them and crop full-resolution
close-ups of those moments with ffmpeg for detailed reading.

### Step 3 — Interpret under the protocol

Read `references/reading-protocol.md` (short) before writing conclusions. It
defines: how to ground claims in observables, the confidence vocabulary, what
FER labels can and cannot support, and the mandatory disclaimer block for
relational/psychological readings.

### Step 4 — Deliver

Prefer visual deliverables next to prose: the contact sheet, an annotated
evidence board of the key moments (tile the crops with captions), and per-role
chip strips. State what the evidence does NOT support as plainly as what it
does — a finding of "no visible tension" is a finding.
