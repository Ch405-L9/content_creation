#!/usr/bin/env python3
"""Composite an exact logo onto a car hood: remove old red graphic, perspective-warp the logo, shade it like paint.

Usage: .venv/bin/python edit/tools/hood_logo.py SPEC.json
SPEC: {"src", "out", "logo", "hood": [[x,y]x4 cowl-L,cowl-R,nose-R,nose-L],
       "logo_quad": [[x,y]x4 TL,TR,BR,BL], "laser": [[x1,y1],[x2,y2],width] or null,
       "red_box": [x0,y0,x1,y1], "paint": [R,G,B], "opacity": 0.95}
Writes the output plus <out>.debug.png (mask/quad overlay). Never overwrites.
"""
import json, sys
from pathlib import Path
import cv2
import numpy as np

spec = json.loads(Path(sys.argv[1]).read_text())
src, out = Path(spec["src"]), Path(spec["out"])
if out.exists():
    sys.exit(f"refusing to overwrite {out}")
img = cv2.imread(str(src), cv2.IMREAD_COLOR)
h, w = img.shape[:2]

# 1) hood polygon and laser exclusion band
hood = np.zeros((h, w), np.uint8)
cv2.fillPoly(hood, [np.array(spec["hood"], np.int32)], 255)
laser = np.zeros((h, w), np.uint8)
if spec.get("laser"):
    (x1, y1), (x2, y2), lw = spec["laser"]
    cv2.line(laser, (int(x1), int(y1)), (int(x2), int(y2)), 255, int(lw))

# 2) old red graphic mask (inside hood box, not laser), dilated, then inpaint
b, g, r = [c.astype(np.int16) for c in cv2.split(img)]
red = ((r - np.maximum(g, b)) > 40) & (r > 70)
box = np.zeros((h, w), bool)
x0, y0, x1, y1 = spec["red_box"]
box[y0:y1, x0:x1] = True
mask = (red & box & (hood > 0) & (laser == 0)).astype(np.uint8) * 255
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=spec.get("dilate", 2))
mask[laser > 0] = 0
clean = cv2.inpaint(img, mask, spec.get("inpaint_radius", 9), cv2.INPAINT_TELEA)
# re-grain the inpainted area so it matches the surrounding matte-paint texture
if spec.get("regrain", True):
    ring = cv2.dilate(mask, np.ones((25, 25), np.uint8)) & ~mask & hood
    hp = img.astype(np.float32) - cv2.GaussianBlur(img, (0, 0), 2).astype(np.float32)
    vals = hp[ring > 0].ravel()
    std = float(1.4826 * np.median(np.abs(vals - np.median(vals)))) if vals.size else 2.0  # robust (MAD) grain level
    std *= spec.get("regrain_strength", 0.6)
    rng = np.random.default_rng(7)
    noise = cv2.GaussianBlur(rng.normal(0, 1, img.shape[:2]).astype(np.float32), (0, 0), 0.7)
    noise = (noise / (noise.std() + 1e-6) * std)[..., None]
    soft = cv2.GaussianBlur(mask.astype(np.float32) / 255.0, (0, 0), 3)[..., None]
    clean = np.clip(clean.astype(np.float32) + noise * soft, 0, 255).astype(np.uint8)

# 3) logo alpha from red-on-white artwork, warped onto the hood quad
logo = cv2.imread(spec["logo"], cv2.IMREAD_COLOR)
lb, lg, lr = [c.astype(np.float32) for c in cv2.split(logo)]
alpha_logo = np.clip((lr - np.maximum(lg, lb)) / 120.0, 0, 1)
if spec.get("bold", 0):  # thicken strokes so the logo survives strong foreshortening
    k = int(spec["bold"]); alpha_logo = cv2.dilate(alpha_logo, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
lh, lw_ = alpha_logo.shape
srcq = np.float32([[0, 0], [lw_, 0], [lw_, lh], [0, lh]])
dstq = np.float32(spec["logo_quad"])
M = cv2.getPerspectiveTransform(srcq, dstq)
alpha = cv2.warpPerspective(alpha_logo, M, (w, h), flags=cv2.INTER_CUBIC)
alpha = cv2.GaussianBlur(alpha, (3, 3), 0) * spec.get("opacity", 0.95)
alpha *= (hood > 0)
alpha *= (1.0 - cv2.GaussianBlur(laser.astype(np.float32) / 255.0, (9, 9), 0))  # laser stays on top

# 4) paint shading: modulate paint colour by the hood's local luminance (keeps reflections/highlights)
lum = cv2.cvtColor(clean, cv2.COLOR_BGR2GRAY).astype(np.float32)
lum_s = cv2.GaussianBlur(lum, (0, 0), 3)
ref = np.percentile(lum_s[hood > 0], 60) + 1e-3
shade = np.clip(lum_s / ref, 0.25, 2.2)[..., None]
pr, pg, pb = spec.get("paint", [200, 22, 28])
paint = np.clip(np.float32([pb, pg, pr])[None, None, :] * shade * 0.9 + lum_s[..., None] * 0.12, 0, 255)
result = clean.astype(np.float32) * (1 - alpha[..., None]) + paint * alpha[..., None]
result = result.astype(np.uint8)
cv2.imwrite(str(out), result)

dbg = result.copy()
cv2.polylines(dbg, [np.array(spec["hood"], np.int32)], True, (0, 255, 255), 1)
cv2.polylines(dbg, [dstq.astype(np.int32)], True, (255, 255, 0), 1)
dbg[mask > 0] = (dbg[mask > 0] * 0.5 + np.array([255, 0, 255]) * 0.5).astype(np.uint8)
cv2.imwrite(str(out) + ".debug.png", dbg)
print("wrote", out, "mask px", int((mask > 0).sum()))
