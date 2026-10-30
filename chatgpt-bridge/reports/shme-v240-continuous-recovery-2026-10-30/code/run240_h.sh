#!/bin/bash
# V2.40 H: wall stop (one forced stand search on a blocked Ext) + head priority (SHM240_HeadOn); gate; 30 / 120 FPS
source Saved/Codex/SHME_V240_20261030/lib240.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
echo "H start $(date +%T)" >> $O
for st in wall:WALL240 head:HEAD240; do n=${st%%:*}; k=${st##*:}
  MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V240_20261030/manifest240.py ${n}1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 100 >> $O
  SHME_KIND=write SHME_MANIFEST=$MD/${n}1.json bash $R $D/req/${n}_w.py ${n}_w 1800 > $D/last_${n}_w.out 2>&1; grep -a -o "$k .*\|AssertionError.*\|Traceback.*" $D/last_${n}_w.out | cut -c1-400 >> $O
  grep -a -q '"saved": true' $D/last_${n}_w.out || { echo "H_FAILED $n" >> $O; exit 1; }
done
relaunch h 30
WARM=1 ab hgate "j38_c90r:o"
"$PY" -c "
import sys; sys.path[:0]=['Tools/SHME_V231_20261026']
from ltp231 import load
R=load('v240hgate_j38_c90r_o_r1'); n=sum(1 for r in R if 'SHM238_Cut' in str(r.get('av_Phase27_SelectedObject')))
print('GATE_CUT_FRAMES', n)" >> $O
tail -1 $O | grep -q "GATE_CUT_FRAMES [1-9]" || { echo "H_FAILED gate: production does not route the cut" >> $O; exit 1; }
J="j40_wall:tk j40_wall:ext j40_wall:o j39_lr:tkh j39_rl:tkh j39_rw:tkh j40_rlw:tkh j38_cc90:tkh j38_c90r:hd j38_c90r:o j39_lr:o j39_push_plan:tk j39_push_plan:ext j38_c90l:hd j38_c90l:o"
WARM=1 ab h30 "$J"
relaunch h120 120
WARM=1 ab h120 "j40_wall:tk j40_wall:ext j39_rl:o j39_rl:tkh j39_push_plan:o j39_push_plan:tk j39_push_plan:ext j39_lr:tkh j40_rlw:tkh j40_lrw:tkh j38_c90r:hd"
relaunch hend 30
echo "H_DONE $(date +%T)" >> $O
