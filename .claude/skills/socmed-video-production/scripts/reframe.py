#!/usr/bin/env python3
"""Reframe a video to a new aspect ratio (default 1080x1920 vertical); audio is stream-copied.

Modes:
  crop      fill the frame and crop; --x-center / --y-center (0..1) choose what stays in frame
  blur_pad  fit the whole picture over a blurred, filled copy of itself
  pad       fit the whole picture with solid bars
A single static crop cannot follow a moving subject: check every shot, and split
or keyframe in Kdenlive when the subject leaves the frame.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path
from project_paths import existing_input, new_output, probe, project_root, require_tools, stream

CODECS = {"libx264": "h264", "libx265": "hevc"}
PRESETS = {"ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("media", type=Path)
    ap.add_argument("--output", type=Path, required=True, help="New .mp4 inside the project (never overwritten)")
    ap.add_argument("--root", type=Path, default=None, help="Project root (default: CLAUDE_PROJECT_DIR, else cwd)")
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1920)
    ap.add_argument("--mode", choices=("crop", "blur_pad", "pad"), default="crop")
    ap.add_argument("--x-center", type=float, default=0.5, help="Crop focus, 0 = left edge, 1 = right edge")
    ap.add_argument("--y-center", type=float, default=0.5, help="Crop focus, 0 = top, 1 = bottom")
    ap.add_argument("--pad-color", default="black", choices=("black", "white", "gray"))
    ap.add_argument("--video-codec", default="libx264", choices=sorted(CODECS))
    ap.add_argument("--crf", type=int, default=20)
    ap.add_argument("--preset", default="medium", choices=sorted(PRESETS))
    args = ap.parse_args()
    w, h = args.width, args.height
    if not (2 <= w <= 8192 and 2 <= h <= 8192 and w % 2 == 0 and h % 2 == 0):
        ap.error("width/height must be even integers between 2 and 8192")
    if not (0 <= args.x_center <= 1 and 0 <= args.y_center <= 1 and 0 <= args.crf <= 51):
        ap.error("--x-center/--y-center must be 0..1 and --crf 0..51")
    try:
        root = project_root(args.root)
        media = existing_input(args.media, root)
        output = new_output(args.output, root, {".mp4"})
        tools = require_tools("ffmpeg", "ffprobe")
    except (ValueError, RuntimeError) as exc:
        ap.error(str(exc))
    meta = probe(tools["ffprobe"], media)
    video = stream(meta, "video")
    if video is None:
        ap.error("input has no video stream")
    has_audio = stream(meta, "audio") is not None
    xc, yc = args.x_center, args.y_center
    if args.mode == "crop":
        graph = (f"[0:v:0]scale={w}:{h}:force_original_aspect_ratio=increase,"
                 f"crop={w}:{h}:(iw-{w})*{xc}:(ih-{h})*{yc},setsar=1,format=yuv420p[v]")
    elif args.mode == "blur_pad":
        graph = (f"[0:v:0]split=2[bg][fg];"
                 f"[bg]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},boxblur=luma_radius=40:luma_power=2,eq=brightness=-0.08[bgb];"
                 f"[fg]scale={w}:{h}:force_original_aspect_ratio=decrease[fgs];"
                 f"[bgb][fgs]overlay=(W-w)/2:(H-h)/2,setsar=1,format=yuv420p[v]")
    else:
        graph = (f"[0:v:0]scale={w}:{h}:force_original_aspect_ratio=decrease,"
                 f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color={args.pad_color},setsar=1,format=yuv420p[v]")
    cmd = [tools["ffmpeg"], "-nostdin", "-hide_banner", "-loglevel", "error", "-i", str(media),
           "-filter_complex", graph, "-map", "[v]", "-c:v", args.video_codec, "-preset", args.preset, "-crf", str(args.crf)]
    cmd += ["-map", "0:a:0", "-c:a", "copy"] if has_audio else ["-an"]
    cmd += ["-movflags", "+faststart", str(output)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=7200, check=False)
    if proc.returncode:
        if output.exists() and not output.is_symlink():
            output.unlink()
        print(f"ERROR: FFmpeg reframe failed:\n{proc.stderr[-3000:]}", file=sys.stderr)
        return 1
    out_video = stream(probe(tools["ffprobe"], output), "video") or {}
    ok = out_video.get("width") == w and out_video.get("height") == h
    print(json.dumps({"output": str(output), "mode": args.mode, "source_size": [video.get("width"), video.get("height")],
                      "output_size": [out_video.get("width"), out_video.get("height")], "size_ok": ok,
                      "audio": "stream-copied" if has_audio else "none",
                      "note": "Watch the whole render: check that faces, text and action stay inside the frame and platform safe zones."}, indent=2))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
