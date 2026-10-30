#!/bin/bash
source Saved/Codex/SHME_V240_20261030/lib240.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
echo "D start $(date +%T)" >> $O
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V240_20261030/manifest240.py exit1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 100 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/exit1.json bash $R $D/req/exit_w.py exit_w 1800 > $D/last_exit_w.out 2>&1; grep -a -o "EXIT240 .*\|AssertionError.*\|Traceback.*" $D/last_exit_w.out | cut -c1-250 >> $O
grep -a -q '"saved": true' $D/last_exit_w.out || { echo "D_FAILED exit" >> $O; exit 1; }
J="j39_rw:tk j39_rl:tk j39_lr:tk j38_cc90:tk j39_rl_e:tk j39_rl_l:tk j39_lw:tk"
WARM=1 ab d30 "$J"
relaunch d120 120
WARM=1 ab d120 "$J"
relaunch dend 30
echo "D_DONE $(date +%T)" >> $O
