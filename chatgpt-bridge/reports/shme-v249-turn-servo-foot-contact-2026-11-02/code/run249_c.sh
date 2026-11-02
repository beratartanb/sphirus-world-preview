#!/bin/bash
# run249_c.sh : V2.49 chain C = 60 FPS servo A/B (skipped in chain B by the guard) after chain B
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; source $D/lib249.sh
until grep -q TB249_DONE $O; do sleep 20; done
relaunch c60 60; WARM=1 ab c60 "j45_sl2:rm j45_sl2:o jstart:rm"
echo TC249_DONE >> $O
