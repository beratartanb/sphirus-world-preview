#!/bin/bash
# run255_a.sh : V2.55 reproduce the wrong-direction report on PRODUCTION (V2.54): seeded key fuzz, 60 fixed, camera still and mouse moving
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; O=$D/run255_a.out; source $D/lib255.sh
relaunch a60 60
WARM=1 ab a60 "fz_sprint_a:o fz_sprint_m:o fz_jog_a:o fz_jog_m:o fz_walk_a:o fz_walk_m:o" Saved/Codex/SHME_V254_20261104/vars254.sh
echo TA255_DONE >> $O
