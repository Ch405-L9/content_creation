"""Burn shot-list text cards, tags and dialogue captions onto a picture cut (authored text only)."""
import json, subprocess, sys, textwrap
from pathlib import Path
root, shotlist, src, out, txtdir = (Path(sys.argv[1]), *map(Path, sys.argv[2:6]))
src, out, txtdir = root/src, root/out, root/txtdir
if out.exists(): sys.exit(f'refusing to overwrite {out}')
txtdir.mkdir(parents=True, exist_ok=True)
d = json.loads((root/shotlist).read_text())
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
captions = {5: "Look at us now.\nWe run the town.", 9: "Check the motion.", 14: "I'm a queen on the track,\nnever gonna back down.",
            17: "Yeah, I came to take the crown,\nwatch me break it down.", 18: "Feel the heat,\nremember my name.", 20: "…never slowing down,\nwe be wanting more."}
items = []  # (name, text, t0, t1, style)
for s in d['shots']:
    a, b = s['t']
    if s.get('text'):
        style = 'reveal' if s['n'] == 19 else ('end' if s['n'] == 20 else 'card')
        if style == 'reveal':
            l1, l2 = s['text'].split('\n')
            items += [(f"{s['n']:02d}a", l1, a + 0.2, b, 'reveal'), (f"{s['n']:02d}b", l2, a + 1.3, b, 'reveal_big')]
        else:
            items.append((f"{s['n']:02d}", s['text'], a, b, style))
    if s.get('tag'):
        items.append((f"{s['n']:02d}tag", s['tag'], a, b, 'tag'))
    if s['n'] in captions:
        items.append((f"{s['n']:02d}cap", captions[s['n']], a, b, 'caption'))
STY = {  # fontsize, wrap width, y expression, colour, box opacity
    'card': (58, 24, 'h*0.24', '0xFFD600', 0.85), 'end': (96, 14, 'h*0.30', '0xFFD600', 0.85),
    'tag': (28, 48, 'h*0.135', 'white', 0.55), 'caption': (46, 34, 'h*0.66', 'white', 0.70),
    'reveal': (50, 32, 'h*0.40', 'white', 0.0), 'reveal_big': (72, 18, 'h*0.47', '0xFFD600', 0.0)}
chains = []
for name, text, t0, t1, style in items:
    fs, width, y, col, box = STY[style]
    lines = [w for part in text.split('\n') for w in (textwrap.wrap(part, width) or [''])]
    if style == 'tag' and t0 > 30: fs, y, lines = 32, 'h*0.17', [w for w in textwrap.wrap(text, 46)]
    for k, line in enumerate(lines):
        f = txtdir / f'{name}_{k}.txt'; f.write_text(line)
        yy = f"({y})+{k}*{int(fs*1.32)}"
        boxpart = f":box=1:boxcolor=black@{box}:boxborderw={int(fs*0.28)}" if box else ""
        chains.append(f"drawtext=fontfile={BOLD}:textfile={f}:expansion=none:fontsize={fs}:fontcolor={col}{boxpart}"
                      f":x=(w-text_w)/2:y={yy}:enable='between(t,{t0:.3f},{t1:.3f})'")
graph = "fps=24," + ",".join(chains) + ",format=yuv420p"
gfile = txtdir / 'filtergraph.txt'; gfile.write_text(graph)
cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-n', '-i', str(src), '-filter_script:v', str(gfile), '-c:v', 'libx264', '-crf', '18',
       '-preset', 'medium', '-r', '24', '-c:a', 'copy', '-movflags', '+faststart', str(out)]
subprocess.run(cmd, check=True)
print(out, len(items), 'overlays')
