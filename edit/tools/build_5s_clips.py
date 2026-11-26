#!/usr/bin/env python3
"""Build standalone 5-second Met Gala-style clips (one per intro still): motion + grade + tag + sound, -14 LUFS.

Run from the project root: python3 edit/tools/build_5s_clips.py
Outputs (never overwritten): review/clips_5s/<name>_5s_v1.mp4
"""
import argparse, subprocess, sys
from pathlib import Path

ROOT = Path.cwd(); OUT = ROOT / "review/clips_5s"; WORK = ROOT / "edit/finish_clips_5s"
OUT.mkdir(parents=True, exist_ok=True); WORK.mkdir(parents=True, exist_ok=True)
G, P, Y, Z = "assets/originals/capcut_gen/", "assets/proxies/", "assets/audio/sfx_synth/", "assets/originals/sfx_zr1x/"
DUR = 5.0
# name, still, zoom_end, x_drift, extra sound cues [(file, start, gain)]
CLIPS = [
    ("01_pendant", G + "pendant_shot1_v1.png", 0.18, 0.0, [(Y + "impact_boom.wav", 0.0, 0.7), (Y + "tape_stop.wav", 4.4, 0.5)]),
    ("02_gordon", G + "gordon_walk_shot2_v1.png", 0.22, 0.0, [(Y + "whoosh_fast.wav", 0.0, 1.4), (Y + "heartbeat_3s6.wav", 1.2, 0.5)]),
    ("03_trixie", G + "trixie_shot3_v3.png", 0.16, 0.3, [(Y + "whoosh_fast.wav", 0.0, 1.4), (Y + "impact_boom.wav", 2.4, 0.45)]),
    ("04_mustang", P + "car_shot4_mach5logo_v5.png", 0.20, 0.0, [(Y + "impact_boom.wav", 0.0, 0.9), (Z + "sounds_high_rpm-gain.mp4", 0.05, 0.6),
                                                                (Z + "sounds_idle_rumble.mp4", 1.6, 0.4)]),
    ("05_gordon_trixie", P + "both_shot5_mach5logo_v3.png", 0.08, 0.35, [(Y + "whoosh_fast.wav", 0.0, 1.3), (Z + "sounds_idle_rumble.mp4", 0.8, 0.35)]),
]
LOOK = ("scale=1134:2016:flags=lanczos,crop=1080:1920:x='27+20*sin(t*0.9)':y='48+28*sin(t*0.7+1)',"
        "eq=contrast=1.08:saturation=0.88:brightness=-0.02,curves=master='0/0 0.12/0.04 0.5/0.47 1/1',"
        "noise=alls=12:allf=t+u,vignette=PI/5")
F = "/usr/share/fonts/opentype/urw-base35/NimbusSansNarrow-Bold.otf"
TAG = WORK / "tag.txt"; TAG.write_text("UNOFFICIAL FAN TRIBUTE · AI-GENERATED · FICTION")
TITLE = (f"drawtext=fontfile={F}:textfile={TAG}:expansion=none:fontsize=30:fontcolor=white@0.85"
         ":shadowcolor=black@0.85:shadowx=3:shadowy=3:x=(w-text_w)/2:y=h*0.135")

ap = argparse.ArgumentParser(); ap.add_argument("--only", nargs="*"); ap.add_argument("--version", default="v1")
ARGS = ap.parse_args()

def run(args):
    subprocess.run(args, check=True)

for name, still, zoom, xdrift, cues in CLIPS:
    if ARGS.only and name not in ARGS.only:
        continue
    V = ARGS.version
    final = OUT / f"{name}_5s_{V}.mp4"
    if final.exists():
        sys.exit(f"refusing to overwrite {final}")
    motion = WORK / f"{name}_{V}_motion.mp4"
    run([str(ROOT / "edit/tools/still_motion.sh"), str(ROOT / still), str(motion), str(DUR), str(zoom), str(xdrift)])
    pic = WORK / f"{name}_{V}_graded.mp4"
    run(["ffmpeg", "-nostdin", "-v", "error", "-n", "-i", str(motion), "-vf", f"{LOOK},{TITLE},format=yuv420p", "-an",
         "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-r", "24", "-frames:v", str(int(DUR * 24)), str(pic)])
    base = [(Y + "sub_drop.wav", 0.0, 0.8), (Y + "drone_low_3s.wav", 0.0, 0.45), (Y + "drone_low_3s.wav", 2.6, 0.4)] + cues
    ins, labs, g = [], [], []
    for i, (f, st, gain) in enumerate(base):
        ins += ["-i", str(ROOT / f)]; ms = int(st * 1000)
        g.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={gain},adelay={ms}|{ms}[c{i}]"); labs.append(f"[c{i}]")
    g.append("".join(labs) + f"amix=inputs={len(labs)}:normalize=0:duration=longest,alimiter=limit=0.89,"
             f"afade=t=out:st={DUR - 0.5}:d=0.5,apad=whole_dur={DUR},atrim=0:{DUR}[a]")
    gf = WORK / f"{name}_{V}_audio.txt"; gf.write_text(";\n".join(g))
    mix = WORK / f"{name}_{V}_mix.wav"
    run(["ffmpeg", "-nostdin", "-v", "error", "-n", *ins, "-filter_complex_script", str(gf), "-map", "[a]", "-c:a", "pcm_s24le", str(mix)])
    muxed = WORK / f"{name}_{V}_muxed.mp4"
    run(["ffmpeg", "-nostdin", "-v", "error", "-n", "-i", str(pic), "-i", str(mix), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(muxed)])
    run([sys.executable, str(ROOT / ".claude/skills/socmed-video-production/scripts/normalize_loudness.py"), str(muxed),
         "--root", str(ROOT), "--output", str(final), "--target-lufs", "-14", "--true-peak", "-1.5"])
    print("built", final)
