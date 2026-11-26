#!/usr/bin/env python3
"""Build the Mustang exit-chase cutscene (and the interior shift insert) from the Seedance clips.

Each shot: (source, in_s, out_s, speed, frames). Picture and sound are rendered separately, muxed, then
loudness-normalized to -14 LUFS / -1.5 dBTP. The clips' own generated audio (rain/road) is the ambience bed.
Run from the project root:  python3 edit/tools/build_cutscene.py [--only exit_chase interior_shift full] [--version v1]
Outputs (never overwritten): review/cutscene/<name>_<version>.mp4
"""
import argparse, subprocess, sys
from pathlib import Path

ROOT = Path.cwd(); OUT = ROOT / "review/cutscene"; WORK = ROOT / "edit/finish_cutscene"
OUT.mkdir(parents=True, exist_ok=True); WORK.mkdir(parents=True, exist_ok=True)
G, Y, Z = "assets/originals/capcut_gen/", "assets/audio/sfx_synth/", "assets/originals/sfx_zr1x/"
FPS = 24

# (source, in, out, speed, frames, ambience_gain)
A = ("assets/proxies/chase_A_flyby_seedance_v1_mach5.mp4", 2.20, 3.90, 1.3, 31, 0.55)
PB = "assets/proxies/chase_B_tracking_seedance_v1_plateblur.mp4"   # generated plate text blurred (blur_track.py)
# Source 3.45-4.0 s slides back up the car (reads as reversing) then jumps ahead: cut it out, hard cut to the pull-away.
BS = [(PB, 0.20, 3.45, 1.6, 48, 0.45), (PB, 4.02, 5.04, 1.0, 24, 0.45)]
C1 = (G + "chase_C1_footwell_seedance_v1.mp4", 0.0, 0.66, 1.0, 16, 0.35)  # left foot down / right lifts; glitch at 0.67 s
# v2: regenerated keyframe with left-hand-drive geometry (driver left seat, right hand on console shifter)
C2 = (G + "chase_C2_shifter_seedance_v2.mp4", 0.50, 1.33, 1.0, 20, 0.35)  # lever pulled back ~0.85 s source
SNAP = (0.85 - 0.50) / 1.0                                                    # snap time inside the C2 shot
# Phone-operator push-in on Gordon (low angle -> tight face, dutch roll, AF hunt): edit/phone_specs/c3_phone_zoom_v1.json
C3 = ("assets/proxies/chase_C3_phone_zoom_v1.mp4", 0.0, 2.5, 1.0, 60, 0.4)

# Sound cues are (file, start_s_in_sequence, gain, source_offset_s). Times follow the shot cuts.
SEQUENCES = {
    "exit_chase": ([A, *BS], lambda c: [
        (Y + "whoosh_fast.wav", 0.45, 1.2, 0.0),
        (Z + "sounds_passing-by.mp4", 0.0, 1.0, 0.95),        # pass-by peak (1.8 s) lands on the visual pass (~0.85 s)
        (Z + "sounds_passing-by-1.mp4", 0.55, 0.6, 0.0),
        (Y + "impact_boom.wav", c[1], 0.5, 0.0),
        (Z + "sounds_cockpit_0-110mph_14s.mp4", c[1], 0.55, 8.0),  # sustained high-speed engine under the tracking shot
        (Y + "whoosh_fast.wav", c[2] - 0.12, 0.8, 0.0),
        (Z + "sounds_high_rpm-gain.mp4", c[2] - 0.05, 0.8, 0.0),   # pull-away
        (Y + "siren_wail_far_6s.wav", 0.0, 0.22, 0.6),
    ]),
    "interior_shift": ([C1, C2], lambda c: [
        (Z + "sounds_cockpit_110mph_downshift.mp4", 0.0, 0.9, 1.4),
        (Y + "whoosh_fast.wav", c[1] - 0.15, 0.6, 0.0),
        (Y + "impact_boom.wav", c[1] + SNAP, 0.35, 0.0),            # gear goes in
        (Y + "siren_wail_far_6s.wav", 0.0, 0.12, 2.0),
    ]),
    "phone_zoom": ([C3], lambda c: [
        (Z + "sounds_cockpit_0-110mph_14s.mp4", 0.0, 0.6, 9.0),       # engine at speed, heard from inside
        (Y + "whoosh_fast.wav", 0.35, 0.7, 0.0),                    # the snap zoom
        (Y + "heartbeat_3s6.wav", 1.0, 0.5, 0.0),                   # intensity once focus locks
        (Y + "siren_wail_far_6s.wav", 0.0, 0.12, 3.0),
    ]),
    # Option: interior insert cut between the fly-by and the tracking shot.
    "full_with_interior": ([A, C1, C2, *BS], lambda c: [
        (Y + "whoosh_fast.wav", 0.45, 1.2, 0.0),
        (Z + "sounds_passing-by.mp4", 0.0, 1.0, 0.95),
        (Z + "sounds_passing-by-1.mp4", 0.55, 0.6, 0.0),
        (Z + "sounds_cockpit_110mph_downshift.mp4", c[1], 0.85, 1.4),
        (Y + "impact_boom.wav", c[2] + SNAP, 0.35, 0.0),
        (Y + "whoosh_fast.wav", c[3] - 0.15, 0.9, 0.0),
        (Y + "impact_boom.wav", c[3], 0.45, 0.0),
        (Z + "sounds_cockpit_0-110mph_14s.mp4", c[3], 0.55, 8.0),
        (Y + "whoosh_fast.wav", c[4] - 0.12, 0.8, 0.0),
        (Z + "sounds_high_rpm-gain.mp4", c[4] - 0.05, 0.8, 0.0),
        (Y + "siren_wail_far_6s.wav", 0.0, 0.2, 0.0),
    ]),
}

