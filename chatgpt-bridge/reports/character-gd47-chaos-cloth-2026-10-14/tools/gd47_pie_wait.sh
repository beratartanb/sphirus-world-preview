#!/bin/bash
# gd47_pie_wait.sh <tag> <GD47P dict> : run the PIE job, wait for data/pie_<tag>.json, summarise, move shots
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD47_ChaosCloth_20261014; T=$1
rm -f $N/data/pie_$T.json; bash $N/tools/gd47_pie.sh $T "$2" >/dev/null
for i in $(seq 1 400); do [ -f $N/data/pie_$T.json ] && break; sleep 2; done; sleep 3
"/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" -c "
import json; d=json.load(open('$N/data/pie_$T.json')); print('error', d.get('error')); print(d['events'])
for s in d['shots']: print(' ', s)
for k,v in (d.get('cloth') or {}).items():
  for n,e in v.items(): print(k, n, e and {x: e.get(x) for x in ('visible','attach','leader','is_simulation_enabled','materials')})"
mkdir -p $N/data/shots_$T; rm -f $N/data/shots_$T/*; mv -f Saved/Screenshots/WindowsEditor/gd47_${T}_*.png $N/data/shots_$T/ 2>/dev/null; echo "shots: $(ls $N/data/shots_$T | wc -l)"
