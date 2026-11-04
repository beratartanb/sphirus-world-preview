#!/bin/bash
# make_videos.sh <final_tag> : BEFORE | FINAL side-by-side route videos from the fixed-step MediaCapture frames (same frame = same game time),
# real-speed Motion-JPEG AVI parts (<= 95 MB each, GitHub limit). Route A = house -> shore -> rock shelf -> glade; route B = rear forest link.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
TAG=${1:-final}; D=Saved/Codex/PineForestRedesign_20261104; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
mkdir -p $D/video
for R in A B; do
  SUF=""; [ "$TAG" != final ] && SUF="_$TAG"
  rm -rf "$D/video/trip_${R}${SUF}"
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File Tools/AIToolingEval_20261031/triptych.ps1 -Base "$D/cap" -Clip frames -Out "$D/video/trip_${R}${SUF}" -Scale 0.5 -Sets "walk_before${R},walk_${TAG}${R}" -Names "BEFORE,AFTER (Pine Forest redesign $TAG)" | tail -1
  "$PY" -I Tools/ExteriorWorld_XR2_20261031/avi_parts.py "$D/video/trip_${R}${SUF}" "$D/video/route${R}_before_after${SUF}" 30 2 95 | tail -4
done
ls -la $D/video/*.avi | awk '{print $5, $9}'
