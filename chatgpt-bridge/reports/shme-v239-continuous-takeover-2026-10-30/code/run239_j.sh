#!/bin/bash
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; V9=/Game/GraceRanger/SHME/Animations/V239; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
M9() { MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V239_20261030/manifest239.py "$@" | tail -c 160 >> $O; }
echo "J start $(date +%T)" >> $O
TKS=$(for s in R_P21 R_P10; do for k in 1 2 3 4; do for t in Back Opp; do echo $V9/SHM239_Tk_${s}_K${k}_$t; done; done; done)
[ -f $MD/tkdb3.json ] || M9 tkdb3 --assets $V9/PSD_SHM239_Tk_Back $V9/PSD_SHM239_Tk_Opp $TKS
[ -f $D/last_tkdb3_w.out ] && grep -q TDB239_BIAS $D/last_tkdb3_w.out || SHME_KIND=write SHME_MANIFEST=$MD/tkdb3.json bash $R $D/req/tkdb3_w.py tkdb3_w 1800 > $D/last_tkdb3_w.out 2>&1; grep -a -o "TDB239_BIAS.*\|Traceback.*\|Error.\{0,200\}" $D/last_tkdb3_w.out >> $O
[ "$(grep -a -c 'TDB239_BIAS' $D/last_tkdb3_w.out)" = 2 ] || { echo "J_FAILED tkdb3" >> $O; exit 1; }
M9 thr1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching
SHME_KIND=write SHME_MANIFEST=$MD/thr1.json bash $R $D/req/thr_w.py thr_w 1800 > $D/last_thr_w.out 2>&1; grep -a -o "THR239 .*" $D/last_thr_w.out | cut -c1-400 >> $O
grep -a -q '"ok": true' $D/last_thr_w.out && grep -a -q '"saved": true' $D/last_thr_w.out || { echo "J_FAILED thr" >> $O; exit 1; }
WARM=1 ab jw "j39_rl:tk"
ab j "j39_rl:tk j39_rw:tk j38_c90r:tk j38_cc90:tk"
echo "J_DONE $(date +%T)" >> $O
