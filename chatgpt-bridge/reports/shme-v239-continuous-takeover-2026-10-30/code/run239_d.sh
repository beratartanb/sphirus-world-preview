#!/bin/bash
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
echo "D start $(date +%T)" >> $O
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V239_20261030/manifest239.py latch1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 150 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/latch1.json bash $R $D/req/latch_w.py latch_w 1800 > $D/last_latch_w.out 2>&1; grep -a -o "LATCH239 .*" $D/last_latch_w.out | cut -c1-700 >> $O
grep -a -q '"ok": true' $D/last_latch_w.out && grep -a -q '"saved": true' $D/last_latch_w.out || { echo "D_FAILED latch" >> $O; exit 1; }
ab d "j39_rl:tk j39_rw:tk j39_rl:o"
echo "D_DONE $(date +%T)" >> $O
