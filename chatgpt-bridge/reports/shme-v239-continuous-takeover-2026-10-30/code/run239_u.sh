#!/bin/bash
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; V9=/Game/GraceRanger/SHME/Animations/V239; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
M9() { MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V239_20261030/manifest239.py "$@" | tail -c 120 >> $O; }
echo "U start $(date +%T)" >> $O
SAVED=$("$PY" -c "import json,glob;J={};[J.update({n:c for n,c in json.load(open(f))['clips'].items() if c.get('saved')}) for f in sorted(glob.glob('$D/gen239_tk_write_part*.json'))];print(' '.join('$V9/'+n for n in sorted(J)))")
NEWDB=$(for sd in R L; do for tg in Back Opp; do echo $V9/PSD_SHM239_Tk${sd}_$tg $V9/PSD_SHM239_TkP${sd}_$tg; done; done)
M9 tkside --assets $SAVED --new $NEWDB
SHME_KIND=write SHME_MANIFEST=$MD/tkside.json bash $R $D/req/tkdb_side.py tkdb_side 3000 > $D/last_tkdb_side.out 2>&1; echo "TDB_SIDE_N $(grep -a -c TDB239_BIAS $D/last_tkdb_side.out)" >> $O
[ "$(grep -a -c 'TDB239_BIAS' $D/last_tkdb_side.out)" = 8 ] || { echo "U_FAILED tkdb_side" >> $O; exit 1; }
M9 side1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching
SHME_KIND=write SHME_MANIFEST=$MD/side1.json bash $R $D/req/side_w.py side_w 1800 > $D/last_side_w.out 2>&1; grep -a -o "SIDE239 .*\|AssertionError.*" $D/last_side_w.out | cut -c1-300 >> $O
grep -a -q '"saved": true' $D/last_side_w.out || { echo "U_FAILED side" >> $O; exit 1; }
echo "U_DONE $(date +%T)" >> $O
