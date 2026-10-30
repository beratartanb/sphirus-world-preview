#!/bin/bash
# V2.39 H: StepN on the cut clips, PREFIX takeover clips (P21 + P10, K1-4, Back / Opp), DB rebuild, request-time switch, test
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out; MD=$D/checkpoint/manifests
V8=/Game/GraceRanger/SHME/Animations/V238; V9=/Game/GraceRanger/SHME/Animations/V239; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
M9() { MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V239_20261030/manifest239.py "$@" | tail -c 160 >> $O; }
echo "H start $(date +%T)" >> $O
M9 step2 --assets $(for s in R L; do for p in $(seq -w 0 23); do echo $V8/SHM238_Cut_${s}_P$p; done; done)
SHME_KIND=write SHME_MANIFEST=$MD/step2.json bash $R $D/req/step_w.py step_w 1800 > $D/last_step_w.out 2>&1; grep -a -o "STEP239 .\{0,120\}" $D/last_step_w.out >> $O
grep -a -q '"ok": true' $D/last_step_w.out || { echo "H_FAILED step" >> $O; exit 1; }
OLD=$(for k in 1 2 3; do for t in Back Opp; do echo $V9/SHM239_Tk_R_P21_K${k}_$t; done; done)
NEW=$(for t in Back Opp; do echo $V9/SHM239_Tk_R_P21_K4_$t; for k in 1 2 3 4; do echo $V9/SHM239_Tk_R_P10_K${k}_$t; done; done)
M9 tk2 --assets $OLD --new $NEW
SHME_KIND=write SHME_MANIFEST=$MD/tk2.json bash $R $D/req/tk2_w.py tk2_w 2400 > $D/last_tk2_w.out 2>&1
"$PY" -c "import json;J=json.load(open('$D/gen239_tk_write.json'))['clips'];bad=[n for n,c in J.items() if not c.get('saved')];print('TK2', len(J), 'unsaved', bad, [ (n[-10:], c.get('error','')[-150:]) for n,c in J.items() if 'error' in c][:3])" >> $O
tail -1 $O | grep -q "unsaved \[\]" || { echo "H_FAILED tk2" >> $O; exit 1; }
M9 tkdb2 --assets $V9/PSD_SHM239_Tk_Back $V9/PSD_SHM239_Tk_Opp $OLD $NEW
SHME_KIND=write SHME_MANIFEST=$MD/tkdb2.json bash $R $D/req/tkdb2_w.py tkdb2_w 1800 > $D/last_tkdb2_w.out 2>&1; grep -a -o "TDB239 .\{0,300\}" $D/last_tkdb2_w.out >> $O
[ "$(grep -a -c 'TDB239_BIAS' $D/last_tkdb2_w.out)" = 2 ] || { echo "H_FAILED tkdb2" >> $O; exit 1; }
M9 req1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching
SHME_KIND=write SHME_MANIFEST=$MD/req1.json bash $R $D/req/req_w.py req_w 1800 > $D/last_req_w.out 2>&1; grep -a -o "REQ239 .*" $D/last_req_w.out | cut -c1-400 >> $O
grep -a -q '"ok": true' $D/last_req_w.out && grep -a -q '"saved": true' $D/last_req_w.out || { echo "H_FAILED req" >> $O; exit 1; }
WARM=1 ab h "j39_rl:tk j39_rw:tk"
echo "H_DONE $(date +%T)" >> $O
