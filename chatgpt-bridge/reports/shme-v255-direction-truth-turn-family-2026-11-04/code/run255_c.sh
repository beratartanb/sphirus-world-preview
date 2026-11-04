#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; O=$D/run255_c.out; source $D/lib255.sh
WARM=1 ab c60 "s54_revR:t1 s54_revL:t1 s54_revR:t1" $D/vars255.sh
echo TC255_DONE >> $O
