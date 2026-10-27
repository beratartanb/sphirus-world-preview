#!/bin/bash
# run232_b5.sh : V2.32 B5 (same editor, after B4_DONE): camera round 2 (c2 / c2b) on the camera set + mouse flick + real route.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "B4_DONE" $O; do sleep 30; done
export WARM=0 MEMPROBE=1
J=""; for v in c2 c2b; do for s in cam32_w45 cam32_j90 cam32_s90 cam32_s90l cam32_s180 cam32_brk2 cam32_wallturn cam32_look cam32_idlelook cam32_analog cam32_chain cam_corr s29_cam; do J="$J $s:$v"; done; done
J="$J s29_cam:o map_r1:c2 ins_ws:c2 legs_slope_sprint:c2 ter_drop_walk:c2"
ab b5 "$J" $D/vars232.sh
echo "B5_DONE $(date +%T)" >> $O
