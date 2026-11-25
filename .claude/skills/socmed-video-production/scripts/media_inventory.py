#!/usr/bin/env python3
"""Inventory media under a project root with ffprobe metadata; no media is changed."""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi", ".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".opus", ".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path.cwd(), help='Project root')
    ap.add_argument('--output', type=Path, help='JSON report path (default: ROOT/logs/media_inventory.json)')
    args = ap.parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        ap.error(f'root is not a directory: {root}')
    ffprobe = shutil.which('ffprobe')
    if not ffprobe:
        ap.error('ffprobe is not installed or not in PATH')
    files = []
    for path in sorted(root.rglob('*')):
        if path.is_symlink() or not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        if any(part in {'.git', '.venv', 'node_modules'} for part in path.relative_to(root).parts):
            continue
        rel = path.relative_to(root).as_posix()
        record = {'path': rel, 'bytes': path.stat().st_size}
        try:
            proc = subprocess.run([ffprobe, '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)], capture_output=True, text=True, timeout=90, check=False)
            if proc.returncode == 0:
                meta = json.loads(proc.stdout)
                fmt = meta.get('format', {})
                record['format'] = {k: fmt.get(k) for k in ('format_name', 'duration', 'bit_rate', 'tags') if k in fmt}
                record['streams'] = [{k: st.get(k) for k in ('index', 'codec_type', 'codec_name', 'width', 'height', 'avg_frame_rate', 'r_frame_rate', 'sample_rate', 'channels', 'channel_layout', 'pix_fmt', 'color_space', 'color_transfer', 'color_primaries', 'duration') if k in st} for st in meta.get('streams', [])]
            else:
                record['error'] = proc.stderr.strip()[-2000:]
        except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as exc:
            record['error'] = str(exc)
        files.append(record)
    output = args.output.expanduser().resolve() if args.output else root / 'logs' / 'media_inventory.json'
    if not output.is_relative_to(root):
        ap.error('output must remain under the project root')
    output.parent.mkdir(parents=True, exist_ok=True)
    report = {'generated_utc': datetime.now(timezone.utc).isoformat(), 'project_root': str(root), 'ffprobe': ffprobe, 'items': len(files), 'media': files}
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({'output': str(output), 'items': len(files), 'probe_errors': sum('error' in item for item in files)}, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
