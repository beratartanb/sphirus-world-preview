#!/bin/bash
# V2.41 B: entry schema PSS_SHM241_TkEntry (traj 0, both feet) on the gated phases, fixed 30
source Saved/Codex/SHME_V241_20261031/lib241.sh; O=$D/chain.out
echo "B start $(date +%T)" >> $O
WARM=1 ab b30 "j41_rl_p10:tkh j41_rl_p16:tkh j41_rl_p21:tkh j41_rl_p04:tkh j41_rw_p10:tkh j41_rw_p16:tkh j41_lr_p10:tkh j41_lr_p16:tkh j41_rlw_p10:tkh j41_rlw_p16:tkh"
echo "B_DONE $(date +%T)" >> $O
