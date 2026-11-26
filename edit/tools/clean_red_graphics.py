#!/usr/bin/env python3
"""Remove red hood/roof graphics (old M, pinstripes) from a still inside a box, inpaint, and regrain to match the
surrounding surface. Also clears the CapCut 'Ai' corner badge.
Usage: .venv/bin/python edit/tools/clean_red_graphics.py IN OUT --box x0 y0 x1 y1 [--thr 22] [--badge x y w h]
Never overwrites."""
import argparse, sys
from pathlib import Path
import cv2
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--box", type=int, nargs=4, required=True)
ap.add_argument("--thr", type=int, default=22)
ap.add_argument("--badge", type=int, nargs=4, default=[30, 30, 120, 110])
a = ap.parse_args()
if Path(a.out).exists():
    sys.exit(f"refusing to overwrite {a.out}")
f = cv2.imread(a.inp)
b, g, r = [c.astype(np.int16) for c in cv2.split(f)]
m = ((r - np.maximum(g, b)) > a.thr) & (r > 55)
box = np.zeros_like(m); x0, y0, x1, y1 = a.box; box[y0:y1, x0:x1] = True; m &= box
md = cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=3)
c = cv2.inpaint(f, md * 255, 7, cv2.INPAINT_TELEA).astype(np.float32)
lum = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32)
hp = lum - cv2.GaussianBlur(lum, (0, 0), 2.0)
ring = cv2.dilate(md, np.ones((15, 15), np.uint8)) & (1 - md)          # surface right around the removed graphics
sd = float(hp[ring > 0].std()) if ring.any() else 6.0
noise = np.random.default_rng(7).normal(0, sd, lum.shape).astype(np.float32)
noise -= cv2.GaussianBlur(noise, (0, 0), 2.0) * 0.5
mm = cv2.GaussianBlur(md.astype(np.float32), (0, 0), 2)[..., None]
c = np.clip(c + noise[..., None] * mm, 0, 255).astype(np.uint8)
bx, by, bw, bh = a.badge; bm = np.zeros(lum.shape, np.uint8); bm[by:by + bh, bx:bx + bw] = 255
c = cv2.inpaint(c, bm, 7, cv2.INPAINT_TELEA)
cv2.imwrite(a.out, c); print("cleaned", int(m.sum()), "red px; grain sd", round(sd, 1))
