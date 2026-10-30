#!/bin/bash
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
echo "F start $(date +%T)" >> $O
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V239_20261030/manifest239.py tkon1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 150 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/tkon1.json bash $R $D/req/tkon_w.py tkon_w 1800 > $D/last_tkon_w.out 2>&1; grep -a -o "TKON239 .*" $D/last_tkon_w.out | cut -c1-700 >> $O
grep -a -q '"ok": true' $D/last_tkon_w.out && grep -a -q '"saved": true' $D/last_tkon_w.out || { echo "F_FAILED tkon" >> $O; exit 1; }
ab f "j39_rl:tk j39_rw:tk"
echo "F_DONE $(date +%T)" >> $O
