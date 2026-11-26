#!/usr/bin/env python3
"""Blur a moving region (e.g. a licence plate) by tracking it from one seed box, forward and backward.

Usage: .venv/bin/python edit/tools/blur_track.py IN OUT --seed-time 4.3 --box x y w h [--start 3.9] [--end 99]
       [--pad 0.35] [--debug DIR]
Multi-scale template matching in a local search window; the template refreshes every frame so it follows
size changes. Writes OUT (H.264 CRF 12, source audio copied). Never overwrites.
"""
import argparse, subprocess, sys
from pathlib import Path
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--seed-time", type=float, required=True)
ap.add_argument("--box", type=int, nargs=4, required=True)
ap.add_argument("--start", type=float, default=0.0); ap.add_argument("--end", type=float, default=1e9)
ap.add_argument("--pad", type=float, default=0.35); ap.add_argument("--search", type=int, default=60)
ap.add_argument("--debug")
a = ap.parse_args()
out = Path(a.out)
if out.exists():
    sys.exit(f"refusing to overwrite {out}")

cap = cv2.VideoCapture(a.inp)
fps = cap.get(cv2.CAP_PROP_FPS)
frames = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    frames.append(f)
n = len(frames); h, w = frames[0].shape[:2]
seed = min(n - 1, int(round(a.seed_time * fps)))
f0, f1 = max(0, int(a.start * fps)), min(n - 1, int(a.end * fps))
gray = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames]

def track(order):
    x, y, bw, bh = a.box; boxes = {}
    tpl = gray[seed][y:y + bh, x:x + bw]
    for i in order:
        best = None
        for s in (0.92, 0.96, 1.0, 1.04, 1.08):
            tw, th = max(8, int(round(tpl.shape[1] * s))), max(6, int(round(tpl.shape[0] * s)))
            t = cv2.resize(tpl, (tw, th))
            sx0, sy0 = max(0, x - a.search), max(0, y - a.search)
            sx1, sy1 = min(w, x + bw + a.search), min(h, y + bh + a.search)
            win = gray[i][sy0:sy1, sx0:sx1]
            if win.shape[0] < th or win.shape[1] < tw:
                continue
            r = cv2.matchTemplate(win, t, cv2.TM_CCOEFF_NORMED)
            _, mv, _, ml = cv2.minMaxLoc(r)
            if best is None or mv > best[0]:
                best = (mv, sx0 + ml[0], sy0 + ml[1], tw, th)
        if best is None:
            break
        _, x, y, bw, bh = best
        boxes[i] = (x, y, bw, bh, round(best[0], 3))
        tpl = gray[i][y:y + bh, x:x + bw]
    return boxes

boxes = {**track(range(seed, f1 + 1)), **track(range(seed, f0 - 1, -1))}
proc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-n", "-f", "rawvideo", "-pix_fmt", "bgr24",
                         "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-i", a.inp, "-map", "0:v", "-map", "1:a?",
                         "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "copy",
                         "-shortest", str(out)], stdin=subprocess.PIPE)
dbg = Path(a.debug) if a.debug else None
if dbg:
    dbg.mkdir(parents=True, exist_ok=True)
for i, f in enumerate(frames):
    if i in boxes:
        x, y, bw, bh, _ = boxes[i]
        px, py = int(bw * a.pad), int(bh * a.pad)
        x0, y0, x1, y1 = max(0, x - px), max(0, y - py), min(w, x + bw + px), min(h, y + bh + py)
        roi = f[y0:y1, x0:x1]
        small = cv2.resize(roi, (max(1, roi.shape[1] // 8), max(1, roi.shape[0] // 8)), interpolation=cv2.INTER_AREA)
        blur = cv2.GaussianBlur(cv2.resize(small, (roi.shape[1], roi.shape[0]), interpolation=cv2.INTER_LINEAR), (0, 0), 3)
        m = np.zeros(roi.shape[:2], np.float32)
        cv2.ellipse(m, (roi.shape[1] // 2, roi.shape[0] // 2), (roi.shape[1] // 2, roi.shape[0] // 2), 0, 0, 360, 1, -1)
        m = cv2.GaussianBlur(m, (0, 0), 3)[..., None]
        f[y0:y1, x0:x1] = (roi * (1 - m) + blur * m).astype(np.uint8)
        if dbg and i % 4 == 0:
            d = f.copy(); cv2.rectangle(d, (x, y), (x + bw, y + bh), (0, 255, 255), 1)
            cv2.imwrite(str(dbg / f"f{i:03d}.png"), d[max(0, y - 120):y + bh + 120, max(0, x - 160):x + bw + 160])
    proc.stdin.write(f.tobytes())
proc.stdin.close(); proc.wait()
print("tracked frames", min(boxes), "-", max(boxes), "of", n, "min score", min(b[4] for b in boxes.values()))
