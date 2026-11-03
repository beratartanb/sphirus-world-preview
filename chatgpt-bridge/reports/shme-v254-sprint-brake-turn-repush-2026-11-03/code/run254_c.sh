#!/bin/bash
# run254_c.sh : V2.54 chain C = route hold + 4 phase clips
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V254_20261104; O=$D/run254_c.out; source $D/lib254.sh
relaunch c60 60
WARM=1 ab c60 "s54_revR:o s54_revR:rv s54_revL:o s54_revL:rv s54_revR:rv:2 s54_revL:rv:2"
echo TC254_DONE >> $O
