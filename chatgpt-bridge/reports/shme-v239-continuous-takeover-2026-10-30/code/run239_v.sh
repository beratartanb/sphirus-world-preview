#!/bin/bash
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
echo "V start $(date +%T)" >> $O
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V239_20261030/manifest239.py ext2 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 100 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/ext2.json bash $R $D/req/ext2_w.py ext2_w 1800 > $D/last_ext2_w.out 2>&1; grep -a -o "EXT2_239 .*" $D/last_ext2_w.out | cut -c1-300 >> $O
grep -a -q '"saved": true' $D/last_ext2_w.out || { echo "V_FAILED ext2" >> $O; exit 1; }
ab v "j39_push_plan:tk j39_push_jog:tk j38_c90r:tk j39_rl:tk j39_rl_e:tk j39_rw:tk j39_lr:tk"
echo "V_DONE $(date +%T)" >> $O
