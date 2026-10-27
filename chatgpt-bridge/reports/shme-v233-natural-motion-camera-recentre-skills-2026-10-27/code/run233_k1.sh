#!/bin/bash
# run233_k1.sh : V2.33 camera auto recentre stage 1 (same editor camC): o vs rec on the recentre cases + counter-cases (fixed 30, 1 rep:
# fixed step is deterministic; repeats for the stable candidate).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; export O=$D/chain.out; source $D/lib233.sh
echo "K1 start $(date +%T)" >> $O
export WARM=1 MEMPROBE=1
J=""; for s in cam33_wturn cam33_wturn_w cam33_jturn cam33_sturn cam33_back cam33_look cam33_idlelook cam33_pad c30_calm ins_ws cam_corr; do J="$J $s:o $s:rec"; done
ab k1 "$J" $D/vars233.sh
echo "K1_DONE $(date +%T)" >> $O
