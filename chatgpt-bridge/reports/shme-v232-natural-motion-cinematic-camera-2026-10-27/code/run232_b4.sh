#!/bin/bash
# run232_b4.sh : V2.32 B4 (same editor, after B3_DONE): E walk plant unplant angle 90 / 120 vs production on the walk direction-change set.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "B3_DONE\|B3_FAILED" $O; do sleep 30; done
export WARM=0 MEMPROBE=1
J=""; for v in o pa90 pa120; do for s in c29_combo a29_angb c30_calm wdiag wstart cam32_w45 k_walkback; do J="$J $s:$v"; done; done
ab b4 "$J" $D/vars232.sh
echo "B4_DONE $(date +%T)" >> $O
