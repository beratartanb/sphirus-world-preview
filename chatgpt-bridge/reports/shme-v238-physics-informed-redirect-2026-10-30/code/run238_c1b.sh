#!/bin/bash
source Saved/Codex/SHME_V238_20261030/lib238.sh; O=$D/chain.out; MD=$D/checkpoint/manifests
echo "C1B start $(date +%T)" >> $O
SHME_KIND=write SHME_MANIFEST=$MD/yaw1.json bash $R $D/req/yaw1.py yaw1 1800 > $D/last_yaw1.out 2>&1; grep -a -o "YAW238 .*" $D/last_yaw1.out | cut -c1-1200 >> $O
grep -a -q '"ok": true' $D/last_yaw1.out && grep -a -q '"saved": true' $D/last_yaw1.out || { echo "C1B_FAILED yaw" >> $O; exit 1; }
WARM=1 ab c1 "j38_c90r:cut1 j38_c90r:o j38_c90l:cut1"
ab c1 "j38_c90r:cut1:2 j38_c90r:cut1S" $D/vars238_cap.sh
echo "C1B_DONE $(date +%T)" >> $O
