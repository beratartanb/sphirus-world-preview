#!/bin/bash
# rec.sh <tag> <plan name>... : house-map recordings from the shore start (no map load; unique labels mr1_<plan>_<tag>), hip analysis + slide
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; TAG=$1; shift; HK="$(cat Saved/UE59Work/r5/hk3_line.txt)"
for p in "$@"; do L=mr1_${p}_$TAG; [ -f Saved/Codex/Grip_20261106/rec/$L.json ] && { echo "EXISTS $L"; continue; }
  DFPS=${HZ:-60.0} bash Tools/UE59_20261118/run2.sh $L ${POS:-1400 2980 79 42} "$(cat Saved/UE59Work/mr1/p_$p.txt)" "$HK" > /dev/null 2>&1
  "$PY" Tools/UE59_20261124/an_hip.py $L Saved/UE59Work/mr1/p_$p.txt 2>&1 | cut -c1-250; "$PY" Tools/UE59_20261122/an_slide3.py $L Saved/UE59Work/mr1/p_$p.txt 8 2>&1 | grep TOTAL | sed 's/curve:.*ground:/ground:/' | cut -c1-110; done
