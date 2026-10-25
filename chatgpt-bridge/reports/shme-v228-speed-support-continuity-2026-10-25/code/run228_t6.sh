#!/bin/bash
# run228_t6.sh : after the snap-fix build: terrain lengthen 18 (te4b) + identity inspection re-check (ins5) + production references, fixed 30.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V228_20261025; export O=$D/chain.out; source $D/lib228.sh
echo "T6 start $(date +%T)" >> $O; export WARM=1
relaunch t6 30
ab t6 "ter_drop_jog:te4b ter_drop_walk:te4b map_r1:te4b ter_bump_jog:te4b ins_ws2:ins5 ins_ws:ins5 map_r1:o" $D/vars228.sh
echo "T6_DONE $(date +%T)" >> $O
