#!/bin/bash
# V2.41 E: production guard (knobs 0) + tkk (per-K entry DB) on the gated phases, fixed 30
source Saved/Codex/SHME_V241_20261031/lib241.sh; O=$D/chain.out
echo "E start $(date +%T)" >> $O
bash $R Tools/SHME_V240_20261030/verify240.py verify240 600 | grep -a "VERIFY240" | cut -c1-300 >> $O
WARM=1 ab e30 "j38_c90r:o j41_rl_p10:tkk j41_rl_p10:tkk:2 j41_rl_p16:tkk j41_rl_p21:tkk j41_rl_p04:tkk j41_rw_p10:tkk j41_rw_p16:tkk j41_lr_p10:tkk j41_lr_p16:tkk j41_rlw_p10:tkk j41_rlw_p16:tkk"
echo "E_DONE $(date +%T)" >> $O
