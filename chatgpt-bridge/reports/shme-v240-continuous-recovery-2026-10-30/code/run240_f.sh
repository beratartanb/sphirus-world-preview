#!/bin/bash
# V2.40 F: repair the snapshot exec chain, behaviour gate (production must route the V2.38 cut), candidate 30 / 120
source Saved/Codex/SHME_V240_20261030/lib240.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
echo "F start $(date +%T)" >> $O
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V240_20261030/manifest240.py fix1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 100 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/fix1.json bash $R $D/req/fix_w.py fix_w 1800 > $D/last_fix_w.out 2>&1; grep -a -o "FIX240 .*\|AssertionError.*\|Traceback.*" $D/last_fix_w.out | cut -c1-300 >> $O
grep -a -q '"saved": true' $D/last_fix_w.out || { echo "F_FAILED fix" >> $O; exit 1; }
relaunch f 30
WARM=1 ab fgate "j38_c90r:o"
"$PY" -c "
import sys; sys.path[:0]=['Tools/SHME_V231_20261026']
from ltp231 import load
R=load('v240fgate_j38_c90r_o_r1'); n=sum(1 for r in R if 'SHM238_Cut' in str(r.get('av_Phase27_SelectedObject')))
print('GATE_CUT_FRAMES', n)" >> $O
tail -1 $O | grep -q "GATE_CUT_FRAMES [1-9]" || { echo "F_FAILED gate: production does not route the cut" >> $O; exit 1; }
J="j39_rw:tk j39_rl:tk j39_lr:tk j38_cc90:tk j39_rl_e:tk j39_rl_l:tk j39_lw:tk j40_rlw:tk j40_lrw:tk j39_rw:o j39_lr:o j38_cc90:o j40_rlw:o"
WARM=1 ab f30 "$J"
relaunch f120 120
WARM=1 ab f120 "$J"
relaunch fend 30
echo "F_DONE $(date +%T)" >> $O
