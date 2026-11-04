#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; O=$D/run255_d.out; source $D/lib255.sh
CAP_START=4.6 CAP_SECS=3.2 ab dcap "s54_revR:t1S" $D/vars255.sh
echo TD255_DONE >> $O
