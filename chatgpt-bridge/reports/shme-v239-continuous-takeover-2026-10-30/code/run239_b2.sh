#!/bin/bash
# V2.39 B: contact-clock curve on the 48 cut clips -> R_P21 takeover clips -> takeover DBs -> ABP owner (OFF) -> clean reopen -> first test
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out; MD=$D/checkpoint/manifests
V8=/Game/GraceRanger/SHME/Animations/V238; V9=/Game/GraceRanger/SHME/Animations/V239; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
M9() { MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V239_20261030/manifest239.py "$@" | tail -c 160 >> $O; }
echo "B start $(date +%T)" >> $O
echo "B2 start $(date +%T)" >> $O
TKS=$(for k in 1 2 3; do for t in Back Opp; do echo $V9/SHM239_Tk_R_P21_K${k}_$t; done; done)
M9 tkdb1 --assets $TKS --new $V9/PSD_SHM239_Tk_Back $V9/PSD_SHM239_Tk_Opp
SHME_KIND=write SHME_MANIFEST=$MD/tkdb1.json bash $R $D/req/tkdb_w.py tkdb_w 1800 > $D/last_tkdb_w.out 2>&1; grep -a -o "TDB239.*" $D/last_tkdb_w.out | cut -c1-400 >> $O
[ "$(grep -a -c 'TDB239_BIAS' $D/last_tkdb_w.out)" = 2 ] || { echo "B2_FAILED tkdb" >> $O; exit 1; }
M9 own1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching
SHME_KIND=write SHME_MANIFEST=$MD/own1.json bash $R $D/req/own_w.py own_w 1800 > $D/last_own_w.out 2>&1; grep -a -o "OWN239 .*" $D/last_own_w.out | cut -c1-900 >> $O
grep -a -q '"ok": true' $D/last_own_w.out && grep -a -q '"saved": true' $D/last_own_w.out || { echo "B2_FAILED own" >> $O; exit 1; }
relaunch b 30
WARM=1 ab b "j39_rl:o j39_rl:tk j39_rw:tk j38_cc90:tk j38_c90r:tk"
echo "B2_DONE $(date +%T)" >> $O
