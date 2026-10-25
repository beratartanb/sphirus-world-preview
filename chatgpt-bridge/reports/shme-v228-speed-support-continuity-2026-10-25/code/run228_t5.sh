#!/bin/bash
# run228_t5.sh : after the component build: terrain candidates (lift ceiling 36, true-edge landing shift) and the inspection identity mode, fixed 30.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V228_20261025; export O=$D/chain.out; source $D/lib228.sh
echo "T5 start $(date +%T)" >> $O; export WARM=1
relaunch t5 30
ab t5 "ter_drop_jog:o ter_drop_jog:tl36 ter_drop_jog:te4 ter_drop_walk:tl36 ter_drop_walk:te4 ter_step2:te4 ter_bump_jog:te4 ter_hill8_jog:te4 map_r1:te4 ins_ws2:ins5 ins_ws:ins5 ins_ws2:o" $D/vars228.sh
echo "T5_DONE $(date +%T)" >> $O
