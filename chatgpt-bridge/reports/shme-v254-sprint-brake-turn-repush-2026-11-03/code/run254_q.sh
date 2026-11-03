#!/bin/bash
# run254_q.sh : V2.54 production: 135 / jog / walk reversal coverage
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V254_20261104; O=$D/run254_q.out; source $D/lib254.sh
until grep -q "TP254_DONE\|RELAUNCH_FAILED" $D/run254_p.out 2>/dev/null; do sleep 15; done
relaunch q60 60
WARM=1 ab q60 "s54_r135:o j54_r135:o w54_rev:o j54_rev:o"
CAP_START=4.8 CAP_SECS=2.8 ab qcap "s54_r135:prodS" $D/vars254_cap.sh
echo TQ254_DONE >> $O
