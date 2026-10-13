#!/bin/bash
# gd47_pie.sh <tag> <python dict for builtins.GD47P> : PIE check job + move the screenshots into data/shots_<tag>/
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD47_ChaosCloth_20261014; TAG=$1
GD47_PRE="builtins.GD47P = $2" bash $N/tools/gd47_run.sh $N/jobs/pie_cloth.py pie-$TAG 1500
mkdir -p $N/data/shots_$TAG; n=0; for f in Saved/Screenshots/WindowsEditor/gd47_${TAG}_*.png; do [ -f "$f" ] && mv -f "$f" $N/data/shots_$TAG/ && n=$((n+1)); done; echo "shots moved: $n"
