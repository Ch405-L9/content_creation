#!/usr/bin/env python3
"""S4 mirror shots: the hood seen through the windshield is static (fixed in-car camera).
Step 1 (--plate): from frame 0, repaint the hood band matte black (keeps soft shading and the street-light
         glints) and save a plate PNG; then run edit/tools/hood_m_still.py on it to add the board M.
Step 2 (--apply): composite that finished plate over the hood mask on every frame.
usage:
  hood_fix_static.py --plate IN.mp4 PLATE.png MASK.png
  hood_fix_static.py --apply IN.mp4 PLATE_WITH_M.png MASK.png OUT.mp4
"""
import sys
import cv2
import numpy as np

Y0, Y1 = 1100, 1242          # hood band in the 720x1280 CapCut frame (above the wiper / cowl line)

def first_frame(p):
    cap = cv2.VideoCapture(p); ok, f = cap.read(); return f

if sys.argv[1] == "--plate":
    src, plate_p, mask_p = sys.argv[2:5]
    f = first_frame(src)
    band = f[Y0:Y1].copy()
    hsv = cv2.cvtColor(band, cv2.COLOR_BGR2HSV)
    v, s, hh = hsv[..., 2].astype(np.float32), hsv[..., 1], hsv[..., 0]
    white = (v > 95) & (s < 70)
    red = ((hh < 12) | (hh > 165)) & (s > 80) & (v > 60)
    m = (white | red).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros_like(m)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 2000:
            keep[lab == i] = 1
    keep = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8))
    # smooth hood silhouette: top edge per column -> quadratic fit, fill down to the cowl line
    cols = np.where(keep.any(0))[0]
    tops = np.array([np.argmax(keep[:, c]) for c in cols])
    coef = np.polyfit(cols, tops, 2)
    xs = np.arange(keep.shape[1]); ytop = np.clip(np.polyval(coef, xs), 0, keep.shape[0] - 1).astype(int)
    keep = np.zeros_like(keep)
    for x in xs:
        keep[ytop[x]:, x] = 1
    cowl = (v < 60)                       # keep the dark cowl / wiper strip at the bottom untouched
    keep[(cowl) & (np.arange(keep.shape[0])[:, None] > keep.shape[0] * 0.75)] = 0
    # matte black paint: low base with a little of the original shading; specular glints kept, dimmed
    g = cv2.GaussianBlur(v, (0, 0), 6)
    shade = 14 + 0.10 * g
    glint = np.clip(v - 225, 0, None) * 2.5
    paint = np.clip(shade + glint, 0, 255)
    painted = np.dstack([paint * 0.95, paint * 0.97, paint]).astype(np.uint8)
    out = band.copy(); out[keep > 0] = painted[keep > 0]
    full = f.copy(); full[Y0:Y1] = out
    cv2.imwrite(plate_p, full)
    mask = np.zeros(f.shape[:2], np.uint8); mask[Y0:Y1] = keep * 255
    cv2.imwrite(mask_p, mask)
    print("plate written; hood px", int(keep.sum()))
elif sys.argv[1] == "--apply":
    src, plate_p, mask_p, dst = sys.argv[2:6]
    plate = cv2.imread(plate_p).astype(np.float32)
    mask = cv2.GaussianBlur(cv2.imread(mask_p, 0).astype(np.float32) / 255, (0, 0), 2.5)[..., None]
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS); w = int(cap.get(3)); h = int(cap.get(4))
    vw = cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h)); n = 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        vw.write((plate * mask + f.astype(np.float32) * (1 - mask)).astype(np.uint8)); n += 1
    vw.release(); print("frames", n)
