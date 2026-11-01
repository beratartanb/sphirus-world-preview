#!/bin/bash
# media242.sh <name> <labelA> <labelB> <nameA> <nameB> [scale 0.5] : side-by-side real-speed MJPEG AVI (30 fps fixed-step captures, same frame =
# same game time) of two harness captures -> Saved/Codex/SHME_V242_20261101/vid/<name>_realtime.avi (parts <= 90 MB via avi_parts.py)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
N=$1; A=$2; B=$3; NA=$4; NB=$5; SCL=${6:-0.5}; V=Saved/Codex/SHME_V138_20260927/Video; O=Saved/Codex/SHME_V242_20261101/vid; TMP=$O/tri_$N; mkdir -p $O; rm -rf "${TMP:?}"
PY="/c/Program Files/Blender Foundation/Blender 5.2/5.2/python/bin/python.exe"
mkdir -p $TMP/A/frames $TMP/B/frames; cp $V/$A/*.jpg $TMP/A/frames/; cp $V/$B/*.jpg $TMP/B/frames/
powershell.exe -NoProfile -ExecutionPolicy Bypass -File Tools/AIToolingEval_20261031/triptych.ps1 -Base "$(cygpath -w $TMP)" -Clip frames -Out "$(cygpath -w $TMP/out)" -Scale $SCL -Sets "A,B" -Names "$NA,$NB" | tail -1
"$PY" Tools/ExteriorWorld_XR2_20261031/avi_parts.py $TMP/out $O/${N}_realtime 30 1 90 | tail -3
rm -rf "${TMP:?}/A" "${TMP:?}/B"; ls -la $O | grep "$N"
