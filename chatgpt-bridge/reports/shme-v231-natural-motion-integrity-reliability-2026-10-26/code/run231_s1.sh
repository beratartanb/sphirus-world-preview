#!/bin/bash
# run231_s1.sh : V2.31 session 1 - fresh editor (fixed 30): production verify (V2.30 expectations, post-cleanup integrity) then idle for interactive jobs.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V231_20261026; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib231.sh
echo "S1 start $(date +%T)" >> $O
relaunch s1 30
bash $R $D/req/verify_p0.py verify_p0 900 > $D/verify_p0.out 2>&1; grep -a "VERIFY230" $D/verify_p0.out | cut -c1-600 >> $O
echo "S1_READY $(date +%T)" >> $O
