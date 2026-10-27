#!/bin/bash
# run232_b12.sh : V2.32 B12 (same editor, after B11_DONE): E walk plant unplant angle through the ABP CDO (pb90 / pb120) vs o.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "B11_DONE" $O; do sleep 30; done
export WARM=0 MEMPROBE=1
J=""; for v in o pb90 pb120; do for s in c29_combo a29_angb wdiag cam32_w45 k_walkback c30_calm; do J="$J $s:$v"; done; done
ab b12 "$J" $D/vars232.sh
echo "B12_DONE $(date +%T)" >> $O
