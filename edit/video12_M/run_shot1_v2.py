#!/usr/bin/env python3
"""Video 12 shot 1 (frames 1..30 = 0-1.233 s): exact board M fitted to the hood on frame 1 (edit/video12_M/f0_CAD.npy),
tracked per frame with affine ECC of the car region; old M/pinstripe removed with clean_red_graphics.py, new M painted with
hood_m_still.py. Output frames: edit/video12_M/out2/fNNN.png. Run from the project root."""
import subprocess, sys
from pathlib import Path
import cv2, numpy as np
D = Path("edit/video12_M"); O = D / "out4"; T = D / "tmp"; O.mkdir(exist_ok=True); T.mkdir(exist_ok=True)
C, A, Dv = np.load(D / "f0_CAD.npy")
vent = np.array([[145, 651], [205, 622], [301, 635], [265, 657], [175, 662]], float)
box = np.array([[95, 600], [315, 600], [315, 722], [95, 722]], float)
g = lambda p: cv2.cvtColor(cv2.imread(str(p)), cv2.COLOR_BGR2GRAY).astype(np.float32)
roi = (slice(590, 740), slice(40, 360)); g0 = g(D / "f001.png")[roi]
def oldM(i):                                   # centroid of the old red M (largest red blob on the hood)
    f = cv2.imread(str(D / f"f{i:03d}.png")); b_, g_, r_ = [c.astype(np.int16) for c in cv2.split(f)]
    m = ((r_ - np.maximum(g_, b_)) > 40) & (r_ > 70); bx_ = np.zeros_like(m); bx_[620:740, 110:330] = True; m &= bx_
    n, lab, st, cen = cv2.connectedComponentsWithStats(m.astype(np.uint8)); k = 1 + np.argmax(st[1:, 4])
    return [cen[k][0], cen[k][1], st[k, 2], st[k, 3]]
obs = np.array([oldM(i) for i in range(1, 31)]); t = np.arange(30)
fit = np.stack([np.polyval(np.polyfit(t, obs[:, j], 2), t) for j in range(4)], 1)   # smoothed old-M path + size
prev = np.eye(2, 3, dtype=np.float32)
py = sys.executable
for i in range(1, 31):
    fi = D / f"f{i:03d}.png"
    sc = 0.5 * (fit[i - 1, 2] / fit[0, 2] + fit[i - 1, 3] / fit[0, 3])      # scale from old-M box size
    Wf = np.array([[sc, 0, 0], [0, sc, 0], [0, 0, 1]], float)
    Wf[:2, 2] = fit[i - 1, :2] - sc * fit[0, :2]                            # old-M centre follows its measured path
    tp = lambda P: (np.c_[P, np.ones(len(P))] @ Wf[:2].T)
    tv = lambda v: Wf[:2, :2] @ v
    c = tp(C[None])[0]; a = tv(A); d = tv(Dv); vp = tp(vent); bx = tp(box)
    x0, y0 = np.floor(bx.min(0)).astype(int); x1, y1 = np.ceil(bx.max(0)).astype(int)
    cl, out = T / f"c{i:03d}.png", O / f"f{i:03d}.png"
    for p in (cl, out):
        p.unlink(missing_ok=True)
    subprocess.run([py, "edit/tools/clean_red_graphics.py", str(fi), str(cl), "--box", str(max(x0, 0)), str(y0), str(x1), str(y1),
                    "--thr", "25", "--badge", "0", "0", "1", "1", "--grain", "0.25"], check=True, capture_output=True)
    subprocess.run([py, "edit/tools/clean_red_graphics.py", str(cl), str(cl) + ".r.png", "--box", "180", "490", "680", "575",
                    "--thr", "22", "--badge", "0", "0", "1", "1", "--grain", "0.25"], check=True, capture_output=True)
    Path(str(cl) + ".r.png").replace(cl)                                   # roof stripes removed too
    subprocess.run([py, "edit/tools/hood_m_still.py", str(cl), str(out), "--center", f"{c[0]:.2f}", f"{c[1]:.2f}",
                    "--across", f"{a[0]:.2f}", f"{a[1]:.2f}", "--down", f"{d[0]:.2f}", f"{d[1]:.2f}",
                    "--color", "142", "30", "38", "--gloss", "0.05", "--shade-max", "1.1", "--texture", "0.6",
                    "--vent", " ".join(f"{x:.1f},{y:.1f}" for x, y in vp)], check=True, capture_output=True)
    if i in (1, 15, 30):
        print(i, np.round(Wf[:2], 3).tolist())
print("done")
