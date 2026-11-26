#!/usr/bin/env python3
"""Render a safe sequential hard-cut draft from a validated timeline JSON."""
from __future__ import annotations
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from timeline_utils import load_timeline


def ffprobe_json(ffprobe: str, source: Path) -> dict:
    proc = subprocess.run([ffprobe, '-v', 'error', '-show_streams', '-of', 'json', str(source)], capture_output=True, text=True, timeout=90, check=False)
    if proc.returncode:
        raise RuntimeError(f'ffprobe failed for {source}: {proc.stderr.strip()[-1200:]}')
    return json.loads(proc.stdout)


def write_log(log: Path, text: str) -> None:
    """Write the render log without following a planted symlink."""
    fd = os.open(log, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o644)
    with os.fdopen(fd, 'w', encoding='utf-8') as fh:
        fh.write(text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('timeline', type=Path)
    ap.add_argument('--root', type=Path, default=None, help='Project root (default: CLAUDE_PROJECT_DIR, else two levels above the timeline)')
    ap.add_argument('--output', required=True, type=Path, help='New MP4 path inside project root; existing outputs are never overwritten')
    args = ap.parse_args()
    timeline_path = args.timeline.expanduser().resolve()
    data, errors, root = load_timeline(timeline_path, args.root)
    if errors or data is None or root is None:
        print(json.dumps({'valid': False, 'errors': errors}, indent=2), file=sys.stderr)
        return 2
    output = args.output.expanduser().resolve()
    if not output.is_relative_to(root):
        ap.error('output must remain under the project root')
    if output.exists() or output.is_symlink():
        ap.error(f'refusing to overwrite existing output: {output}')
    if output.suffix.lower() != '.mp4':
        ap.error('this draft renderer writes .mp4 only')
    ffmpeg, ffprobe = shutil.which('ffmpeg'), shutil.which('ffprobe')
    if not ffmpeg or not ffprobe:
        ap.error('ffmpeg and ffprobe must be installed and available in PATH')
    p = data['profile']; width = p['width']; height = p['height']; fps = f"{p['fps_num']}/{p.get('fps_den', 1)}"
    fit = p.get('fit_mode', 'contain')
    if fit == 'contain':
        scale = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black"
    else:
        scale = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}"
    video_codec = p.get('video_codec', 'libx264'); audio_codec = p.get('audio_codec', 'aac')
    if video_codec not in {'libx264', 'libx265', 'libvpx-vp9', 'libaom-av1'}:
        ap.error('video codec is not allowed')
    # Limit this packaged renderer to containers/codecs that support the MP4 intermediate contract.
    if video_codec not in {'libx264', 'libx265'} or audio_codec != 'aac':
        ap.error('MP4 draft renderer currently supports libx264/libx265 video and AAC audio only')
    output.parent.mkdir(parents=True, exist_ok=True)
    errors_log = output.with_suffix(output.suffix + '.render.log')
    if errors_log.is_symlink() or errors_log.exists() or not errors_log.parent.resolve().is_relative_to(root):
        ap.error(f'refusing to reuse existing or external render log: {errors_log}')
    try:
        with tempfile.TemporaryDirectory(prefix='.roughcut-', dir=str(output.parent)) as work_name:
            work = Path(work_name)
            segments: list[Path] = []
            for index, clip in enumerate(data['clips']):
                src = (root / clip['source']).resolve() if not Path(clip['source']).is_absolute() else Path(clip['source']).resolve()
                probe = ffprobe_json(ffprobe, src)
                has_audio = any(s.get('codec_type') == 'audio' for s in probe.get('streams', []))
                start, end = float(clip['in_sec']), float(clip['out_sec'])
                duration = end - start
                seg = work / f'segment_{index:04d}.mkv'  # PCM audio: no per-segment AAC priming/padding drift
                cmd = [ffmpeg, '-nostdin', '-hide_banner', '-loglevel', 'warning', '-y', '-i', str(src)]
                if not has_audio:
                    cmd += ['-f', 'lavfi', '-t', f'{duration:.6f}', '-i', 'anullsrc=r=48000:cl=stereo']
                v = f"[0:v:0]trim=start={start:.6f}:end={end:.6f},setpts=PTS-STARTPTS,fps={fps},{scale},setsar=1,format=yuv420p[v]"
                if has_audio:
                    a = f"[0:a:0]atrim=start={start:.6f}:end={end:.6f},asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,apad=whole_dur={duration:.6f}[a]"
                else:
                    a = f"[1:a:0]atrim=duration={duration:.6f},asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a]"
                cmd += ['-filter_complex', v + ';' + a, '-map', '[v]', '-map', '[a]', '-t', f'{duration:.6f}', '-c:v', video_codec, '-preset', p.get('preset', 'medium'), '-crf', str(p.get('crf', 23)), '-c:a', 'pcm_s16le', '-ar', '48000', '-ac', '2', str(seg)]
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600, check=False)
                if proc.returncode:
                    raise RuntimeError(f'FFmpeg failed for clip {index + 1} ({clip["source"]}):\n{proc.stderr[-5000:]}')
                segments.append(seg)
            concat = work / 'concat.txt'
            concat.write_text(''.join("file '" + str(s).replace("'", "'\\''") + "'\n" for s in segments), encoding='utf-8')
            cmd = [ffmpeg, '-nostdin', '-hide_banner', '-loglevel', 'warning', '-f', 'concat', '-safe', '0', '-i', str(concat), '-c:v', 'copy', '-c:a', audio_codec, '-b:a', '192k', '-movflags', '+faststart', str(output)]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=7200, check=False)
            if proc.returncode:
                raise RuntimeError(f'FFmpeg concat failed:\n{proc.stderr[-5000:]}')
            check = subprocess.run([ffprobe, '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(output)], capture_output=True, text=True, timeout=90, check=False)
            if check.returncode:
                raise RuntimeError(f'FFprobe could not validate rendered output: {check.stderr[-2000:]}')
            meta = json.loads(check.stdout)
            if not any(s.get('codec_type') == 'video' for s in meta.get('streams', [])):
                raise RuntimeError('Rendered output has no video stream')
            if not any(s.get('codec_type') == 'audio' for s in meta.get('streams', [])):
                raise RuntimeError('Rendered output has no audio stream')
    except Exception as exc:
        write_log(errors_log, str(exc) + '\n')
        if output.exists():
            output.unlink()
        print(f'ERROR: {exc}\nRender log: {errors_log}', file=sys.stderr)
        return 1
    write_log(errors_log, 'Render completed. This rough cut still requires visual and audio review.\n')
    print(json.dumps({'output': str(output), 'duration_seconds': meta.get('format', {}).get('duration'), 'video': next((s for s in meta.get('streams', []) if s.get('codec_type') == 'video'), {}), 'audio': next((s for s in meta.get('streams', []) if s.get('codec_type') == 'audio'), {}), 'render_log': str(errors_log), 'note': 'Review the full export; this tool performs sequential hard cuts only.'}, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
