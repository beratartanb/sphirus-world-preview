#!/bin/bash
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; V9=/Game/GraceRanger/SHME/Animations/V239; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
M9() { MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V239_20261030/manifest239.py "$@" | tail -c 160 >> $O; }
echo "K start $(date +%T)" >> $O
TKS=$(for s in R_P21 R_P10; do for k in 1 2 3 4; do for t in Back Opp; do echo $V9/SHM239_Tk_${s}_K${k}_$t; done; done; done)
M9 tkp1 --assets $TKS --new $V9/PSD_SHM239_TkP_Back $V9/PSD_SHM239_TkP_Opp
SHME_KIND=write SHME_MANIFEST=$MD/tkp1.json bash $R $D/req/tkp_w.py tkp_w 1800 > $D/last_tkp_w.out 2>&1; grep -a -o "TDB239_BIAS.*\|Traceback.*" $D/last_tkp_w.out >> $O
[ "$(grep -a -c 'TDB239_BIAS' $D/last_tkp_w.out)" = 2 ] || { echo "K_FAILED tkp" >> $O; exit 1; }
M9 play1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching
SHME_KIND=write SHME_MANIFEST=$MD/play1.json bash $R $D/req/play_w.py play_w 1800 > $D/last_play_w.out 2>&1; grep -a -o "PLAY239 .*\|Traceback.*\|AssertionError.*" $D/last_play_w.out | cut -c1-400 >> $O
grep -a -q '"ok": true' $D/last_play_w.out && grep -a -q '"saved": true' $D/last_play_w.out || { echo "K_FAILED play" >> $O; exit 1; }
WARM=1 ab kw "j39_rl:tk j39_rw:tk"
ab k "j39_rl:tk j39_rw:tk j38_c90r:tk j38_cc90:tk"
echo "K_DONE $(date +%T)" >> $O
