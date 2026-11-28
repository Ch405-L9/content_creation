#!/usr/bin/env bash
# build_v2.sh — next shot v2 (new camera-language prompts; Arena + Omni sources). Parts -> luma match -> A/B deliverables.
set -euo pipefail
cd "$(dirname "$0")"
R=../../assets/proxies/refs/next_shot
AR=../../assets/originals/arena_gen/next_shot
OM=../../assets/originals/aistudio_gen/next_shot
P=parts_v2; mkdir -p $P/graded ../../review/next_shot

# part  source                           start dur  frames  ref-seg
./retime.sh $AR/arena_k1_buildup_A.mp4     $P/p1_buildup.mp4   0 3.0 35
./retime.sh $AR/arena_k2b_speedB_Medit_A.mp4 $P/p2b_speed.mp4  0 4.0 54   # user pick: speed B, door M removed via Arena edit
./retime.sh $OM/omni_k3_shiftdown_v2.mp4   $P/p3_shiftdown.mp4 0 3.2 44
./retime.sh $OM/omni_k4_victory_v3.mp4     $P/p4_victory.mp4   0 2.5 34
./retime.sh $OM/omni_k5_calm_v2.mp4        $P/p5_calm_raw.mp4  0 1.5 20
# calm: 1 black frame first, like the reference segment
ffmpeg -v error -y -i $P/p5_calm_raw.mp4 -filter_complex \
 "[0:v]tpad=start=1:start_mode=add:color=black,trim=end_frame=21[v];[0:a]adelay=33|33,atrim=end=0.7,apad,atrim=end=0.7[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 14 -pix_fmt yuv420p -c:a aac -b:a 192k $P/p5_calm.mp4
cp parts/graded/p2a_flash.mp4 $P/graded/p2a_flash.mp4   # 2-frame flash (unchanged, already graded)

# luma match each part to its reference segment
ymean() { ffmpeg -v error -i "$1" -vf "signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-" -f null - \
  | awk -F= '/YAVG/{s+=$2;n++}END{print s/n}'; }
for pair in p1_buildup:seg1 p2b_speed:seg2 p3_shiftdown:seg3 p4_victory:seg4 p5_calm:seg5; do
  p=${pair%%:*}; s=${pair##*:}
  k=$(python3 -c "print(round(min(1.6,max(0.6,$(ymean $R/$s.mp4)/$(ymean $P/$p.mp4))),3))")
  echo "$p k=$k"
  ffmpeg -v error -y -i $P/$p.mp4 -vf "lutyuv=y='clip(val*$k,16,235)'" -c:v libx264 -crf 14 -pix_fmt yuv420p -c:a copy $P/graded/$p.mp4
done

lay="scale=1080:608:flags=lanczos,setsar=1,pad=1080:1920:0:754:black,fps=30"
mk() { out=$1; n=$2; shift 2; ins=(); fc=""; i=0
  for p in "$@"; do ins+=(-i $P/graded/$p.mp4); fc+="[$i:v][$i:a]"; i=$((i+1)); done
  ffmpeg -v error -y "${ins[@]}" -filter_complex "${fc}concat=n=$i:v=1:a=1[v0][a0];[v0]$lay[v];[a0]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]" \
   -map "[v]" -map "[a]" -frames:v $n -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$out"; }
mk ../../review/next_shot/next_shot_A_buildup_speed_v2.mp4 91 p1_buildup p2a_flash p2b_speed
mk ../../review/next_shot/next_shot_B_shiftdown_victory_calm_v2.mp4 99 p3_shiftdown p4_victory p5_calm
