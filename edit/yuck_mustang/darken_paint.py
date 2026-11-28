#!/usr/bin/env python3
"""Darken grey/silver car paint toward matte black in the exterior Yuck shots (S2/S3).

Mask = low-saturation, mid/high-luma pixels in large connected regions, minus a dilated skin
mask (arm, hands, watch on the wrist stay untouched). Masked pixels: luma scaled by GAIN,
saturation reduced, edges feathered. usage: darken_paint.py IN OUT [GAIN=0.35] [--preview PNG]
"""
import sys
import cv2
import numpy as np

src, dst = sys.argv[1], sys.argv[2]
gain = float(sys.argv[3]) if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else 0.35
preview = sys.argv[sys.argv.index("--preview") + 1] if "--preview" in sys.argv else None

def mask_for(f):
    h, w = f.shape[:2]
    lab = cv2.cvtColor(f, cv2.COLOR_BGR2LAB).astype(np.int16)
    L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]
    paint = ((A < 137) & (B < 142) & (L > 30)).astype(np.uint8)
    skin = ((A > 138) & (B > 142)).astype(np.uint8)
    skin = cv2.dilate(skin, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (35, 35)))
    paint[skin > 0] = 0
    paint = cv2.morphologyEx(paint, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab_, st, _ = cv2.connectedComponentsWithStats(paint, 8)
    keep = np.zeros_like(paint)
    for i in range(1, n):
        # car body panels (door below the sill, roof above the window) span the full frame width;
        # clothing / background pieces do not
        if st[i, cv2.CC_STAT_WIDTH] > w * 0.85:
            keep[lab_ == i] = 1
    keep = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    return cv2.GaussianBlur(keep.astype(np.float32), (31, 31), 0)

cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = None if preview else cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
prev = None
n = 0
while True:
    ok, f = cap.read()
    if not ok:
        break
    m = mask_for(f)
    m = m if prev is None else 0.6 * m + 0.4 * prev   # temporal smoothing against flicker
    prev = m
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV).astype(np.float32)
    k = 1 - m * (1 - gain)
    hsv[..., 2] *= k
    hsv[..., 1] *= (1 - 0.6 * m)
    g = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR)
    if preview:
        vis = np.hstack([f, g, cv2.cvtColor((m * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)])
        cv2.imwrite(preview, cv2.resize(vis, None, fx=0.4, fy=0.4))
        break
    out.write(g)
    n += 1
if out:
    out.release()
print("frames", n)
