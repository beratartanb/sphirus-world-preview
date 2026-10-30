#!/bin/bash
# V2.40 J (after I): wall stop variants (stand DB / stop DB / force off) at 30 + 120, then captures (fixed 30)
source Saved/Codex/SHME_V240_20261030/lib240.sh; O=$D/chain.out
echo "J start $(date +%T)" >> $O
WARM=1 ab j30 "j40_wall:wst j40_wall:wof j40_wall:tkh j40_wall:o j39_push_plan:wst j38_c90r:wst"
relaunch j120 120
WARM=1 ab j120 "j40_wall:wst j40_wall:wof j40_wall:tkh"
relaunch jcap 30
WARM=1 ab cap "j40_rlw:oS j40_rlw:tkhS j40_rlw:tkhD j40_rlw:tkhG j40_rlw:oG j39_rl:oS j39_rl:tkhS j39_lr:oS j39_lr:tkhS j38_cc90:oS j38_cc90:tkhS j39_push_plan:oS j39_push_plan:tkhS j40_wall:oS j40_wall:tkhS j40_wall:wstS j40_wall:wofS j38_c90r:oG j38_c90r:tkhG" $D/vars240_cap.sh
relaunch jend 30
echo "J_DONE $(date +%T)" >> $O
