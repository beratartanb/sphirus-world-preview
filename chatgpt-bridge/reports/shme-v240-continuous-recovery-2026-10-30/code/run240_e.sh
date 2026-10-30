#!/bin/bash
source Saved/Codex/SHME_V240_20261030/lib240.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; V0=/Game/GraceRanger/SHME/Animations/V240; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
M0() { MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V240_20261030/manifest240.py "$@" | tail -c 110 >> $O; }
echo "E start $(date +%T)" >> $O
M0 exit2 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching
SHME_KIND=write SHME_MANIFEST=$MD/exit2.json bash $R $D/req/exit2_w.py exit2_w 1800 > $D/last_exit2_w.out 2>&1; grep -a -o "EXIT2_240 .*\|AssertionError.*\|Traceback.*" $D/last_exit2_w.out | cut -c1-250 >> $O
grep -a -q '"saved": true' $D/last_exit2_w.out || { echo "E_FAILED exit2" >> $O; exit 1; }
M0 sch1 --assets $(for e in $(seq -w 0 95); do echo $V0/PSD_SHM240_E$e; done)
SHME_KIND=write SHME_MANIFEST=$MD/sch1.json bash $R $D/req/sch_w.py sch_w 1800 > $D/last_sch_w.out 2>&1; grep -a -o "SCH240 .*" $D/last_sch_w.out | cut -c1-200 >> $O
grep -a -q '"ok": true' $D/last_sch_w.out || { echo "E_FAILED sch" >> $O; exit 1; }
J="j39_rw:tk j39_rl:tk j39_lr:tk j38_cc90:tk j39_rl_e:tk j39_rl_l:tk j39_lw:tk j39_rw:o j39_lr:o j38_cc90:o"
WARM=1 ab e30w "j39_rl:tk j39_lr:tk"
ab e30 "$J"
relaunch e120 120
WARM=1 ab e120 "$J"
relaunch eend 30
echo "E_DONE $(date +%T)" >> $O
