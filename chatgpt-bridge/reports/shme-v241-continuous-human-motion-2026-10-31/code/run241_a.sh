#!/bin/bash
# V2.41 A: same-physical-state takeover entry (gated right request on the loop phase) o vs tkh, fixed 30 (current editor)
source Saved/Codex/SHME_V241_20261031/lib241.sh; O=$D/chain.out
echo "A start $(date +%T)" >> $O
WARM=1 ab a30 "j41_rl_p10:o j41_rl_p10:tkh j41_rl_p21:tkh j41_rl_p04:tkh j41_rl_p16:tkh j41_rl_p21:o"
echo "A_DONE $(date +%T)" >> $O
