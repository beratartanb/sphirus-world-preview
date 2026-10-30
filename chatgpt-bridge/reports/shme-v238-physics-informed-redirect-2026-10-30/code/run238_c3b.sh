#!/bin/bash
source Saved/Codex/SHME_V238_20261030/lib238.sh; O=$D/chain.out; MD=$D/checkpoint/manifests
echo "C3B start $(date +%T)" >> $O
SHME_KIND=write SHME_MANIFEST=$MD/hold1.json bash $R $D/req/hold1.py hold1 1800 > $D/last_hold1.out 2>&1; grep -a -o "HOLD238 .*" $D/last_hold1.out | cut -c1-900 >> $O
grep -a -q '"ok": true' $D/last_hold1.out && grep -a -q '"saved": true' $D/last_hold1.out || { echo "C3B_FAILED hold" >> $O; exit 1; }
WARM=1 ab c3 "j38_c90r:cut1 j38_c90l:cut1 j38_c90r:cut1:2 j38_c90l:cut1:2 j38_c90r:o j38_c90l:o"
ab c3 "j38_c90r:cut1S j38_c90l:cut1S j38_c90r:cut1G" $D/vars238_cap.sh
echo "C3B_DONE $(date +%T)" >> $O
