#!/bin/bash
# run232_l2.sh : V2.32 L2 (same editor, after B5_DONE): loaded family content - B_F 32 bins (gen231_loaded), F_B P29 re-made (b_short 16),
# V/W curves on every LoadRev clip, both loaded DBs rebuilt (F_B with the production P21 / P30 fallback), warm-up, then B6 tests.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "B5_DONE" $O; do sleep 30; done
for j in ldbf_write ldfb29_write ld_curves ld_db; do bash $R $D/req/$j.py $j 1500 > $D/$j.out 2>&1; echo "L2 $j $(grep -a -o 'G231L {.\{0,80\}\|SPEEDCURVE[0-9]* {.\{0,120\}\|CURVE231 {.\{0,160\}\|RDB226 {.\{0,300\}' $D/$j.out | head -1)" >> $O; grep -aq "Traceback" $D/$j.out && { echo "L2_FAILED $j" >> $O; exit 1; }; done
export WARM=1 MEMPROBE=1
LOG="Saved/Logs/$LR_LOG"
J=""; for v in o ldb ldbtk; do for s in e29_load e29_chain e29_recov e31_s2_4700 e31_s2_4750 e31_s2_4800 e31_s2_4900 j24_ph0; do J="$J $s:$v"; done; done
ab b6 "$J" $D/vars232.sh
echo "B6_DONE $(date +%T)" >> $O
