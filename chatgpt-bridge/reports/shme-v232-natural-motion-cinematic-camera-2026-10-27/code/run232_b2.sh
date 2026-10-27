#!/bin/bash
# run232_b2.sh : V2.32 B2 (same editor as B1, after B1_DONE): tick-order candidate tk vs production o on the motion defect set (fixed 30).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "B1_DONE" $O; do sleep 30; done
export WARM=0 MEMPROBE=1
J="c30_calm:oSET c30_calm:oFP c30_calm:oRAW wstart:oSET wstart:oFP j30_slow:oFP"; for v in o tk; do for s in e29_chain e29_load e31_s2_4750 e31_s2_4900 s29_swl12 j30_slow j30_rel_3200 j30_rel_3450 j24_ph0 c29_combo c30_calm a29_angb wstart jstart d_sprint chain_sprint cam32_s180; do J="$J $s:$v"; done; done
ab b2 "$J" $D/vars232.sh
echo "B2_DONE $(date +%T)" >> $O
