#!/bin/bash
# V2.41 L: frame-rate modes 120 / 60 / 20 / real (one relaunch each). Block order per mode: production o (+ V2.40 wall variants) ->
# ONE in-memory regional-AO switch -> warm pass + candidate tkhaB / tkpB / wsto -> ONE reload (post241_ao).
source Saved/Codex/SHME_V241_20261031/lib241.sh; O=$D/chain.out
export SHME_MANIFEST=$D/checkpoint/manifests/aopre.json
OF="j41_rl_p10:o j41_rl_p16:o j41_lr_p10:o j41_rlw_p10:o j39_rw:o j38_cc90:o j40_rlw:o mtf_jog:o j39_push_plan:o j38_c90r:o j39_lr:o j40_wall:o j40_wall:wst j40_wall:wsto"
CF="j41_rl_p10:tkhaB j41_rl_p16:tkhaB j41_lr_p10:tkhaB j41_rlw_p10:tkhaB j39_rw:tkhaB j38_cc90:tkhaB j40_rlw:tkhaB mtf_jog:tkhaB j39_push_plan:tkhaB j39_push_plan:tkpB j38_c90r:tkhaB j39_lr:tkhaB"
OS="j41_rl_p10:o j41_lr_p10:o j41_rlw_p10:o j38_cc90:o j39_lr:o j40_wall:wst j40_wall:wsto"
CS="j41_rl_p10:tkhaB j41_lr_p10:tkhaB j41_rlw_p10:tkhaB j38_cc90:tkhaB j39_push_plan:tkhaB j39_push_plan:tkpB j39_lr:tkhaB"
WL="j41_rl_p10:tkhaB j41_rl_p16:tkhaB j41_lr_p10:tkhaB j41_rlw_p10:tkhaB"
blk() { bash $R Tools/SHME_V241_20261031/pre241_ao.py pre_ao 600 | grep -a "PREAO241" >> $O; WARM=0 ab $1 "$WL"; ab $1 "$2"; bash $R Tools/SHME_V241_20261031/post241_ao.py post_ao 600 | grep -a "POSTAO241" >> $O; }
echo "L start $(date +%T)" >> $O
relaunch f120 120; WARM=1 ab f120 "$OF"; blk f120 "$CF"
relaunch f60 60;   WARM=1 ab f60 "$OF";  blk f60 "$CF"
relaunch f20 20;   WARM=1 ab f20 "$OS";  blk f20 "$CS"
relaunch freal real; WARM=1 ab freal "$OS"; blk freal "$CS"
relaunch fend 30
echo "L_DONE $(date +%T)" >> $O
