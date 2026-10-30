#!/bin/bash
# V2.40 G: third-request yield + independent external-effect knob; behaviour gate; 30 / 120 FPS
source Saved/Codex/SHME_V240_20261030/lib240.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
echo "G start $(date +%T)" >> $O
for st in yield:YIELD240 extk:EXTK240; do n=${st%%:*}; k=${st##*:}
  MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V240_20261030/manifest240.py ${n}1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 100 >> $O
  SHME_KIND=write SHME_MANIFEST=$MD/${n}1.json bash $R $D/req/${n}_w.py ${n}_w 1800 > $D/last_${n}_w.out 2>&1; grep -a -o "$k .*\|AssertionError.*\|Traceback.*" $D/last_${n}_w.out | cut -c1-400 >> $O
  grep -a -q '"saved": true' $D/last_${n}_w.out || { echo "G_FAILED $n" >> $O; exit 1; }
done
relaunch g 30
WARM=1 ab ggate "j38_c90r:o"
"$PY" -c "
import sys; sys.path[:0]=['Tools/SHME_V231_20261026']
from ltp231 import load
R=load('v240ggate_j38_c90r_o_r1'); n=sum(1 for r in R if 'SHM238_Cut' in str(r.get('av_Phase27_SelectedObject')))
print('GATE_CUT_FRAMES', n)" >> $O
tail -1 $O | grep -q "GATE_CUT_FRAMES [1-9]" || { echo "G_FAILED gate: production does not route the cut" >> $O; exit 1; }
J="j40_rlw:tk j40_lrw:tk j39_rl:tk j39_lr:tk j39_rw:tk j38_cc90:tk j39_push_plan:tk j39_push_plan:ext j39_push_plan:o j39_push_jog:ext j40_wall:o j40_wall:ext j40_wall:tk j38_c90r:ext j40_lrw:o"
WARM=1 ab g30 "$J"
relaunch g120 120
WARM=1 ab g120 "j40_rlw:tk j40_lrw:tk j39_rl:tk j39_lr:tk j39_rw:tk j38_cc90:tk j39_lw:tk j39_rl_e:tk j39_push_plan:ext j40_wall:ext j40_rlw:o j40_lrw:o"
relaunch gend 30
echo "G_DONE $(date +%T)" >> $O
