#!/usr/bin/env bash
# Finish a generated clip for delivery: 2K vertical (1440x2560), light sharpen + grain, NO audio, NO text overlays.
# Removes the CapCut corner AI badge (delogo, 720x1280 source coords).
# Usage: edit/tools/finish_2k_silent.sh IN OUT [MAX_SECONDS]
# Never overwrites (ffmpeg -n). H.264 High, CRF 14, yuv420p, faststart.
set -euo pipefail
in="$1"; out="$2"; max="${3:-8.0}"
ffmpeg -nostdin -v error -n -i "$in" -t "$max" -an -vf "\
delogo=x=12:y=12:w=48:h=38,\
scale=1440:2560:flags=lanczos,\
unsharp=5:5:0.6:5:5:0.0,\
eq=contrast=1.04:saturation=0.97,\
noise=alls=6:allf=t+u,\
format=yuv420p" -c:v libx264 -profile:v high -crf 14 -preset slow -r 24 -movflags +faststart "$out"
ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate:format=duration -of compact "$out"
