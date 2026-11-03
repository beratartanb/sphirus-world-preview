#!/bin/bash
# score250.sh <label-regex> [t0 t1] : | label | selected start clip | PEN l/r cm | PLANT l/r cm | BALL l/r cm | pivot249 cm | contact231 cm | pops/worst |
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; T=Tools/SHME_V252_20261103
for L in $(ls Saved/Codex/SHME_V1_20260925/LTP/ | grep -E "$1" | sed 's/\.ltp$//'); do
  c=$("$PY" $T/contact250.py $L ${2:-0} ${3:-1e9})
  pen=$(echo "$c" | sed -E 's/.*PEN +([0-9.-]+) cm.*/\1/' | tr '\n' '/' | sed 's/\/$//')
  pl=$(echo "$c" | sed -E 's/.*PLANT +([0-9.]+) .*/\1/' | tr '\n' '/' | sed 's/\/$//')
  bl=$(echo "$c" | sed -E 's/.*BALL +([0-9.]+) .*/\1/' | tr '\n' '/' | sed 's/\/$//')
  pv=$("$PY" $T/pivot249.py $L ${2:-0} ${3:-1e9} | tail -1 | sed -E 's/.*worst translation ([0-9.]+) cm \(([lr]) [0-9.]+ (.*)\)/\1 (\3)/')
  ct=$("$PY" Tools/SHME_V231_20261026/contact231.py $L ${2:+--t0 $2} ${3:+--t1 $3} 2>&1 | grep -a worst | sed -E 's/.*SLIP\/DRAG +([0-9.]+) cm.*/\1/')
  pp=$(grep -a "^$L |" Saved/Codex/SHME_V2*/chain.out | tail -1 | sed -E 's/.*pops >25 m\/s2: ([0-9]+) \(worst ([0-9]+)\).*/\1 \/ \2/')
  echo "| $L | PEN $pen | PLANT $pl | BALL $bl | $pv | $ct | $pp |"
done
