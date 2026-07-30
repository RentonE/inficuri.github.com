#!/usr/bin/env python3
"""Download and verify the two ONNX models this skill needs.

Both come from public model zoos and are pinned by sha256. Everything runs
locally; these downloads are the only network access the skill ever performs.
"""
import hashlib
import os
import subprocess
import sys
import urllib.request

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(SKILL_DIR, "models")

MODELS = {
    "yunet.onnx": {
        "url": ("https://media.githubusercontent.com/media/opencv/opencv_zoo/"
                "main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"),
        "sha256": "8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4",
    },
    "ferplus.onnx": {
        "url": ("https://media.githubusercontent.com/media/onnx/models/main/"
                "validated/vision/body_analysis/emotion_ferplus/model/emotion-ferplus-8.onnx"),
        "sha256": "a2a2ba6a335a3b29c21acb6272f962bd3d47f84952aaffa03b60986e04efa61c",
    },
}

REQUIRED_PKGS = ["onnxruntime", "cv2", "PIL", "numpy"]
PIP_NAMES = {"cv2": "opencv-python-headless", "PIL": "pillow"}


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_models() -> None:
    os.makedirs(MODELS_DIR, exist_ok=True)
    for name, spec in MODELS.items():
        dest = os.path.join(MODELS_DIR, name)
        if os.path.isfile(dest) and sha256_of(dest) == spec["sha256"]:
            print(f"[ok] {name} present, checksum verified")
            continue
        print(f"[dl] fetching {name} ...")
        urllib.request.urlretrieve(spec["url"], dest)
        got = sha256_of(dest)
        if got != spec["sha256"]:
            os.remove(dest)
            sys.exit(f"[FATAL] checksum mismatch for {name}: {got}")
        print(f"[ok] {name} downloaded, checksum verified")


def ensure_packages() -> None:
    missing = []
    for mod in REQUIRED_PKGS:
        try:
            __import__(mod)
        except ImportError:
            missing.append(PIP_NAMES.get(mod, mod))
    if missing:
        print(f"[pip] installing: {' '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", *missing])
    if subprocess.run(["which", "ffmpeg"], capture_output=True).returncode != 0:
        sys.exit("[FATAL] ffmpeg not found on PATH — install it first (apt-get install ffmpeg)")


if __name__ == "__main__":
    ensure_packages()
    ensure_models()
    print("setup complete:", MODELS_DIR)
