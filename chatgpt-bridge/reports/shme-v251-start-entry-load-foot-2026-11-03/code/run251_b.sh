#!/bin/bash
# run251_b.sh : V2.51 chain B = crop continuing-pose bias (asset level, in o) + eAYL (entry + yaw hand-over + load-aware start foot) +
# weighted idle with all fixes (oiL) at 60 / 30 / real
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V251_20261103; source $D/lib251.sh
relaunch b60 60; WARM=1 ab b60 "jstart:o jstart:eAYL j45_sl2:eAYL w42_id:eAYL gait:eAYL wstart:eAYL taps:eAYL w43_idle:eAYL j40_rlw:eAYL w42_id:oiL gait:oiL wstart:oiL taps:oiL w43_idle:oiL j45_sl2:oiL"
relaunch b30 30; WARM=1 ab b30 "jstart:eAYL j42_lr_p10:eAYL w42_id:eAYL gait:eAYL wstart:eAYL taps:eAYL w42_id:oiL gait:oiL wstart:oiL taps:oiL w43_idle:oiL jstart:oiL j45_sl2:oiL"
relaunch breal real; WARM=1 ab breal "jstart:eAYL j45_sl2:eAYL j45_sl2:eAYL:2 w42_id:oiL wstart:oiL taps:oiL gait:oiL"
echo TB251_DONE >> $O
