#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out; source $D/lib230.sh
echo "T11 start $(date +%T)" >> $O
export WARM=1 MEMPROBE=1
J=""; for s in ter_drop_walk ter_drop_jog ter_step2 ter_bump_jog map_r1 legs_slope_sprint; do J="$J $s:lr2 $s:sp1 $s:sp2"; done
ab t11 "$J" $D/vars230.sh
echo "T11_DONE $(date +%T)" >> $O
