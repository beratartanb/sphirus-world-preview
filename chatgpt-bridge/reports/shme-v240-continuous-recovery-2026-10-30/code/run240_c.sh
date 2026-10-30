#!/bin/bash
source Saved/Codex/SHME_V240_20261030/lib240.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
echo "C start $(date +%T)" >> $O
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V240_20261030/manifest240.py done1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 100 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/done1.json bash $R $D/req/done_w.py done_w 1800 > $D/last_done_w.out 2>&1; grep -a -o "DONE240 .*\|AssertionError.*\|Traceback.*" $D/last_done_w.out | cut -c1-250 >> $O
grep -a -q '"saved": true' $D/last_done_w.out || { echo "C_FAILED done" >> $O; exit 1; }
J="j39_rw:tk j39_rl:tk j39_lr:tk j38_cc90:tk j39_rl_e:tk j39_rl_l:tk j39_lw:tk"
WARM=1 ab c30 "$J"
relaunch c120 120
WARM=1 ab c120 "$J"
relaunch cend 30
echo "C_DONE $(date +%T)" >> $O
