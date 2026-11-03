#!/bin/bash
# ana253.sh <label-regex> : V2.53 per-run summary = contact250 (PEN l/r with ABSOLUTE ball min too), contact231 worst, pops, stance foot
# (stance253: pre-toe slide per start), APA (pelvis t at toe-off), settle (stop settle253)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; T=Tools/SHME_V253_20261104
for L in $(ls Saved/Codex/SHME_V1_20260925/LTP/ | grep -E "$1" | sed 's/\.ltp$//'); do
  s=$(bash $T/score250.sh "^$L[.]ltp" | tail -1)
  pp=$(grep -a "^$L |" Saved/Codex/SHME_V253_20261104/run253_*.out 2>/dev/null | tail -1 | sed -E 's/.*pops >25 m\/s2: ([0-9]+) \(worst ([0-9]+)\).*/\1\/\2/')
  st=$("$PY" $T/stance253.py $L 2>/dev/null | sed -E 's/.*slide pre-toe ([0-9.]+).*pelvis lat [^ ]+ \(toe ([^)]+)\) acc max ([0-9.]+).*/\1|\2|\3/' | tr '\n' ' ')
  ap=$("$PY" $T/apa252.py $L 2>/dev/null | sed -E 's/.*pelvis t ([0-9.]+).*/\1/' | tr '\n' ' ')
  se=$("$PY" $T/settle253.py $L 2>/dev/null | sed -E 's/.*pelvis z dip ([0-9.]+).*trunk fwd ([^ ]+) final.*stop after plant: pelvis ([^ ]+) chest ([^ ]+) head ([^ ]+) shoulder ([^ ]+).*/dip \1 trunk \2 stop p\3 c\4 h\5 s\6/' | tr '\n' ';')
  echo "$s pops $pp"; [ -n "$st" ] && echo "    stance pre-toe ball/heel/yaw, pelvis lat@toe, lat acc: $st"; [ -n "$ap" ] && echo "    APA t: $ap"; [ -n "$se" ] && echo "    settle: $se"
done
