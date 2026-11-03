#!/bin/bash
# run254_b.sh : V2.54 chain B = fresh launch after the turn-around content + runtime install, 60 fixed: phase-gated sprint reversals
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V254_20261104; O=$D/run254_b.out; source $D/lib254.sh
relaunch b60 60
WARM=1 ab b60 "s54_revR:o s54_revR:rv s54_revL:o s54_revL:rv s54_rev:rv s54_revR:rvdb"
echo TB254_DONE >> $O
