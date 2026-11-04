#!/bin/bash
# run255_b.sh : V2.55 same fuzz on the V2.53 sprint routes (rb) and with the auto recentre off (ocam); source clip dump
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; O=$D/run255_b.out; source $D/lib255.sh
until grep -q "TA255_DONE\|RELAUNCH_FAILED" $D/run255_a.out 2>/dev/null; do sleep 10; done
SHME_KIND=measure bash $R Tools/SHME_V255_20261104/clipdump255.py cd255 900 > $D/data/clipdump.out 2>&1
echo CD_DONE >> $O
ab b60 "fz_sprint_a:rb fz_sprint_m:rb fz_sprint_a:ocam" $D/vars255.sh
echo TB255_DONE >> $O
