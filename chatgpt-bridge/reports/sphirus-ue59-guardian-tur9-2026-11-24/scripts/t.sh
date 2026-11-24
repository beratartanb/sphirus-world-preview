#!/bin/bash
# t.sh <version tag> <hz|var> <plan id>... : record plans from r9/plans with unique labels r9_<plan>_<hz>_<tag>; slide + reversal summary -> r9/res/<label>.txt
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
TAG=$1; M=$2; shift 2; HK="$(cat Saved/UE59Work/r9/hk9_line.txt)"; mkdir -p Saved/UE59Work/r9/res
if [ $M = var ]; then HZ=60.0; X="$HK; builtins.VID_VARDT=(22.0,60.0)"; else HZ=$M.0; X="$HK"; fi
for p in "$@"; do L=r9_${p}_${M}_${TAG}; PL=Saved/UE59Work/r9/plans/$p.txt; O=Saved/UE59Work/r9/res/$L.txt
  [ -f Saved/Codex/Grip_20261106/rec/$L.json ] && { echo "EXISTS $L (labels are never reused)"; continue; }
  DFPS=$HZ bash Tools/UE59_20261120/seqP.sh $L $PL "$X" > /dev/null 2>&1
  { echo "#### $L plan $p hz $M tag $TAG $(date +%H:%M)"; "$PY" Tools/UE59_20261122/an_slide3.py $L $PL 8 2>&1 | cut -c1-200; "$PY" Saved/UE59Work/r9/revsum.py $L 2>&1 | cut -c1-260; } > $O
  grep -E "TOTAL" $O | sed "s/^/$L /" | cut -c1-200; done
