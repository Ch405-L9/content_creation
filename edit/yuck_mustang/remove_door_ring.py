#!/usr/bin/env python3
"""Remove the leftover white door-roundel ring from a CapCut S2/S3 edit.

Per frame: in the lower door band, find bright low-saturation connected components that are large
(the ring arc / bar), skip small ones (paint highlights), dilate and inpaint. Audio is not touched
(finish.sh re-muxes the original audio afterwards).
usage: remove_door_ring.py IN.mp4 OUT.mp4 [Y_TOP_FRACTION=0.80]
"""
import sys
import cv2
import numpy as np

src, dst = sys.argv[1], sys.argv[2]
ytop_f = float(sys.argv[3]) if len(sys.argv) > 3 else 0.80
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
y0 = int(h * ytop_f)
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
n = 0
while True:
    ok, f = cap.read()
    if not ok:
        break
    band = f[y0:]
    hsv = cv2.cvtColor(band, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 2] > 150) & (hsv[..., 1] < 60)).astype(np.uint8)
    cnt, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros_like(m)
    for i in range(1, cnt):
        x, y, bw, bh, area = stats[i]
        if bw > w * 0.18 or (area > 400 and bh > 25):  # ring arc / inner bar, not a small specular glint
            keep[lab == i] = 1
    # dark inner disc of the old roundel: large dark blob touching the bottom edge
    dark = (hsv[..., 2] < np.percentile(hsv[..., 2], 35) * 0.75).astype(np.uint8)
    dark = cv2.morphologyEx(dark, cv2.MORPH_OPEN, k)
    cnt2, lab2, st2, _ = cv2.connectedComponentsWithStats(dark, 8)
    bh_band = band.shape[0]
    for i in range(1, cnt2):
        x, y, bw, bh, area = st2[i]
        if y + bh >= bh_band - 2 and bw > w * 0.2 and y > bh_band * 0.25:
            keep[lab2 == i] = 1
    if keep.any():
        keep = cv2.dilate(keep, k, iterations=2)
        band = cv2.inpaint(band, keep * 255, 7, cv2.INPAINT_TELEA)
        # second pass: leftover bright blobs (digits) near the bottom edge
        hsv2 = cv2.cvtColor(band, cv2.COLOR_BGR2HSV)
        m2 = ((hsv2[..., 2] > 140) & (hsv2[..., 1] < 70)).astype(np.uint8)
        c3, l3, s3, _ = cv2.connectedComponentsWithStats(m2, 8)
        k2 = np.zeros_like(m2)
        for i in range(1, c3):
            x, y, bw, bh, area = s3[i]
            if area > 150 and y > band.shape[0] * 0.55:
                k2[l3 == i] = 1
        if k2.any():
            band = cv2.inpaint(band, cv2.dilate(k2, k, iterations=2) * 255, 9, cv2.INPAINT_TELEA)
        f[y0:] = band
    out.write(f)
    n += 1
out.release()
print(f"frames={n} y0={y0}")
