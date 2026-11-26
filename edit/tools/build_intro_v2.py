#!/usr/bin/env python3
"""Build the Mustang Met Gala intro (206 frames) and splice it over v008's opening -> grantrun v009.

Picture and sound are rendered separately and muxed (a single a/v pass dropped audio tails before).
Run from the project root:  python3 edit/tools/build_intro_v2.py
Outputs (never overwritten): review/mustang_intro_v2.mp4, review/grantrun_v009_premaster.mp4
"""
import subprocess, sys
from pathlib import Path

ROOT = Path.cwd()
W = ROOT / "edit/finish_v009"; W.mkdir(parents=True, exist_ok=True)
P, Y, Z = "assets/proxies/", "assets/audio/sfx_synth/", "assets/originals/sfx_zr1x/"
FPS = 24
# (clip, start_frame_in_clip, frames)
SHOTS = [(P + "pendant_shot1_motion_v1.mp4", 14, 34),
         (P + "gordon_shot2_motion_v1.mp4", 7, 43),
         (P + "trixie_shot3_motion_v2.mp4", 7, 43),
         (P + "car_shot4_motion_mach5_v1.mp4", 10, 48),
         (P + "both_shot5_motion_v2.mp4", 10, 38)]
INTRO_FRAMES = sum(s[2] for s in SHOTS)          # 206 = start of v008 shot 7
SPLICE = INTRO_FRAMES / FPS                       # 8.5833 s
cuts, t = [], 0.0
for _, _, n in SHOTS:
    cuts.append(t); t += n / FPS
T = lambda i: (cuts[i], cuts[i] + SHOTS[i][2] / FPS)

def run(args):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-n", *args], check=True)

def need(path):
    p = ROOT / path
    if p.exists():
        sys.exit(f"refusing to overwrite {p}")
    return str(p)

LOOK = ("scale=1134:2016:flags=lanczos,crop=1080:1920:x='27+20*sin(t*0.9)':y='48+28*sin(t*0.7+1)',"
        "eq=contrast=1.08:saturation=0.88:brightness=-0.02,curves=master='0/0 0.12/0.04 0.5/0.47 1/1',"
        "noise=alls=12:allf=t+u,vignette=PI/5")

# ---- titles (same typography as the v008 finish) ----
F = "/usr/share/fonts/opentype/urw-base35/NimbusSansNarrow-Bold.otf"
SH = ":shadowcolor=black@0.85:shadowx=4:shadowy=4"
draws, k = [], 0
def line(text, t0, t1, size, color, y, fade=0.12):
    global k
    f = W / f"title_{k:02d}.txt"; f.write_text(text); k += 1
    a = f"if(lt(t,{t0}+{fade}),(t-{t0})/{fade},if(gt(t,{t1}-{fade}),({t1}-t)/{fade},1))"
    draws.append(f"drawtext=fontfile={F}:textfile={f}:expansion=none:fontsize={size}:fontcolor={color}{SH}"
                 f":x=(w-text_w)/2:y={y}:alpha='{a}':enable='between(t,{t0:.3f},{t1:.3f})'")
a, b = T(0); line("ATL  ·  2:47 AM", a, b, 64, "white", "h*0.20")
line("UNOFFICIAL FAN TRIBUTE · AI-GENERATED · FICTION", a, b + 0.4, 30, "white@0.85", "h*0.135")
a, b = T(1); line("GORDON GRANT, 23", a + 0.1, b, 92, "0xFFD600", "h*0.16")
line("Relationship with authority: no.", a + 0.25, b, 54, "white", "h*0.16+110")
a, b = T(2); line('MICHELLE "TRIXIE"', a + 0.1, b, 92, "0xFFD600", "h*0.16")
line("Navigator. Brains. Zero patience.", a + 0.25, b, 54, "white", "h*0.16+110")

# ---- intro picture ----
ins, parts = [], []
for i, (clip, s0, n) in enumerate(SHOTS):
    ins += ["-i", str(ROOT / clip)]
    parts.append(f"[{i}:v]trim=start_frame={s0}:end_frame={s0 + n},setpts=PTS-STARTPTS,fps={FPS},setsar=1[v{i}]")
graph = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(len(SHOTS))) + \
        f"concat=n={len(SHOTS)}:v=1:a=0,{LOOK},{','.join(draws)},format=yuv420p[v]"
