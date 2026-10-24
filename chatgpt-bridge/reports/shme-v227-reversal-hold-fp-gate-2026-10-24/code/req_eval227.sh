#!/bin/bash
# eval227.sh <tag> <scenarios...> : per scenario x variant (rv32 rh rhH rhF): plant225 worst JogRev slip | exitjump227 lines | posture window
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; T5=Tools/SHME_V225_20261023; T7=Tools/SHME_V227_20261024; E=Saved/Codex/SHME_V1_20260925/Evidence
TAG=$1; shift; VARS="${VARS:-rv32 rh rhH rhF}"
w() { [ -f $E/$1.json ] || { echo "-"; return; }; "$PY" $T5/plant225.py $1 2>/dev/null | grep -o "worst net *[0-9.]*" | grep -o "[0-9.]*$"; }
printf "%-8s" scen; for v in $VARS; do printf " %6s" $v; done; echo "   (worst planted-foot slip while a JogRev clip is selected, cm)"
for s in "$@"; do printf "%-8s" $s; for v in $VARS; do printf " %6s" "$(w v227${TAG}_j24_${s}_${v}_r1)"; done; echo; done
echo; for s in "$@"; do for v in $VARS; do [ -f $E/v227${TAG}_j24_${s}_${v}_r1.json ] && "$PY" $T7/exitjump227.py v227${TAG}_j24_${s}_${v}_r1; done; done
