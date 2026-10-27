#!/bin/bash
# run232_b7.sh : V2.32 B7 (same editor, after B6_DONE): sprint / jog posture owner isolation (trunk lean 29 deg at sprint, head sway 14 cm):
# production vs PBI off / curve lean off / settle+terrain body off / all runtime IK + warping off (one layer at a time).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "B6_DONE\|L2_FAILED" $O; do sleep 30; done
export WARM=0 MEMPROBE=1
J=""; for v in o oPBI oCLD oSET oSCR oRAW; do for s in cam32_s90 cam32_j90; do J="$J $s:$v"; done; done
ab b7 "$J" $D/vars232.sh
echo "B7_DONE $(date +%T)" >> $O
