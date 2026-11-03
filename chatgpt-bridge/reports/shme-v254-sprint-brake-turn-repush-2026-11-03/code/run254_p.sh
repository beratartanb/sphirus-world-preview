#!/bin/bash
# run254_p.sh : V2.54 production verification after promote254 (turn + cut)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V254_20261104; O=$D/run254_p.out; source $D/lib254.sh
relaunch p60 60
WARM=1 ab p60 "s54_revR:o s54_revL:o s54_r90:o s54_l90:o s54_tap:o s54_mid:o wstart:o taps:o gait:o w43_idle:o"
relaunch preal real
WARM=1 ab preal "s54_revR:o s54_r90:o s54_tap:o"
echo TP254_DONE >> $O
