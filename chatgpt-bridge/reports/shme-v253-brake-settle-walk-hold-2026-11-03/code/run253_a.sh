#!/bin/bash
# run253_a.sh : V2.53 chain A (measure only) = layer isolation at 60 fixed: 180 crop-end pop owner (jstart) and the start-entry stance-foot
# surge (wstart / w42_id)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V253_20261104; O=$D/run253_a.out; source $D/lib253.sh
relaunch a60 60
WARM=1 ab a60 "jstart:o jstart:oST jstart:oSW jstart:oORB jstart:oNI jstart:oDB wstart:o wstart:oSW wstart:oFP0 wstart:oORB w42_id:o w42_id:oSW w42_id:oFP0"
echo TA253_DONE >> $O
