"""v004 finish: grade + sound-design cue sheet (from shot list), then title cards (no captions)."""
import json, subprocess, sys, textwrap
from pathlib import Path
root = Path(sys.argv[1]); d = json.loads((root/'edit/shotlist_v004.json').read_text()); T = {s['n']: s['t'] for s in d['shots']}
work = root/'edit/finish_v008'; work.mkdir(exist_ok=True)
pic, graded, final = root/'review/grantrun_finecut_v004_picture.mp4', root/'review/grantrun_finecut_v008_graded.mp4', root/'review/grantrun_finecut_v008_text.mp4'
Z, Y = 'assets/originals/sfx_zr1x/', 'assets/audio/sfx_synth/'
# (file, start_s, gain, trim_s or None)
cues = [(Y+'impact_boom.wav', 0.0, 0.8, None), (Z+'sounds_high_rpm-gain.mp4', 0.0, 0.35, None),
        (Y+'whoosh_fast.wav', T[2][0]-0.25, 1.6, None),
        (Y+'tape_stop.wav', T[4][0]+1.32, 0.7, None),
        (Y+'sub_drop.wav', T[6][0], 0.7, None), (Z+'sounds_cockpit_110mph_downshift.mp4', T[6][0], 0.5, 2.2),
        (Z+'sounds_passing-by.mp4', T[8][0]+0.3, 0.5, None), (Y+'whoosh_fast.wav', T[8][0]-0.2, 1.4, None),
        (Z+'sounds_passing-by-1.mp4', T[10][0], 0.45, None),
        (Y+'impact_boom.wav', T[11][0], 0.45, None), (Y+'whoosh_fast.wav', T[12][0]-0.2, 1.3, None),
        (Y+'riser_2s6.wav', T[16][0]-2.6, 0.55, None), (Y+'sub_drop.wav', T[16][0], 0.85, None),
        (Z+'sounds_idle_rumble.mp4', T[16][0]+0.5, 0.35, 1.6),
        (Y+'drone_low_3s.wav', T[18][0], 0.6, None),
        (Y+'heartbeat_3s6.wav', T[19][0], 0.75, None), (Y+'impact_boom.wav', T[19][0]+1.3, 0.9, None),
        (Z+'sounds_high_rpm-gain.mp4', T[19][0]+1.3, 0.45, 1.0), (Y+'whoosh_fast.wav', T[20][0]-0.2, 1.2, None)]
look = ("fps=24,scale=1134:2016:flags=lanczos,crop=1080:1920:x='27+20*sin(t*0.9)':y='48+28*sin(t*0.7+1)',"
        "eq=contrast=1.08:saturation=0.85:brightness=-0.02,curves=master='0/0 0.12/0.04 0.5/0.47 1/1',noise=alls=12:allf=t+u,vignette=PI/5,format=yuv420p")
q0, q1 = T[16][0], T[16][0] + 0.6
g = [f"[0:v]{look}[v]", f"[0:a]volume=enable='between(t,{q0:.3f},{q1:.3f})':volume=0,volume=enable='between(t,{q1:.3f},{T[16][1]:.3f})':volume=0.35[bed]"]
inputs = ['-i', str(pic)]; labels = ['[bed]']
for i, (f, st, gain, trim) in enumerate(cues, 1):
    inputs += ['-i', str(root/f)]; ms = int(round(st*1000))
    tr = f"atrim=0:{trim},afade=t=out:st={trim-0.3}:d=0.3," if trim else ""
    g.append(f"[{i}:a]{tr}aresample=48000,aformat=channel_layouts=stereo,volume={gain},adelay={ms}|{ms}[c{i}]"); labels.append(f'[c{i}]')
g.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,alimiter=limit=0.89,apad=whole_dur=40,atrim=0:40[a]")
(work/'graph.txt').write_text(';\n'.join(g))
(work/'cue_sheet.json').write_text(json.dumps([{'file': f, 'start': round(s, 3), 'gain': gn, 'trim': t} for f, s, gn, t in cues], indent=2))
if not graded.exists():
    # Picture and sound rendered separately, then muxed: a single a/v pass dropped the bed's last 0.5 s.
    vid, mix = work/'picture_graded.mp4', work/'mix.wav'
    (work/'graph_audio.txt').write_text(';\n'.join(g[1:]))
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-n', '-i', str(pic), '-vf', look, '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium',
                    '-r', '24', '-frames:v', '960', str(vid)], check=True)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-n', *inputs, '-filter_complex_script', str(work/'graph_audio.txt'), '-map', '[a]',
                    '-c:a', 'pcm_s24le', str(mix)], check=True)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-n', '-i', str(vid), '-i', str(mix), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', str(graded)], check=True)
# ---- title cards (no captions) ----
F = '/usr/share/fonts/opentype/urw-base35/NimbusSansNarrow-Bold.otf'
SH = ':shadowcolor=black@0.85:shadowx=4:shadowy=4'
draws, k = [], 0
def line(text, t0, t1, size, color, y, fade=0.12):
    global k
    f = work/f'txt_{k:02d}.txt'; f.write_text(text); k += 1
    alpha = f"if(lt(t,{t0}+{fade}),(t-{t0})/{fade},if(gt(t,{t1}-{fade}),({t1}-t)/{fade},1))"
    draws.append(f"drawtext=fontfile={F}:textfile={f}:expansion=none:fontsize={size}:fontcolor={color}{SH}:x=(w-text_w)/2:y={y}"
                 f":alpha='{alpha}':enable='between(t,{t0:.3f},{t1:.3f})'")
s = {x['n']: x for x in d['shots']}
a, b = T[1]; line('ATL  ·  2:47 AM', a, b + 0.8, 64, 'white', 'h*0.20'); line(s[1]['tag'], a, b + 0.8, 30, 'white@0.85', 'h*0.135')
for n in (4, 5):
    name, *rest = s[n]['text'].split('\n'); a, b = T[n]
    line(name, a + 0.1, b, 92, '0xFFD600', 'h*0.20')
    for j, r in enumerate(textwrap.wrap(' '.join(rest), 26)): line(r, a + 0.25, b, 54, 'white', f'h*0.20+110+{j}*66')
a, b = T[16]; line('They lost him at the Connector.', a + 0.6, b, 60, 'white', 'h*0.22')
a, b = T[19]; l1, l2 = s[19]['text'].split('\n')
line(l1, a + 0.25, b, 58, 'white', 'h*0.40', 0.3)
for j, r in enumerate(textwrap.wrap(l2, 16)): line(r, a + 1.3, b, 96, '0xFFD600', f'h*0.46+{j}*112', 0.05)
a, b = T[20]; line('EP. 2  →', a + 0.15, b, 140, '0xFFD600', 'h*0.66')
for j, r in enumerate(textwrap.wrap(s[20]['tag'], 50)): line(r, a + 0.15, b, 32, 'white@0.9', f'h*0.17+{j}*40')
(work/'titles.txt').write_text(','.join(draws))
if final.exists(): sys.exit(f'refusing to overwrite {final}')
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', str(graded), '-filter_script:v', str(work/'titles.txt'), '-c:v', 'libx264', '-crf', '16',
                '-preset', 'slow', '-r', '24', '-c:a', 'copy', '-movflags', '+faststart', str(final)], check=True)
print('ok', final)
