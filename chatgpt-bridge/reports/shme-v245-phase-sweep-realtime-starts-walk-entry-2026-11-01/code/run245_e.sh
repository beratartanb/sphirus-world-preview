#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V245_20261101; sleep 45
source $D/lib245.sh
WARM=1 ab sweep3 "j45_rl_r0:o j45_rl_r1:o j45_rl_r2:o j45_rl_r3:o j45_rl_r4:o j45_rl_r5:o j45_lr_r0:o j45_lr_r1:o j45_lr_r2:o j45_lr_r3:o j45_lr_r4:o j45_lr_r5:o"
echo SWEEP3_DONE >> $O; echo SWEEP2_DONE >> $O
