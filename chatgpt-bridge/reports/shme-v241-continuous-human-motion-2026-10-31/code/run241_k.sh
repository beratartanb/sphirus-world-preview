#!/bin/bash
# V2.41 K: unedited 30 fps captures (fixed step = real speed), same inputs before / after
source Saved/Codex/SHME_V241_20261031/lib241.sh; O=$D/chain.out
export SHME_MANIFEST=$D/checkpoint/manifests/aopre.json
echo "K start $(date +%T)" >> $O
WARM=1 ab cap "j40_rlw:oS j40_rlw:tkhaS j40_rlw:tkhaD j40_rlw:tkhaG j40_rlw:oG j39_lr:oS j39_lr:tkhaS j38_cc90:oS j38_cc90:tkhaS j39_push_plan:oS j39_push_plan:tkhaS j39_push_plan:tkpS j38_c90r:oG j38_c90r:tkhaG j38_c90r:aohG j40_wall:oS j40_wall:tkhaS" $D/vars241_cap.sh
CAP_START=4.6 CAP_SECS=9.0 ab cap "j41_rl_p10:oS j41_rl_p10:tkhS j41_rl_p10:tkhaS" $D/vars241_cap.sh
echo "K_DONE $(date +%T)" >> $O
