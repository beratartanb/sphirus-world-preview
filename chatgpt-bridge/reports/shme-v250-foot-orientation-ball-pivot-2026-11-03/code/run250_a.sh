#!/bin/bash
# run250_a.sh : V2.50 chain A = stage isolation of the 135/180 turning-start entry toe dig at 60 FPS fixed step (same request, same selection)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V250_20261103; source $D/lib250.sh
relaunch a60 60; WARM=1 ab a60 "j45_sl2:o j45_sl2:oOW j45_sl2:oSW j45_sl2:oLI j45_sl2:oFP0 jstart:o jstart:oOW"
echo TA250_DONE >> $O