(W / "intro_picture_graph.txt").write_text(graph)
intro_pic = need("edit/finish_v009/intro_picture.mp4")
run([*ins, "-filter_complex_script", str(W / "intro_picture_graph.txt"), "-map", "[v]", "-frames:v", str(INTRO_FRAMES),
     "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-r", str(FPS), intro_pic])

# ---- intro sound bed (cue times follow the cuts) ----
cues = [(Y + "sub_drop.wav", 0.0, 0.9, None), (Y + "impact_boom.wav", 0.0, 0.6, None),
        (Y + "drone_low_3s.wav", 0.0, 0.45, None), (Y + "drone_low_3s.wav", 3.0, 0.4, None),
        (Y + "whoosh_fast.wav", cuts[1] - 0.25, 1.4, None), (Y + "whoosh_fast.wav", cuts[2] - 0.25, 1.4, None),
        (Y + "whoosh_fast.wav", cuts[3] - 0.25, 1.3, None), (Y + "impact_boom.wav", cuts[3], 0.9, None),
        (Z + "sounds_high_rpm-gain.mp4", cuts[3] + 0.05, 0.55, None), (Y + "heartbeat_3s6.wav", cuts[4], 0.5, 1.6),
        (Y + "whoosh_fast.wav", SPLICE - 0.3, 1.2, None)]
ains, lab, g = [], [], []
for i, (f, st, gain, trim) in enumerate(cues):
    ains += ["-i", str(ROOT / f)]
    ms = int(round(st * 1000)); tr = f"atrim=0:{trim}," if trim else ""
    g.append(f"[{i}:a]{tr}aresample=48000,aformat=channel_layouts=stereo,volume={gain},adelay={ms}|{ms}[c{i}]"); lab.append(f"[c{i}]")
g.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0:duration=longest,alimiter=limit=0.89,"
         f"apad=whole_dur={SPLICE},atrim=0:{SPLICE}[a]")
(W / "intro_audio_graph.txt").write_text(";\n".join(g))
intro_wav = need("edit/finish_v009/intro_mix.wav")
run([*ains, "-filter_complex_script", str(W / "intro_audio_graph.txt"), "-map", "[a]", "-c:a", "pcm_s24le", intro_wav])

intro_mp4 = need("review/mustang_intro_v2.mp4")
run(["-i", intro_pic, "-i", intro_wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
     "-movflags", "+faststart", intro_mp4])

# ---- splice: intro + v008 (pre-loudnorm text version) from frame 206 to the end ----
v008 = str(ROOT / "review/grantrun_finecut_v008_text.mp4")
tail_pic = need("edit/finish_v009/tail_picture.mp4")
run(["-i", v008, "-vf", f"trim=start_frame={INTRO_FRAMES},setpts=PTS-STARTPTS", "-an", "-c:v", "libx264", "-crf", "16",
     "-preset", "slow", "-r", str(FPS), tail_pic])
tail_wav = need("edit/finish_v009/tail.wav")
run(["-i", v008, "-vn", "-af", f"atrim=start={SPLICE},asetpts=PTS-STARTPTS", "-c:a", "pcm_s24le", tail_wav])
full_pic = need("edit/finish_v009/full_picture.mp4")
(W / "concat.txt").write_text(f"file '{intro_pic}'\nfile '{tail_pic}'\n")
run(["-f", "concat", "-safe", "0", "-i", str(W / "concat.txt"), "-c", "copy", full_pic])
full_wav = need("edit/finish_v009/full_mix.wav")
run(["-i", intro_wav, "-i", tail_wav, "-filter_complex",
     f"[0:a]afade=t=out:st={SPLICE-0.01:.4f}:d=0.01[x];[1:a]afade=t=in:d=0.01[y];[x][y]concat=n=2:v=0:a=1,apad=whole_dur=40,atrim=0:40[a]", "-map", "[a]", "-c:a", "pcm_s24le", full_wav])
out = need("review/grantrun_v009_premaster.mp4")
run(["-i", full_pic, "-i", full_wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
     "-t", "40", "-movflags", "+faststart", out])
print("intro", intro_mp4, "splice at", round(SPLICE, 4), "s ->", out)
