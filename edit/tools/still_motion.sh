#!/usr/bin/env bash
# Turn a 9:16 still into a slow push-in "slow-mo" clip with handheld drift and strobe/flash pops.
# Usage: edit/tools/still_motion.sh IN.png OUT.mp4 DURATION ZOOM_END X_DRIFT_PX_PER_FRAME
# Never overwrites (ffmpeg -n). 1080x1920, 24 fps, H.264 CRF 16, no audio.
set -euo pipefail
in="$1"; out="$2"; dur="${3:-3}"; zoom="${4:-0.15}"; xdrift="${5:-0}"
frames=$(python3 -c "print(round(float('$dur')*24))")
ffmpeg -nostdin -v error -n -loop 1 -framerate 24 -i "$in" -t "$dur" -vf "\
scale=1512:2709:flags=lanczos,\
zoompan=z='1.0+${zoom}*on/${frames}':x='iw/2-(iw/zoom/2)+${xdrift}*on':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=24,\
scale=1188:2112,crop=1080:1920:'54+12*sin(t*1.3)':'96+18*sin(t*1.1)',\
eq=brightness='0.10*gt(sin(2*PI*t*1.9+0.5),0.93)+0.07*gt(sin(2*PI*t*3.1),0.96)':eval=frame,\
setsar=1,format=yuv420p" -c:v libx264 -crf 16 -preset slow -r 24 "$out"
