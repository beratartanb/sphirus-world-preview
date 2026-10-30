#!/bin/bash
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
echo "P start $(date +%T)" >> $O
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V239_20261030/manifest239.py unthr1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 100 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/unthr1.json bash $R $D/req/unthr_w.py unthr_w 1800 > $D/last_unthr_w.out 2>&1; grep -a -o "UNTHR239 .*" $D/last_unthr_w.out | cut -c1-300 >> $O
grep -a -q '"saved": true' $D/last_unthr_w.out || { echo "P_FAILED unthr" >> $O; exit 1; }
ab p "j39_rl:tk j39_rw:tk j39_rl_e:tk j39_rl_l:tk j38_c90r:tk j38_cc90:tk"
echo "P_DONE $(date +%T)" >> $O
