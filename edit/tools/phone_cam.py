#!/usr/bin/env python3
"""Phone-camera operator pass: keyframed digital zoom + roll (dutch) + target framing + autofocus hunting + hand shake.

Usage: .venv/bin/python edit/tools/phone_cam.py SPEC.json
SPEC: {"src", "out", "start": s, "end": s, "size": [1080,1920], "seed": 3,
       "keys": [{"t": 0.0, "zoom": 1.0, "roll": 0, "cx": 0.5, "cy": 0.5, "blur": 0, "shake": 1.0, "ev": 0}, ...],
       "ease": "smooth"}
  t = seconds from start; zoom >= 1 (crop factor on the source); roll in degrees (+ = clockwise dutch);
  cx/cy = framing target as a fraction of the source frame; blur = defocus sigma in output px (AF hunt);
  shake = hand-shake amplitude multiplier; ev = exposure offset in stops.
Values are interpolated between keys with smoothstep easing. Writes OUT (H.264 CRF 14, source audio trimmed).
Never overwrites.
"""
import json, math, subprocess, sys
from pathlib import Path
import cv2
import numpy as np

spec = json.loads(Path(sys.argv[1]).read_text())
out = Path(spec["out"])
if out.exists():
    sys.exit(f"refusing to overwrite {out}")
OW, OH = spec.get("size", [1080, 1920])
cap = cv2.VideoCapture(spec["src"]); fps = cap.get(cv2.CAP_PROP_FPS)
t0, t1 = spec.get("start", 0.0), spec.get("end", 1e9)
frames = []
i = 0
while True:
    ok, f = cap.read()
    if not ok:
        break
    t = i / fps
    if t0 - 1e-6 <= t < t1 - 1e-6:
        frames.append(f)
    i += 1
H, W = frames[0].shape[:2]
keys = sorted(spec["keys"], key=lambda k: k["t"])
FIELDS = ("zoom", "roll", "cx", "cy", "blur", "shake", "ev")
DEF = {"zoom": 1.0, "roll": 0.0, "cx": 0.5, "cy": 0.5, "blur": 0.0, "shake": 1.0, "ev": 0.0}

def val(field, t):
    pts = [(k["t"], k.get(field, None)) for k in keys]
    pts = [(a, b) for a, b in pts if b is not None] or [(0.0, DEF[field])]
    if t <= pts[0][0]:
        return pts[0][1]
    for (ta, va), (tb, vb) in zip(pts, pts[1:]):
        if t <= tb:
            u = (t - ta) / max(tb - ta, 1e-6); u = u * u * (3 - 2 * u)
            return va + (vb - va) * u
    return pts[-1][1]

rng = np.random.default_rng(spec.get("seed", 3))
ph = rng.uniform(0, 2 * math.pi, 12)
def shake(t):
    # hand drift (0.6-1.7 Hz) + road/engine vibration (7-13 Hz), in output pixels / degrees
    dx = 9 * math.sin(2 * math.pi * 0.7 * t + ph[0]) + 5 * math.sin(2 * math.pi * 1.7 * t + ph[1]) \
        + 2.2 * math.sin(2 * math.pi * 9.0 * t + ph[2]) + 1.4 * math.sin(2 * math.pi * 12.7 * t + ph[3])
    dy = 11 * math.sin(2 * math.pi * 0.6 * t + ph[4]) + 4 * math.sin(2 * math.pi * 1.9 * t + ph[5]) \
        + 2.6 * math.sin(2 * math.pi * 7.3 * t + ph[6]) + 1.6 * math.sin(2 * math.pi * 11.1 * t + ph[7])
    dr = 0.8 * math.sin(2 * math.pi * 0.5 * t + ph[8]) + 0.35 * math.sin(2 * math.pi * 2.3 * t + ph[9]) \
        + 0.15 * math.sin(2 * math.pi * 8.1 * t + ph[10])
    return dx, dy, dr

proc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-n", "-f", "rawvideo", "-pix_fmt", "bgr24",
                         "-s", f"{OW}x{OH}", "-r", str(fps), "-i", "-", "-ss", str(t0), "-i", spec["src"],
                         "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "14", "-preset", "slow",
                         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)],
                        stdin=subprocess.PIPE)
assert proc.stdin is not None
base = max(OW / W, OH / H)                       # cover scale from source to output
prev = None
for n, f in enumerate(frames):
    t = n / fps
    z, roll, cx, cy, blur, amp, ev = (val(k, t) for k in FIELDS)
    dx, dy, dr = shake(t)
    s = base * z
    ang = roll + dr * amp
    # affine: move target (cx,cy in source) to output centre (+shake), scale s, rotate ang
    M = cv2.getRotationMatrix2D((cx * W, cy * H), -ang, s)
    M[0, 2] += OW / 2 - cx * W + dx * amp
    M[1, 2] += OH / 2 - cy * H + dy * amp
    g = cv2.warpAffine(f, M, (OW, OH), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    if blur > 0.3:                               # defocus: soft disc-ish blur + highlight bloom
        k = int(blur * 3) | 1
        b = cv2.GaussianBlur(g, (k, k), blur)
        g = cv2.addWeighted(b, 1.0, cv2.GaussianBlur(b, (0, 0), blur * 2), 0.15, 0)
    if prev is not None and amp > 0.5:           # shutter motion blur from the shake velocity
        g = cv2.addWeighted(g, 0.78, prev, 0.22, 0)
    prev = g
    if abs(ev) > 1e-3:
        g = np.clip(g.astype(np.float32) * (2 ** ev), 0, 255).astype(np.uint8)
    noise = rng.normal(0, 4.0, (OH, OW, 1)).astype(np.float32)   # phone sensor grain
    g = np.clip(g.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    proc.stdin.write(g.tobytes())
proc.stdin.close(); proc.wait()
print("wrote", out, len(frames), "frames")
