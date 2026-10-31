#!/bin/bash
# V2.41 J: 30 FPS full regression, production o vs combined candidate tkha (Own + HeadOn + per-K entry + regional AO); + push tkp, wall
source Saved/Codex/SHME_V241_20261031/lib241.sh; O=$D/chain.out
export SHME_MANIFEST=$D/checkpoint/manifests/aopre.json
echo "J start $(date +%T)" >> $O
WARM=1 ab reg "j41_rl_p10:tkha j41_rl_p16:tkha j41_lr_p10:tkha j41_rlw_p10:tkha"
ab reg " j40_rlw:o j40_rlw:tkha j40_lrw:o j40_lrw:tkha j39_rl:o j39_rl:tkha j39_rw:o j39_rw:tkha j39_rl_e:o j39_rl_e:tkha j39_rl_l:o j39_rl_l:tkha j39_lr:o j39_lr:tkha j39_lw:o j39_lw:tkha j38_cc90:o j38_cc90:tkha mtf_jog:o mtf_jog:tkha jlean:o jlean:tkha j38_c90r:o j38_c90r:tkha j38_c90l:o j38_c90l:tkha j38_c90rb:o j38_c90rb:tkha j38_c90lb:o j38_c90lb:tkha j38_c45r:o j38_c45r:tkha j38_c135r:o j38_c135r:tkha w38_c90r:o w38_c90r:tkha s38_c90r:o s38_c90r:tkha j36_rsm:o j36_rsm:tkha j36_stop:o j36_stop:tkha j36_stopr:o j36_stopr:tkha j34_chain1:o j34_chain1:tkha j35_rev:o j35_rev:tkha j30_rel_3450:o j30_rel_3450:tkha j36_sside:o j36_sside:tkha jstart:o jstart:tkha e29_chain:o e29_chain:tkha c29_combo:o c29_combo:tkha jdiag:o jdiag:tkha wdiag:o wdiag:tkha wstart:o wstart:tkha cam32_j90:o cam32_j90:tkha chain_jogcut:o chain_jogcut:tkha ad_jog:o ad_jog:tkha mt_jog:o mt_jog:tkha j39_push_plan:o j39_push_plan:tkha j39_push_jog:o j39_push_jog:tkha j41_rl_p10:o j41_rl_p10:tkha j41_rl_p16:o j41_rl_p16:tkha j41_lr_p10:o j41_lr_p10:tkha j41_rw_p10:tkha j41_rlw_p10:tkha j39_push_plan:tkp j40_wall:tkha j40_wall:wst"
echo "J_DONE $(date +%T)" >> $O
