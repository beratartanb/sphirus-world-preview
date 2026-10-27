#!/bin/bash
# run232_ld.sh : V2.32 loaded-family dry runs (no save, no PIE): B_F 32 bins (default choreography) + F_B P21/P29/P30 variants.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; R=Tools/SHME_V2_20261014/run_v2.sh; export LR_LOG=shmv232_b1b.log
for j in ldbf_dry ldfb_s16 ldfb_s28 ldfb_r42 ldfb_t30; do bash $R $D/req/$j.py $j 900 > $D/$j.out 2>&1; echo "LD $j $(grep -a -c 'G231L ' $D/$j.out)" >> $D/chain.out; done
echo "LD_DONE $(date +%T)" >> $D/chain.out
