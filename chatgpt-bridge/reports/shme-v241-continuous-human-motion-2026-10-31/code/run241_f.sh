#!/bin/bash
# V2.41 F: push heading hold (tkp / extp) vs tkk / ext, fixed 30; production guard
source Saved/Codex/SHME_V241_20261031/lib241.sh; O=$D/chain.out
echo "F start $(date +%T)" >> $O
WARM=1 ab f30 "j38_c90r:o j39_push_plan:o j39_push_plan:tkk j39_push_plan:tkp j39_push_plan:ext j39_push_plan:extp j39_push_jog:tkk j39_push_jog:tkp j41_rl_p10:tkp j41_rl_p10:tkp:2"
echo "F_DONE $(date +%T)" >> $O
