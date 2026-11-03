#!/bin/bash
# run251_a.sh : V2.51 chain A = A/B of the request-frame start database (eA), the yaw hand-over (eY) and both (eAY) at 60 / 30 / real
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V251_20261103; source $D/lib251.sh
relaunch a60 60; WARM=1 ab a60 "jstart:o jstart:eA jstart:eY jstart:eAY j45_sl2:eAY taps:eAY wstart:eAY j41_rl_p10:eAY j40_rlw:eAY w43_idle:eAY gait:eAY"
relaunch a30 30; WARM=1 ab a30 "jstart:eAY j42_lr_p10:eAY j45_sl2:eAY taps:eAY gait:eAY wstart:eAY w42_id:eAY j41_rl_p10:eAY"
relaunch areal real; WARM=1 ab areal "jstart:eAY jstart:eAY:2 j45_sl2:eAY j45_sl2:eAY:2 j45_sl2:eAY:3 taps:eAY"
echo TA251_DONE >> $O
