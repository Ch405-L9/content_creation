#!/usr/bin/env python3
"""S5: replace the Corvette crossed-flags badge on the (static) steering-wheel hub with the chrome Mustang pony.
usage: wheel_badge_plate.py IN.mp4 PLATE.png MASK.png CX CY PONY_W   (writes plate + mask for hood_fix_static.py --apply)"""
import sys, cv2, numpy as np
src, plate_p, mask_p = sys.argv[1:4]; cx, cy, pw = map(int, sys.argv[4:7])
cap = cv2.VideoCapture(src); ok, f = cap.read()
# 1) inpaint the old badge (bright / red pixels inside the hub disc)
r = int(pw * 0.75)
roi = f[cy - r:cy + r, cx - r:cx + r]
hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
bad = (((hsv[..., 2] > 70) & (hsv[..., 1] < 90)) | (((hsv[..., 0] < 12) | (hsv[..., 0] > 165)) & (hsv[..., 1] > 70) & (hsv[..., 2] > 50))).astype(np.uint8)
yy, xx = np.mgrid[-r:r, -r:r]; bad[(xx**2 / (r * 0.95)**2 + yy**2 / (r * 0.7)**2) > 1] = 0
bad = cv2.dilate(bad, np.ones((5, 5), np.uint8), iterations=2)
roi = cv2.inpaint(roi, bad * 255, 6, cv2.INPAINT_TELEA)
# 2) pony from the approved grille close-up
e = cv2.imread("assets/mustang-sc-proto/capcut_inputs/emblem_key_v1.jpg")
pc = e[1220:1560, 560:1120]
pm = (cv2.cvtColor(pc, cv2.COLOR_BGR2HSV)[..., 2] > 120).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(pm, 8); big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
pm = (lab == big).astype(np.uint8)
x, y, w, h = cv2.boundingRect(pm); pc, pm = pc[y:y + h, x:x + w], pm[y:y + h, x:x + w]
ph = int(h * pw / w); pc = cv2.resize(pc, (pw, ph), interpolation=cv2.INTER_AREA)
pa = cv2.GaussianBlur(cv2.resize(pm.astype(np.float32), (pw, ph)), (3, 3), 0)[..., None]
pc = (pc.astype(np.float32) * 0.75)          # dim chrome to the cabin's night light level
y0, x0 = r - ph // 2, r - pw // 2
sub = roi[y0:y0 + ph, x0:x0 + pw].astype(np.float32)
roi[y0:y0 + ph, x0:x0 + pw] = (pc * pa + sub * (1 - pa)).astype(np.uint8)
plate = f.copy(); plate[cy - r:cy + r, cx - r:cx + r] = roi
cv2.imwrite(plate_p, plate)
mask = np.zeros(f.shape[:2], np.uint8)
cv2.ellipse(mask, (cx, cy), (int(r * 0.98), int(r * 0.75)), 0, 0, 360, 255, -1)
cv2.imwrite(mask_p, mask); print("ok", pw, ph)
