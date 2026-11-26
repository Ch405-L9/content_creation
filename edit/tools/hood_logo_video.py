#!/usr/bin/env python3
"""Replace an AI-generated red hood "M" in a video with the true Mach 5 logo (matte deep red), frame by frame.

Usage: .venv/bin/python edit/tools/hood_logo_video.py IN OUT --frames 49 68 --fit 52 63
       [--scale 1.5] [--paint 112 12 18] [--ylim 480 640] [--debug DIR]
- detects the largest red blob (the AI M) in --ylim per frame, fits a smooth quadratic path for centre/size over
  the --fit frames (clean detections) and uses it for every frame in --frames (so edge/blurred frames follow too)
- inpaints the AI M, recolours remaining hood pinstripes to the paint colour, composites the logo upright with true
  proportions (height = scale x detected M height), matte shading, motion blur from the fitted velocity, regrain
Writes OUT (H.264 CRF 12, source audio copied). Never overwrites.
"""
import argparse, subprocess, sys
from pathlib import Path
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--frames", type=int, nargs=2, required=True)
ap.add_argument("--fit", type=int, nargs=2, required=True)
ap.add_argument("--scale", type=float, default=0.95)          # logo width = scale x detected M width
ap.add_argument("--aspect", type=float, default=0.95)         # w/h on the hood (true art 0.59; hood foreshortening)
ap.add_argument("--taper", type=float, default=0.82)          # far-edge width / near-edge width
ap.add_argument("--bold", type=int, default=18)              # stroke dilation at artwork resolution
ap.add_argument("--paint", type=int, nargs=3, default=[132, 14, 22])          # matte fill colour (RGB)
ap.add_argument("--box", type=float, nargs=2)                  # fit logo to the AI M box: width x sx, height x sy
ap.add_argument("--outline", type=int, nargs=2)                # gloss pinstripe around the M: gap width (artwork px)
ap.add_argument("--gloss", type=int, nargs=3, default=[228, 24, 34])           # pinstripe colour (RGB)
ap.add_argument("--ylim", type=int, nargs=2, default=[480, 640])
ap.add_argument("--logo", default="assets/graphics/mach5_logo_ref/mach5_logo_pngegg.png")
ap.add_argument("--debug")
a = ap.parse_args()
out = Path(a.out)
if out.exists():
    sys.exit(f"refusing to overwrite {out}")

cap = cv2.VideoCapture(a.inp); fps = cap.get(cv2.CAP_PROP_FPS); frames = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    frames.append(f)
H, W = frames[0].shape[:2]

def red_mask(f, thr=40):
    b, g, r = [c.astype(np.int16) for c in cv2.split(f)]
    return (((r - np.maximum(g, b)) > thr) & (r > 70)).astype(np.uint8)

def detect(f, prev=None):
    n, lab, st, cen = cv2.connectedComponentsWithStats(red_mask(f))
    c = [k for k in range(1, n) if st[k, 4] > 150 and a.ylim[0] < cen[k][1] < a.ylim[1]]
    if prev is not None:
        c = [k for k in c if abs(cen[k][0] - prev[0]) < 120]
    if not c:
        return None, None
    k = max(c, key=lambda k: st[k, 4])
    x, y, w, h = st[k, :4]
    return (x + w / 2, y + h / 2, w, h), (lab == k)

# 1) detections on the clean fit range -> quadratic paths
obs, prev = {}, None
for i in range(a.fit[0], a.fit[1] + 1):
    d, _ = detect(frames[i], prev)
    if d:
        obs[i] = d; prev = d
idx = np.array(sorted(obs)); P = np.array([obs[i] for i in idx])
fits = [np.polyfit(idx, P[:, j], 2) for j in range(4)]
def at(j, i):                                                  # quadratic inside the fit range, linear outside
    e = min(max(i, a.fit[0]), a.fit[1])
    return np.polyval(fits[j], e) + np.polyval(np.polyder(fits[j]), e) * (i - e)
path = {i: [float(at(j, i)) for j in range(4)] for i in range(a.frames[0], a.frames[1] + 1)}
print("fit frames", len(idx), "path", {i: [round(v) for v in path[i]] for i in (a.frames[0], a.frames[1])})

# 2) logo alpha (red-on-white artwork), cropped to its bounds
logo = cv2.imread(a.logo, cv2.IMREAD_COLOR)
lb, lg, lr = [c.astype(np.float32) for c in cv2.split(logo)]
la = np.clip((lr - np.maximum(lg, lb)) / 120.0, 0, 1)
ys, xs = np.where(la > 0.2); la = la[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
pad = a.bold + (sum(a.outline) + 4 if a.outline else 0)
la = np.pad(la, pad)
if a.bold:
    la = cv2.dilate(la, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (a.bold, a.bold)))
ring = None
if a.outline:                                                  # pinstripe ring offset around the letter
    gap, wid = a.outline
    el = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    ring = np.clip(cv2.dilate(la, el(gap + wid)) - cv2.dilate(la, el(gap)), 0, 1)
pb, pg, pr = a.paint[2], a.paint[1], a.paint[0]
rng = np.random.default_rng(5)
dbg = Path(a.debug) if a.debug else None
if dbg:
    dbg.mkdir(parents=True, exist_ok=True)

