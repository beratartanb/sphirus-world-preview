#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib230.sh
echo "T8 start $(date +%T)" >> $O
bash $R $D/req/db230L_write.py db230L 1800 > $D/db230L.out 2>&1; grep -a "RDB226\|Traceback" $D/db230L.out | cut -c1-500 >> $O
bash $R $D/req/curves230L_write.py curves230L 1800 > $D/curves230L.out 2>&1; grep -a "CURVE\|Traceback" $D/curves230L.out | cut -c1-300 >> $O
bash $R $D/req/loadroute_save.py loadroute 900 > $D/loadroute.out 2>&1; grep -a "LOADROUTE230 {\|Traceback" $D/loadroute.out | cut -c1-600 >> $O
grep -aq '"ok": true' $D/loadroute.out || { echo "T8_STOP loadroute" >> $O; exit 1; }
export WARM=1 MEMPROBE=1
J=""; for s in e29_chain e29_load e29_recov chain_sscut e29_rest s29_ws j24_ph0 j24_dbl s29_dbl; do J="$J $s:lrL"; done
ab t8 "$J" $D/vars230.sh
echo "T8_DONE $(date +%T)" >> $O
