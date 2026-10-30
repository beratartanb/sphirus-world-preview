#!/bin/bash
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
echo "M start $(date +%T)" >> $O
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V239_20261030/manifest239.py srch1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 100 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/srch1.json bash $R $D/req/srch_w.py srch_w 1800 > $D/last_srch_w.out 2>&1; grep -a -o "SRCH239 .*" $D/last_srch_w.out | cut -c1-300 >> $O
grep -a -q '"saved": true' $D/last_srch_w.out || { echo "M_FAILED srch" >> $O; exit 1; }
ab m "j39_rl:tk j39_rw:tk j39_rl_e:tk j39_rl_l:tk j38_c90r:tk j38_cc90:tk"
echo "M_DONE $(date +%T)" >> $O
