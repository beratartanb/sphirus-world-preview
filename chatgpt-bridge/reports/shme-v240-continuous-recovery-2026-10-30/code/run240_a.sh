#!/bin/bash
source Saved/Codex/SHME_V240_20261030/lib240.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
echo "A start $(date +%T)" >> $O
# relaunch a 30 (editor already up)
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V240_20261030/manifest240.py once1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 100 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/once1.json bash $R $D/req/once_w.py once_w 1800 > $D/last_once_w.out 2>&1; grep -a -o "ONCE240 .*\|AssertionError.*\|Traceback.*" $D/last_once_w.out | cut -c1-300 >> $O
grep -a -q '"saved": true' $D/last_once_w.out || { echo "A_FAILED once" >> $O; exit 1; }
WARM=1 ab a30 "j39_rw:tk j39_rw:o j39_rl:tk j39_lr:tk j38_cc90:tk"
relaunch a120 120
WARM=1 ab a120 "j39_rw:tk j39_rw:o j39_rl:tk j39_lr:tk j38_cc90:tk"
relaunch aend 30
echo "A_DONE $(date +%T)" >> $O
