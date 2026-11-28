#!/usr/bin/env bash
# finish.sh CAPCUT_CLIP CLIP_NAME START_S OUT  -> delogo CapCut badge, 1080x1920@24, original YUCK audio for that 5 s window
set -euo pipefail
in=$1; clip=$2; ss=$3; out=$4
ffmpeg -v error -y -i "$in" -ss "$ss" -t 5 -i "assets/originals/quarterfinals/YUCK_clips/$clip.mp4" -filter_complex \
 "[0:v]delogo=x=14:y=12:w=36:h=36,trim=end=5,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1,fps=24[v];[1:a]atrim=end=5,asetpts=PTS-STARTPTS[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$out"
