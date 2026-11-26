"""Render storyboard sheets (one per act) from edit/shotlist JSON."""
import json, subprocess, sys, io, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
root = Path(sys.argv[1]); shotlist = root / sys.argv[2]; outdir = root / sys.argv[3]
outdir.mkdir(parents=True, exist_ok=True)
data = json.loads(shotlist.read_text())
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; R = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
fb, fr, fs, ft = ImageFont.truetype(F, 22), ImageFont.truetype(R, 17), ImageFont.truetype(F, 17), ImageFont.truetype(F, 34)
TW, TH = 270, 480
def frame(shot):
    if shot['src'] == 'BLACK':
        im = Image.new('RGB', (TW, TH), 'black')
    else:
        mid = shot['in'] + (shot['t'][1] - shot['t'][0]) / 2
        png = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-ss', f'{mid:.3f}', '-i', str(root / 'assets' / shot['src']),
                              '-frames:v', '1', '-vf', f'scale={TW}:{TH}:force_original_aspect_ratio=increase,crop={TW}:{TH}', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                             capture_output=True, check=True).stdout
        im = Image.open(io.BytesIO(png)).convert('RGB')
    if shot['text']:  # preview the on-screen text placement (centre-upper safe zone)
        d = ImageDraw.Draw(im); y = TH * 0.30
        for line in [w for part in shot['text'].split('\n') for w in textwrap.wrap(part, 24)]:
            w = d.textlength(line, font=fs); d.rectangle([(TW - w) / 2 - 6, y - 3, (TW + w) / 2 + 6, y + 21], fill=(0, 0, 0))
            d.text(((TW - w) / 2, y), line, font=fs, fill=(255, 214, 0)); y += 26
    return im
cols = 4
for act in data['acts']:
    shots = [s for s in data['shots'] if s['act'] == act['id']]
    rows = (len(shots) + cols - 1) // cols
    cw, ch = TW + 40, TH + 190
    sheet = Image.new('RGB', (cols * cw + 40, rows * ch + 110), (18, 18, 20)); d = ImageDraw.Draw(sheet)
    d.text((40, 22), data['title'], font=fb, fill=(170, 170, 170)); d.text((40, 52), f"ACT {act['id']}: {act['name']}  ·  {act['span'][0]:.1f}–{act['span'][1]:.1f}s", font=ft, fill='white')
    for k, s in enumerate(shots):
        x, y = 40 + (k % cols) * cw, 100 + (k // cols) * ch
        sheet.paste(frame(s), (x, y)); d.rectangle([x, y, x + TW, y + TH], outline=(80, 80, 80))
        d.text((x, y + TH + 8), f"#{s['n']:02d}   {s['t'][0]:.1f}–{s['t'][1]:.1f}s  ({s['t'][1]-s['t'][0]:.1f}s)", font=fb, fill=(255, 214, 0))
        ty = y + TH + 40
        for line in textwrap.wrap(s['beat'], 30)[:4]:
            d.text((x, ty), line, font=fr, fill='white'); ty += 21
        for line in textwrap.wrap('♪ ' + s['audio'], 32)[:2]:
            d.text((x, ty + 4), line, font=fr, fill=(140, 200, 255)); ty += 21
    sheet.save(outdir / f"storyboard_act{act['id']}.png")
    print(outdir / f"storyboard_act{act['id']}.png")
