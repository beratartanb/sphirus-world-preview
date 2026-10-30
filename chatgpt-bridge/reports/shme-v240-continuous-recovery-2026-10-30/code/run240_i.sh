#!/bin/bash
# V2.40 I: wall throttle + head fade after the plan (install240_blk2); gate; focused 30; full 30 FPS regression o vs tkh; 60 / 20 / real
source Saved/Codex/SHME_V240_20261030/lib240.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
echo "I start $(date +%T)" >> $O
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V240_20261030/manifest240.py blk2 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 100 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/blk2.json bash $R $D/req/blk2_w.py blk2_w 1800 > $D/last_blk2_w.out 2>&1; grep -a -o "BLK2_240 .*\|AssertionError.*\|Traceback.*" $D/last_blk2_w.out | cut -c1-400 >> $O
grep -a -q '"saved": true' $D/last_blk2_w.out || { echo "I_FAILED blk2" >> $O; exit 1; }
relaunch i 30
WARM=1 ab igate "j38_c90r:o"
"$PY" -c "
import sys; sys.path[:0]=['Tools/SHME_V231_20261026']
from ltp231 import load
R=load('v240igate_j38_c90r_o_r1'); n=sum(1 for r in R if 'SHM238_Cut' in str(r.get('av_Phase27_SelectedObject')))
print('GATE_CUT_FRAMES', n)" >> $O
tail -1 $O | grep -q "GATE_CUT_FRAMES [1-9]" || { echo "I_FAILED gate" >> $O; exit 1; }
WARM=1 ab i30f "j40_wall:tk j38_c90r:hd j38_c90l:hd j38_c90r:tkh j39_lr:tkh j39_rl:tkh"
echo "I_FOCUSED $(date +%T)" >> $O
WARM=1 ab reg " j39_rl:o j39_rl:tkh j39_rw:o j39_rw:tkh j39_rl_e:o j39_rl_e:tkh j39_rl_l:o j39_rl_l:tkh j39_lr:o j39_lr:tkh j39_lw:o j39_lw:tkh j38_cc90:o j38_cc90:tkh mtf_jog:o mtf_jog:tkh jlean:o jlean:tkh j38_c90r:o j38_c90r:tkh j38_c90l:o j38_c90l:tkh j38_c90rb:o j38_c90rb:tkh j38_c90lb:o j38_c90lb:tkh j38_c45r:o j38_c45r:tkh j38_c135r:o j38_c135r:tkh w38_c90r:o w38_c90r:tkh s38_c90r:o s38_c90r:tkh j36_rsm:o j36_rsm:tkh j36_stop:o j36_stop:tkh j36_stopr:o j36_stopr:tkh j34_chain1:o j34_chain1:tkh j35_rev:o j35_rev:tkh j30_rel_3450:o j30_rel_3450:tkh j36_sside:o j36_sside:tkh jstart:o jstart:tkh e29_chain:o e29_chain:tkh c29_combo:o c29_combo:tkh jdiag:o jdiag:tkh wdiag:o wdiag:tkh wstart:o wstart:tkh cam32_j90:o cam32_j90:tkh j39_push_plan:o j39_push_plan:tkh j39_push_jog:o j39_push_jog:tkh chain_jogcut:o chain_jogcut:tkh ad_jog:o ad_jog:tkh mt_jog:o mt_jog:tkh  j40_rlw:o j40_rlw:tkh j40_lrw:o j40_lrw:tkh j40_wall:o j40_wall:tkh"
echo "I_REG $(date +%T)" >> $O
relaunch i60 60
WARM=1 ab i60 " j39_rl:o j39_rl:tkh j39_rw:o j39_rw:tkh j39_lr:o j39_lr:tkh j38_cc90:o j38_cc90:tkh j40_rlw:o j40_rlw:tkh j40_lrw:o j40_lrw:tkh j39_push_plan:o j39_push_plan:tkh j40_wall:o j40_wall:tkh j38_c90r:o j38_c90r:tkh j38_c90l:o j38_c90l:tkh"
relaunch i20 20
WARM=1 ab i20 " j39_rl:o j39_rl:tkh j39_rw:o j39_rw:tkh j39_lr:o j39_lr:tkh j38_cc90:o j38_cc90:tkh j40_rlw:o j40_rlw:tkh j40_lrw:o j40_lrw:tkh j39_push_plan:o j39_push_plan:tkh j40_wall:o j40_wall:tkh j38_c90r:o j38_c90r:tkh j38_c90l:o j38_c90l:tkh"
relaunch ireal real
WARM=1 ab ireal " j39_rl:o j39_rl:tkh j39_rw:o j39_rw:tkh j39_lr:o j39_lr:tkh j38_cc90:o j38_cc90:tkh j40_rlw:o j40_rlw:tkh j40_lrw:o j40_lrw:tkh j39_push_plan:o j39_push_plan:tkh j40_wall:o j40_wall:tkh j38_c90r:o j38_c90r:tkh j38_c90l:o j38_c90l:tkh"
relaunch iend 30
echo "I_DONE $(date +%T)" >> $O
