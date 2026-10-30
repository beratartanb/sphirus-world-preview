#!/bin/bash
# V2.39 Y: production intact check (verify238 in the clean 30 FPS editor) + captures (30 FPS game time, real speed)
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out
echo "Y start $(date +%T)" >> $O
SHME_KIND=measure bash $R $D/req/verify238.py verify 1800 > $D/verify_y.out 2>&1; grep -a -o '"ALL_OK": [a-z]*\|"bad": \[[^]]*\]' $D/verify_y.out | head -2 | tr '\n' ' ' | sed 's/^/VERIFY238_V239 /' >> $O; echo >> $O
ab cap "j39_rl:oS j39_rl:tkS j39_rl:oG j39_rl:tkG j39_rw:tkS j39_lr:tkS j38_cc90:oS j38_cc90:tkS j39_push_plan:oS j39_push_plan:tkS j39_rl:tkD" $D/vars239_cap.sh
echo "Y_DONE $(date +%T)" >> $O
