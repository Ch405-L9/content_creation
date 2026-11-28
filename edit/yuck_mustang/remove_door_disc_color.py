#!/usr/bin/env python3
"""Remove a saturated red/yellow door roundel sitting on the bottom edge of a CapCut S2/S3 edit.

Per frame, in the bottom band: mask saturated red/orange/yellow pixels plus the bright rim around them,
keep only components touching the bottom edge (the roundel, not tail lights or skin), dilate, and fill
with the dark door paint (inpaint seeded from the surrounding door). Audio is re-muxed later by finish.sh.
usage: remove_door_disc_color.py IN.mp4 OUT.mp4 [Y_TOP_FRACTION=0.78]
"""
import sys
import cv2
import numpy as np

src, dst = sys.argv[1], sys.argv[2]
ytop_f = float(sys.argv[3]) if len(sys.argv) > 3 else 0.78
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
y0 = int(h * ytop_f)
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
n = 0
while True:
    ok, f = cap.read()
    if not ok:
        break
    band = f[y0:].copy()
    bh = band.shape[0]
    hsv = cv2.cvtColor(band, cv2.COLOR_BGR2HSV)
    hh, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    warm = (((hh < 35) | (hh > 165)) & (s > 90) & (v > 70))
    pale = (v > 150) & (s < 90)                      # cream/white rim and number
    m = (warm | pale).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
    cnt, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros_like(m)
    for i in range(1, cnt):
        x, y, bw, bhh, area = st[i]
        if y + bhh >= bh - 3 and area > 600:          # touches the bottom edge: the roundel
            keep[lab == i] = 1
    if keep.any():
        keep = cv2.dilate(keep, k, iterations=2)
        # fill: horizontal-then-vertical inpaint from the dark door around it
        band = cv2.inpaint(band, keep * 255, 15, cv2.INPAINT_TELEA)
        # keep the fill matte and dark like the paint above it
        ref = cv2.cvtColor(f[y0 - 40:y0], cv2.COLOR_BGR2HSV)[..., 2]
        cap_v = float(np.percentile(ref, 60))
        hb = cv2.cvtColor(band, cv2.COLOR_BGR2HSV).astype(np.float32)
        mk = cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 6)
        hb[..., 2] = hb[..., 2] * (1 - mk) + np.minimum(hb[..., 2], cap_v) * mk
        hb[..., 1] = hb[..., 1] * (1 - 0.8 * mk)
        band = cv2.cvtColor(np.clip(hb, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR)
        f[y0:] = band
    out.write(f)
    n += 1
out.release()
print(f"frames={n} y0={y0}")
