#!/usr/bin/env python3
"""Video 12 shot 1 (frames 0-29): replace the old small hood M with the approved big matte M (car sheet v2).
- M alpha taken from the approved front 3/4 (carsheet_front34_bigM_matte_user_v1.png), aligned to the reference geometry
  (front34_nostripe.png) by ECC, then mapped onto frame 0 by a 4-point homography (vent tip, hood corner, shut line, mirror base).
- per frame: affine ECC track of the car region vs frame 0; old M + vent pinstripe removed (inpaint + regrain);
  new M painted deep red, shaded by the frame's own lighting, with the surface texture carried through.
Writes edit/video12_M/out/fNNN.png for frames 0..29 (others untouched). Run from the project root.
"""
import cv2, numpy as np
from pathlib import Path

D = Path("edit/video12_M"); OUT = D / "out"; OUT.mkdir(exist_ok=True)
A = cv2.imread("edit/car_sheet_m/front34_nostripe.png")
B = cv2.imread("assets/originals/capcut_gen/carsheet_front34_bigM_matte_user_v1.png")
Wsm = np.load(D / "B_to_A_small.npy")                       # A_small -> B_small
sA = 836 / A.shape[1]; sB = B.shape[1] / 836
# M alpha in B: solid mask extracted from the approved image (edit/video12_M/B_Mmask.png, smoothed + cleaned)
mB = cv2.imread(str(D / "B_Mmask.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0
mB = cv2.GaussianBlur(mB, (0, 0), 1.0)
# full-res A -> B affine
M_AB = np.vstack([Wsm, [0, 0, 1]]) @ np.diag([sA, sA, 1]); M_AB = np.diag([sB, sB, 1]) @ M_AB
mA = cv2.warpAffine(mB, M_AB[:2], (A.shape[1], A.shape[0]), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP)
# A -> frame0 homography from 4 correspondences
srcA = np.float32([[282, 360], [85, 432], [535, 522], [510, 272]])
dstF = np.float32([[145, 651], [65, 680], [255, 712], [240, 604]])
H = cv2.getPerspectiveTransform(srcA, dstF)
f0 = cv2.imread(str(D / "f001.png")); Hh, Ww = f0.shape[:2]
m0 = cv2.warpPerspective(mA, H, (Ww, Hh), flags=cv2.INTER_LINEAR)
m0 = cv2.GaussianBlur(m0, (0, 0), 0.5)

def gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
roi = (slice(560, 780), slice(0, 420))
g0 = gray(f0)[roi]
rng = np.random.default_rng(3)
for i in range(30):
    f = cv2.imread(str(D / f"f{i + 1:03d}.png"))
    W = np.eye(2, 3, dtype=np.float32)
    try:
        _, W = cv2.findTransformECC(g0, gray(f)[roi], W, cv2.MOTION_AFFINE,
                                    (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-5), None, 5)
    except cv2.error:
        pass
    # W maps roi(frame0) coords -> roi(frame i) coords; convert to full-frame affine
    T = np.array([[1, 0, -0], [0, 1, -560], [0, 0, 1]], np.float32)
    Wf = np.linalg.inv(T) @ np.vstack([W, [0, 0, 1]]) @ T
    alpha = cv2.warpAffine(m0, Wf[:2], (Ww, Hh), flags=cv2.INTER_LINEAR)
    # remove old red graphics on the hood
    bb, gg, rr = [c.astype(np.int16) for c in cv2.split(f)]
    red = ((rr - np.maximum(gg, bb)) > 25) & (rr > 50)
    box = np.zeros_like(red); box[600:722, 95:315] = True
    red = cv2.dilate((red & box).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=2)
    clean = cv2.inpaint(f, red * 255, 5, cv2.INPAINT_TELEA).astype(np.float32)
    lum = gray(f)
    hp = lum - cv2.GaussianBlur(lum, (0, 0), 1.5)
    noise = rng.normal(0, min(max(hp[640:700, 60:120].std() * 0.5, 1.5), 5.0), lum.shape).astype(np.float32)
    clean += (noise * cv2.GaussianBlur(red.astype(np.float32), (0, 0), 1.5))[..., None]
    # paint the approved M (deep red, matte), shaded by the cleaned surface
    cl = cv2.cvtColor(np.clip(clean, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    ys, xs = np.where(alpha > 0.5)
    ref = max(np.median(cl[ys, xs]), 1.0) if len(ys) else 60.0
    rel = cv2.GaussianBlur(cl, (0, 0), 1.5) / ref
    paint = np.float32([38, 30, 142])[None, None, :] * np.clip(0.75 + 0.25 * rel, 0.55, 1.15)[..., None]
    paint *= (((cl + 1) / (cv2.GaussianBlur(cl, (0, 0), 2.0) + 1)) ** 0.6)[..., None]
    a3 = alpha[..., None]
    res = clean * (1 - a3) + paint * a3
    cv2.imwrite(str(OUT / f"f{i + 1:03d}.png"), np.clip(res, 0, 255).astype(np.uint8))
    if i in (0, 15, 29):
        print(i, "track", np.round(Wf[:2], 3).tolist())
print("done")
