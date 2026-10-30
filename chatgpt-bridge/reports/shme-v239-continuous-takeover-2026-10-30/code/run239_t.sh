#!/bin/bash
# V2.39 T: external-effect residual (the plan yields) + live balance read -> push vs planned-motion tests
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
M9() { MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V239_20261030/manifest239.py "$@" | tail -c 120 >> $O; }
echo "T start $(date +%T)" >> $O
M9 ext1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching
SHME_KIND=write SHME_MANIFEST=$MD/ext1.json bash $R $D/req/ext_w.py ext_w 1800 > $D/last_ext_w.out 2>&1; grep -a -o "EXT239 .*\|AssertionError.*\|Traceback.*" $D/last_ext_w.out | cut -c1-400 >> $O
grep -a -q '"saved": true' $D/last_ext_w.out || { echo "T_FAILED ext" >> $O; exit 1; }
M9 bal1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching
SHME_KIND=write SHME_MANIFEST=$MD/bal1.json bash $R $D/req/bal_w.py bal_w 1800 > $D/last_bal_w.out 2>&1; grep -a -o "BAL239 .*\|AssertionError.*\|Traceback.*" $D/last_bal_w.out | cut -c1-300 >> $O
grep -a -q '"saved": true' $D/last_bal_w.out || { echo "T_FAILED bal" >> $O; exit 1; }
ab t "j39_push_plan:o j39_push_plan:tk j39_push_jog:o j39_push_jog:tk j38_c90r:tk j39_rl:tk j39_rw:tk j39_lr:tk"
echo "T_DONE $(date +%T)" >> $O
