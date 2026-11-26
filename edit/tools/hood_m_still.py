#!/usr/bin/env python3
"""Paint the board's authoritative 'M' (gloss red, Vette-style) onto a car hood in a still image.

Usage: .venv/bin/python edit/tools/hood_m_still.py IN OUT --center cx cy --across ax ay --down dx dy
         [--color R G B] [--gloss 0.35] [--debug DEBUG.png]
  --center  image point for the centre of the M's bounding box
  --across  image vector spanning the M's full width (car lateral direction on the hood)
  --down    image vector spanning the M's full height, from the peaks (windshield side) to the leg tips (nose)
  The two vectors define the hood-plane mapping (affine), so the letter lies flat on the hood in perspective.
Shape: assets/graphics/board_refs/board_M_poly.npy (traced from the Music Video Stills board, Chaikin-smoothed).
Never overwrites.
"""
import argparse, sys
from pathlib import Path
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--center", type=float, nargs=2, required=True)
ap.add_argument("--across", type=float, nargs=2, required=True)
ap.add_argument("--down", type=float, nargs=2, required=True)
ap.add_argument("--color", type=int, nargs=3, default=[206, 22, 34])     # Vette gloss red (RGB)
ap.add_argument("--gloss", type=float, default=0.35)                     # strength of the hood's reflections on the paint
ap.add_argument("--shade-max", type=float, default=1.35)                 # cap on hood-light brightening (lower = flatter / matte)
ap.add_argument("--poly", default="assets/graphics/board_refs/board_M_poly.npy")
ap.add_argument("--cut", nargs="*", default=[],
                help='polygons left unpainted (vent openings), each "x,y x,y ..." in image px')
ap.add_argument("--vent", nargs="*", default=[],
                help='vent polygons: paint stays on the slat faces (darker, recessed) but is cut along the slat edges')
ap.add_argument("--debug")
a = ap.parse_args()
out = Path(a.out)
if out.exists():
    sys.exit(f"refusing to overwrite {out}")

P = np.load(a.poly)
for _ in range(2):                                    # Chaikin smoothing of the traced outline
    Q = np.roll(P, -1, 0)
    P = np.vstack([np.column_stack([0.75 * P[:, 0] + 0.25 * Q[:, 0], 0.75 * P[:, 1] + 0.25 * Q[:, 1]]),
                   np.column_stack([0.25 * P[:, 0] + 0.75 * Q[:, 0], 0.25 * P[:, 1] + 0.75 * Q[:, 1]])]).reshape(2, -1, 2).transpose(1, 0, 2).reshape(-1, 2)
x0, y0 = P.min(0); x1, y1 = P.max(0)
u = (P[:, 0] - (x0 + x1) / 2) / (x1 - x0)             # -0.5..0.5 across
v = (P[:, 1] - (y0 + y1) / 2) / (y1 - y0)             # -0.5..0.5 down
C = np.array(a.center); A = np.array(a.across); D = np.array(a.down)
img_pts = C + u[:, None] * A + v[:, None] * D

f = cv2.imread(a.inp, cv2.IMREAD_COLOR)
H, W = f.shape[:2]
k = 4
m = np.zeros((H * k, W * k), np.uint8)
cv2.fillPoly(m, [np.round(img_pts * k).astype(np.int32)], 255, lineType=cv2.LINE_AA)
alpha = cv2.resize(m, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
if a.cut:                                              # paint stops at the vent openings ("cut to fit the vents")
    cm = np.zeros((H * k, W * k), np.uint8)
    for poly in a.cut:
        pts = np.array([[float(v) for v in q.split(",")] for q in poly.split()])
        cv2.fillPoly(cm, [np.round(pts * k).astype(np.int32)], 255, lineType=cv2.LINE_AA)
    alpha *= 1 - cv2.resize(cm, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
vent = np.zeros((H, W), np.float32)
if a.vent:
    vm = np.zeros((H * k, W * k), np.uint8)
    for poly in a.vent:
        pts = np.array([[float(v) for v in q.split(",")] for q in poly.split()])
        cv2.fillPoly(vm, [np.round(pts * k).astype(np.int32)], 255, lineType=cv2.LINE_AA)
    vent = cv2.resize(vm, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
    g0 = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    edges = cv2.dilate(((g0 > 62) & (vent > 0.5)).astype(np.uint8), np.ones((2, 2), np.uint8)).astype(np.float32)
    alpha *= 1 - edges                                 # slat edges / gaps stay visible -> the M reads as cut by the vent
alpha = cv2.GaussianBlur(alpha, (0, 0), 0.6)[..., None]

lum = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32)
ys, xs = np.where(alpha[..., 0] > 0.5)
ref = max(np.median(lum[ys, xs]), 1.0)
rel = cv2.GaussianBlur(lum, (0, 0), 2.0) / ref           # hood shading under the letter
base = np.float32(a.color[::-1])[None, None, :]
paint = base * np.clip(0.75 + 0.25 * rel, 0.55, a.shade_max)[..., None]
spec = np.clip(rel - 1.0, 0, 3)[..., None] * 255 * a.gloss   # reflections stay visible = gloss clearcoat
paint = np.clip(paint + spec, 0, 255)
paint = paint * (1 - 0.35 * vent[..., None])               # recessed slat faces sit in shadow
res = f.astype(np.float32) * (1 - alpha) + paint * alpha
cv2.imwrite(str(out), np.clip(res, 0, 255).astype(np.uint8))
if a.debug:
    x, y = int(xs.min()), int(ys.min())
    cv2.imwrite(a.debug, np.clip(res, 0, 255).astype(np.uint8)[max(0, y - 120):int(ys.max()) + 120, max(0, x - 200):int(xs.max()) + 200])
print("wrote", out, "M bbox", int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