for i, (cx, cy, mw, mh) in path.items():
    f = frames[i]
    _, body = detect(f, (cx, cy))
    # AI M region: detected blob (if any) + fitted box, dilated
    m = np.zeros((H, W), np.uint8)
    cv2.ellipse(m, (int(cx), int(cy)), (int(mw * 0.8), int(mh * 0.9)), 0, 0, 360, 1, -1)
    m &= red_mask(f, 18)
    if body is not None:
        m |= body.astype(np.uint8)
    m = cv2.dilate(m, np.ones((5, 5), np.uint8), iterations=2) * 255
    clean = cv2.inpaint(f, m, 7, cv2.INPAINT_TELEA)
    # recolour remaining hood pinstripes to the matte paint colour
    band = np.zeros((H, W), np.uint8)
    cv2.rectangle(band, (0, int(cy - 1.6 * mh)), (W, int(cy + 0.5 * mh)), 1, -1)   # stays above the headlights
    bright = cv2.cvtColor(clean, cv2.COLOR_BGR2GRAY) > 150
    sm = (red_mask(clean, 30) & band & ~bright).astype(np.float32)
    sm = cv2.GaussianBlur(sm, (0, 0), 1.0)[..., None]
    lum = cv2.cvtColor(clean, cv2.COLOR_BGR2GRAY).astype(np.float32)
    lum_s = cv2.GaussianBlur(lum, (0, 0), 3)
    ref = max(np.percentile(lum_s[int(cy - mh):int(cy + mh), max(0, int(cx - mw)):int(cx + mw)], 60), 1.0)
    shade = np.clip(lum_s / ref, 0.7, 1.15)[..., None]            # compressed range = matte, no glossy hot spots
    paint = np.float32([pb, pg, pr])[None, None, :] * shade
    # high-gloss red: stretched shading + specular highlight from the hood's own reflections
    gshade = np.clip(lum_s / ref, 0.55, 1.9)[..., None]
    spec = np.clip((lum_s - ref * 1.15) / max(ref, 1.0), 0, 1.5)[..., None] * 90
    gloss = np.clip(np.float32(a.gloss[::-1])[None, None, :] * gshade + spec, 0, 255)
    clean = (clean * (1 - sm) + (gloss if a.outline else paint) * sm).astype(np.float32)
    # logo layer: flat on the hood - foreshortened height, narrower at the far (windshield) edge
    if a.box:
        lw = max(4, int(round(mw * a.box[0]))); lh = max(4, int(round(mh * a.box[1])))
    else:
        lw = max(4, int(round(mw * a.scale))); lh = int(round(lw / a.aspect))
    t = (1 - a.taper) * lw / 2
    srcq = np.float32([[0, 0], [la.shape[1], 0], [la.shape[1], la.shape[0]], [0, la.shape[0]]])
    dstq = np.float32([[cx - lw / 2 + t, cy - lh / 2], [cx + lw / 2 - t, cy - lh / 2],
                       [cx + lw / 2, cy + lh / 2], [cx - lw / 2, cy + lh / 2]])
    PT = cv2.getPerspectiveTransform(srcq, dstq)
    full = cv2.warpPerspective(la, PT, (W, H), flags=cv2.INTER_AREA)
    rfull = cv2.warpPerspective(ring, PT, (W, H), flags=cv2.INTER_AREA) if ring is not None else None
    # motion blur along the fitted velocity
    vx = np.polyval(np.polyder(fits[0]), i); vy = np.polyval(np.polyder(fits[1]), i)
    L = int(min(40, np.hypot(vx, vy) * 0.6))
    if L >= 3:
        k = np.zeros((L, L), np.float32); ang = np.arctan2(vy, vx)
        c0 = (L - 1) / 2
        cv2.line(k, (int(c0 - np.cos(ang) * c0), int(c0 - np.sin(ang) * c0)),
                 (int(c0 + np.cos(ang) * c0), int(c0 + np.sin(ang) * c0)), 1, 1)
        full = cv2.filter2D(full, -1, k / k.sum())
        if rfull is not None:
            rfull = cv2.filter2D(rfull, -1, k / k.sum())
    full = cv2.GaussianBlur(full, (3, 3), 0) * 0.95
    res = clean * (1 - full[..., None]) + paint * full[..., None]
    if rfull is not None:
        rfull = np.clip(cv2.GaussianBlur(rfull, (3, 3), 0) * 1.1, 0, 1)
        res = res * (1 - rfull[..., None]) + gloss * rfull[..., None]
        full = np.maximum(full, rfull)
    noise = cv2.GaussianBlur(rng.normal(0, 3.0, (H, W)).astype(np.float32), (0, 0), 0.7)[..., None]
    res = np.clip(res + noise * np.maximum(full, m / 255.0)[..., None], 0, 255).astype(np.uint8)
    frames[i] = res
    if dbg:
        cv2.imwrite(str(dbg / f"f{i:03d}.png"), res[max(0, int(cy - 160)):int(cy + 200), :])

proc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-n", "-f", "rawvideo", "-pix_fmt", "bgr24",
                         "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-i", a.inp, "-map", "0:v", "-map", "1:a?",
                         "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "copy",
                         "-shortest", str(out)], stdin=subprocess.PIPE)
assert proc.stdin is not None
for f in frames:
    proc.stdin.write(f.tobytes())
proc.stdin.close(); proc.wait()
print("wrote", out)
