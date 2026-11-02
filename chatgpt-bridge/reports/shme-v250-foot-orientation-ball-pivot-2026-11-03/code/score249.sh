#!/bin/bash
# score249.sh <label-regex> : markdown rows | label | first start clip in 8.5-13 s | pivot249 worst translation | contact231 worst | pops |
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; C=Saved/Codex/SHME_V250_20261103/chain.out
for L in $(ls Saved/Codex/SHME_V1_20260925/LTP/ | grep -E "$1" | sed 's/\.ltp$//'); do
  pv=$("$PY" Tools/SHME_V249_20261102/pivot249.py $L | tail -1 | sed -E 's/.*worst translation ([0-9.]+) cm \(([lr]) [0-9.]+ (.*)\)/\1 (\3)/')
  ct=$("$PY" Tools/SHME_V231_20261026/contact231.py $L 2>&1 | grep -a worst | sed -E 's/.*SLIP\/DRAG +([0-9.]+) cm at ([0-9.]+) [lr] ([^|]*)\|.*/\1 @\2 (\3)/')
  pp=$(grep -a "^$L |" $C | tail -1 | sed -E 's/.*pops >25 m\/s2: ([0-9]+) \(worst ([0-9]+)\).*/\1 \/ \2/')
  echo "| $L | $pv | $ct | $pp |"
done
