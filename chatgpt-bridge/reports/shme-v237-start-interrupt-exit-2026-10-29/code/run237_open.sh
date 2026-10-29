#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V237_20261029; export O=$D/chain.out; source $D/lib237.sh
echo "OPEN start $(date +%T) (reason: V2.37 source inspection + candidates, fixed 30)" >> $O
relaunch a1 30
echo "OPEN_DONE $(date +%T)" >> $O
