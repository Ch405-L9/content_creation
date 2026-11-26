#!/usr/bin/env python3
"""Two-pass EBU R128 loudness normalization with FFmpeg loudnorm; video is stream-copied.

Default target is -14 LUFS integrated / -1 dBTP, a common starting point for
social feeds. Platforms differ and change: confirm the target for each delivery.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from project_paths import existing_input, new_output, probe, project_root, require_tools, stream

SUFFIXES = {".mp4", ".mov", ".mkv", ".m4a", ".wav"}


def measure(ffmpeg: str, media: Path, i: float, tp: float, lra: float) -> dict[str, str]:
    cmd = [ffmpeg, "-nostdin", "-hide_banner", "-i", str(media), "-map", "0:a:0",
           "-af", f"loudnorm=I={i}:TP={tp}:LRA={lra}:print_format=json", "-f", "null", "-"]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600, check=False)
    if proc.returncode:
        raise RuntimeError(f"loudness analysis failed: {proc.stderr[-2000:]}")
    found = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", proc.stderr)
    if not found:
        raise RuntimeError("could not read loudnorm measurement from FFmpeg output")
    data = json.loads(found[-1])
    for key in ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset"):
        value = float(data[key])  # rejects anything non-numeric before it reaches a filter string
        if value != value or abs(value) == float("inf"):
            raise RuntimeError(f"unusable loudness measurement {key}={data[key]} (silent audio?)")
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("media", type=Path)
    ap.add_argument("--output", type=Path, required=True, help="New file inside the project (never overwritten)")
    ap.add_argument("--root", type=Path, default=None, help="Project root (default: CLAUDE_PROJECT_DIR, else cwd)")
    ap.add_argument("--target-lufs", type=float, default=-14.0)
    ap.add_argument("--true-peak", type=float, default=-1.0)
    ap.add_argument("--lra", type=float, default=11.0)
    ap.add_argument("--audio-bitrate", default="192k", choices=("128k", "160k", "192k", "256k", "320k"))
    args = ap.parse_args()
    if not (-40 <= args.target_lufs <= -5 and -9 <= args.true_peak <= 0 and 1 <= args.lra <= 50):
        ap.error("targets out of range: LUFS -40..-5, true peak -9..0, LRA 1..50")
    try:
        root = project_root(args.root)
        media = existing_input(args.media, root)
        output = new_output(args.output, root, SUFFIXES)
        tools = require_tools("ffmpeg", "ffprobe")
    except (ValueError, RuntimeError) as exc:
        ap.error(str(exc))
    ffmpeg, ffprobe = tools["ffmpeg"], tools["ffprobe"]
    meta = probe(ffprobe, media)
    if stream(meta, "audio") is None:
        ap.error("input has no audio stream")
    has_video = stream(meta, "video") is not None and output.suffix.lower() in {".mp4", ".mov", ".mkv"}
    i, tp, lra = args.target_lufs, args.true_peak, args.lra
    before = measure(ffmpeg, media, i, tp, lra)
    af = (f"loudnorm=I={i}:TP={tp}:LRA={lra}:measured_I={float(before['input_i'])}:measured_TP={float(before['input_tp'])}"
          f":measured_LRA={float(before['input_lra'])}:measured_thresh={float(before['input_thresh'])}"
          f":offset={float(before['target_offset'])}:linear=true:print_format=summary,aresample=48000")
    cmd = [ffmpeg, "-nostdin", "-hide_banner", "-loglevel", "error", "-i", str(media)]
    cmd += ["-map", "0:v:0", "-c:v", "copy"] if has_video else ["-vn"]
    cmd += ["-map", "0:a:0", "-af", af]
    cmd += ["-c:a", "pcm_s16le"] if output.suffix.lower() == ".wav" else ["-c:a", "aac", "-b:a", args.audio_bitrate]
    if output.suffix.lower() in {".mp4", ".mov", ".m4a"}:
        cmd += ["-movflags", "+faststart"]
    cmd.append(str(output))
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=7200, check=False)
    if proc.returncode:
        if output.exists() and not output.is_symlink():
            output.unlink()
        print(f"ERROR: FFmpeg normalization failed:\n{proc.stderr[-3000:]}", file=sys.stderr)
        return 1
    after = measure(ffmpeg, output, i, tp, lra)
    off_target = abs(float(after["input_i"]) - i) > 1.0 or float(after["input_tp"]) > tp + 0.5
    print(json.dumps({"output": str(output), "target": {"integrated_lufs": i, "true_peak_dbtp": tp, "lra": lra},
                      "before": {"integrated_lufs": float(before["input_i"]), "true_peak_dbtp": float(before["input_tp"]), "lra": float(before["input_lra"])},
                      "after": {"integrated_lufs": float(after["input_i"]), "true_peak_dbtp": float(after["input_tp"]), "lra": float(after["input_lra"])},
                      "video": "stream-copied" if has_video else "none",
                      "warning": "result is more than 1 LU off target or above the peak limit; listen and review" if off_target else None,
                      "note": "Meters are not ears: listen to dialogue clarity and music balance before approval."}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