LOOK = ("scale=1188:2112:flags=lanczos,crop=1080:1920:54:96,"          # 1.65x up; the crop also drops the corner AI badge
        "eq=contrast=1.06:saturation=0.88:brightness=0.01,curves=master='0/0 0.06/0.04 0.5/0.53 1/1',"
        "colorbalance=bs=0.04:bm=0.02,noise=alls=10:allf=t+u,vignette=PI/5")
F = "/usr/share/fonts/opentype/urw-base35/NimbusSansNarrow-Bold.otf"
TAG = WORK / "tag.txt"; TAG.write_text("UNOFFICIAL FAN TRIBUTE · AI-GENERATED · FICTION")
TITLE = (f"drawtext=fontfile={F}:textfile={TAG}:expansion=none:fontsize=30:fontcolor=white@0.85"
         ":shadowcolor=black@0.85:shadowx=3:shadowy=3:x=(w-text_w)/2:y=h*0.135")

ap = argparse.ArgumentParser(); ap.add_argument("--only", nargs="*"); ap.add_argument("--version", default="v1")
ARGS = ap.parse_args()

def run(args):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-n", *args], check=True)

def build(name, shots, cue_fn):
    V = ARGS.version
    final = OUT / f"{name}_{V}.mp4"
    if final.exists():
        sys.exit(f"refusing to overwrite {final}")
    missing = [s[0] for s in shots if not (ROOT / s[0]).exists()]
    if missing:
        print(f"skip {name}: missing {missing}"); return
    cuts, t = [], 0.0
    for s in shots:
        cuts.append(t); t += s[4] / FPS
    dur = t; frames = sum(s[4] for s in shots)

    ins, parts = [], []
    for i, (src, a, b, sp, n, _) in enumerate(shots):
        ins += ["-i", str(ROOT / src)]
        parts.append(f"[{i}:v]trim=start={a}:end={b},setpts=(PTS-STARTPTS)/{sp},fps={FPS},trim=end_frame={n},"
                     f"setpts=PTS-STARTPTS,setsar=1[v{i}]")
    graph = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(len(shots))) + \
            f"concat=n={len(shots)}:v=1:a=0,{LOOK},{TITLE},format=yuv420p[v]"
    gfile = WORK / f"{name}_{V}_picture.txt"; gfile.write_text(graph)
    pic = WORK / f"{name}_{V}_picture.mp4"
    run([*ins, "-filter_complex_script", str(gfile), "-map", "[v]", "-frames:v", str(frames),
         "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-r", str(FPS), str(pic)])

    ains, lab, g = [], [], []
    for i, (src, a, b, sp, n, gain) in enumerate(shots):          # generated rain/road bed, retimed with the picture
        ains += ["-i", str(ROOT / src)]; ms = int(round(cuts[i] * 1000))
        g.append(f"[{i}:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,atempo={sp},atrim=0:{n / FPS:.4f},"
                 f"aresample=48000,aformat=channel_layouts=stereo,volume={gain},afade=t=in:d=0.02,"
                 f"adelay={ms}|{ms}[c{i}]"); lab.append(f"[c{i}]")
    for j, (f, st, gain, off) in enumerate(cue_fn(cuts)):
        k = len(shots) + j; ains += ["-i", str(ROOT / f)]; ms = int(round(st * 1000))
        g.append(f"[{k}:a]atrim=start={off},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
                 f"volume={gain},adelay={ms}|{ms}[c{k}]"); lab.append(f"[c{k}]")
    g.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0:duration=longest,alimiter=limit=0.89,"
             f"afade=t=out:st={dur - 0.25:.3f}:d=0.25,apad=whole_dur={dur:.4f},atrim=0:{dur:.4f}[a]")
    afile = WORK / f"{name}_{V}_audio.txt"; afile.write_text(";\n".join(g))
    mix = WORK / f"{name}_{V}_mix.wav"
    run([*ains, "-filter_complex_script", str(afile), "-map", "[a]", "-c:a", "pcm_s24le", str(mix)])

    muxed = WORK / f"{name}_{V}_muxed.mp4"
    run(["-i", str(pic), "-i", str(mix), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
         "-movflags", "+faststart", str(muxed)])
    subprocess.run([sys.executable, str(ROOT / ".claude/skills/socmed-video-production/scripts/normalize_loudness.py"),
                    str(muxed), "--root", str(ROOT), "--output", str(final), "--target-lufs", "-14",
                    "--true-peak", "-1.5"], check=True)
    print("built", final, f"{frames} frames / {dur:.3f}s, cuts at", [round(c, 3) for c in cuts])

for name, (shots, cue_fn) in SEQUENCES.items():
    if ARGS.only and name not in ARGS.only:
        continue
    build(name, shots, cue_fn)
