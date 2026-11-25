#!/usr/bin/env python3
"""Probe a rendered file and optionally compare dimensions/fps to a profile JSON."""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('media', type=Path)
    ap.add_argument('--profile', type=Path, help='production.json or platform_profiles.json')
    ap.add_argument('--profile-id', help='Key inside platform_profiles.json profiles object')
    args = ap.parse_args()
    media = args.media.expanduser().resolve()
    if not media.is_file() or media.stat().st_size == 0:
        ap.error(f'media is missing or empty: {media}')
    ffprobe = shutil.which('ffprobe')
    if not ffprobe:
        ap.error('ffprobe is not installed or not in PATH')
    proc = subprocess.run([ffprobe, '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(media)], capture_output=True, text=True, timeout=90, check=False)
    if proc.returncode:
        print(proc.stderr, file=sys.stderr); return 2
    data = json.loads(proc.stdout)
    streams = data.get('streams', [])
    video = next((x for x in streams if x.get('codec_type') == 'video'), None)
    audio = next((x for x in streams if x.get('codec_type') == 'audio'), None)
    errors, warnings = [], []
    if video is None: errors.append('no video stream')
    if audio is None: warnings.append('no audio stream')
    expected = None
    if args.profile:
        cfg = json.loads(args.profile.expanduser().resolve().read_text(encoding='utf-8'))
        if 'profiles' in cfg:
            profiles = cfg['profiles']
            key = args.profile_id or next(iter(profiles), None)
            expected = profiles.get(key) if key else None
            if expected is None: ap.error('profile-id was not found')
        elif 'deliverables' in cfg:
            expected = cfg['deliverables'][0] if cfg['deliverables'] else None
        else:
            expected = cfg.get('profile', cfg)
    if expected and video:
        for key in ('width', 'height'):
            if key in expected and video.get(key) != expected[key]: errors.append(f'{key} mismatch: expected {expected[key]}, got {video.get(key)}')
        fpsn, fpsd = expected.get('fps_num'), expected.get('fps_den', 1)
        actual_fps = video.get('avg_frame_rate') or video.get('r_frame_rate')
        if fpsn and actual_fps and actual_fps != '0/0':
            try:
                if abs(float(Fraction(actual_fps)) - float(Fraction(int(fpsn), int(fpsd)))) > 0.02:
                    errors.append(f'frame-rate mismatch: expected {fpsn}/{fpsd}, got {actual_fps}')
            except (ValueError, ZeroDivisionError): warnings.append(f'could not parse frame rate {actual_fps}')
        codec_aliases = {'libx264': 'h264', 'libx265': 'hevc', 'libvpx-vp9': 'vp9', 'libaom-av1': 'av1'}
        if expected.get('video_codec'):
            wanted = codec_aliases.get(expected['video_codec'], expected['video_codec'])
            if video.get('codec_name') != wanted: errors.append(f'video codec mismatch: expected {wanted}, got {video.get("codec_name")}')
        if expected.get('pixel_format') and video.get('pix_fmt') != expected['pixel_format']:
            errors.append(f'pixel format mismatch: expected {expected["pixel_format"]}, got {video.get("pix_fmt")}')
        if expected.get('audio_codec'):
            if audio is None: errors.append('expected an audio stream but none is present')
            else:
                wanted_audio = codec_aliases.get(expected['audio_codec'], expected['audio_codec'])
                if audio.get('codec_name') != wanted_audio: errors.append(f'audio codec mismatch: expected {wanted_audio}, got {audio.get("codec_name")}')
        actual_duration = float(data.get('format', {}).get('duration', 0) or 0)
        max_duration = expected.get('max_duration_seconds')
        if isinstance(max_duration, (int, float)) and actual_duration > float(max_duration) + 0.05:
            errors.append(f'maximum duration exceeded: allowed {max_duration:.3f}s, got {actual_duration:.3f}s')
        target_duration = expected.get('target_duration_seconds')
        if isinstance(target_duration, (int, float)) and abs(actual_duration - float(target_duration)) > float(expected.get('duration_tolerance_seconds', 1.0)):
            warnings.append(f'duration differs from target {float(target_duration):.3f}s: got {actual_duration:.3f}s')
    report = {'valid': not errors, 'file': str(media), 'bytes': media.stat().st_size, 'duration_seconds': data.get('format', {}).get('duration'), 'video': video, 'audio': audio, 'errors': errors, 'warnings': warnings, 'profile_checked': expected}
    print(json.dumps(report, indent=2))
    return 0 if not errors else 2

if __name__ == '__main__':
    raise SystemExit(main())
