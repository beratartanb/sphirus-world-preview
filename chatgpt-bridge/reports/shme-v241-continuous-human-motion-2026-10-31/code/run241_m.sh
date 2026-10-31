#!/bin/bash
# V2.41 M: re-capture the AO variants (K captures ran with a refused PRE = no AO), 30 fps fixed step
source Saved/Codex/SHME_V241_20261031/lib241.sh; O=$D/chain.out
export SHME_MANIFEST=$D/checkpoint/manifests/aopre.json
echo "M start $(date +%T)" >> $O
WARM=1 ab cap2 "j40_rlw:tkhaS j40_rlw:tkhaD j40_rlw:tkhaG j39_lr:tkhaS j38_cc90:tkhaS j39_push_plan:tkhaS j38_c90r:tkhaG j38_c90r:aohG j40_wall:tkhaS" $D/vars241_cap.sh
CAP_START=4.6 CAP_SECS=9.0 ab cap2 "j41_rl_p10:tkhaS" $D/vars241_cap.sh
echo "M_DONE $(date +%T)" >> $O
