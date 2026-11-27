#!/usr/bin/env bash
# retime.sh IN OUT START_S SRC_DUR_S TARGET_FRAMES  -> 1280x720@30, exact frame count, audio tempo-matched
set -euo pipefail
in=$1; out=$2; ss=$3; dur=$4; n=$5
tgt=$(python3 -c "print($n/30)")
f=$(python3 -c "print($tgt/$dur)")          # video pts factor
a=$(python3 -c "print($dur/$tgt)")          # audio tempo
atf=$(python3 -c "
a=$a; parts=[]
while a>2.0: parts.append('atempo=2.0'); a/=2.0
parts.append('atempo=%.5f'%a); print(','.join(parts))")
ffmpeg -v error -y -ss $ss -t $dur -i "$in" -filter_complex \
 "[0:v]setpts=(PTS-STARTPTS)*$f,fps=30,scale=1280:720:flags=lanczos,setsar=1,trim=end_frame=$n[v];[0:a]asetpts=PTS-STARTPTS,$atf,atrim=end=$tgt,apad,atrim=end=$tgt,aresample=48000[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 14 -pix_fmt yuv420p -c:a aac -b:a 192k "$out"
echo "$out $(ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 "$out") frames"
