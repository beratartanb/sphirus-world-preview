#!/bin/bash
# run254_a.sh : V2.54 chain A (measure only) = reproduce the high-speed direction changes in production at 60 fixed
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V254_20261104; O=$D/run254_a.out; source $D/lib254.sh
relaunch a60 60
WARM=1 ab a60 "s54_rev:o j54_rev:o w54_rev:o s54_r90:o s54_l90:o s54_r135:o j54_r90:o j54_r135:o s54_tap:o s54_mid:o s54_lr:o"
echo TA254_DONE >> $O
