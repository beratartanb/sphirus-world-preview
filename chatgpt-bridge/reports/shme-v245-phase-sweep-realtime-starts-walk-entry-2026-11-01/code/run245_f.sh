#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V245_20261101
for i in $(seq 1 360); do grep -q WALK5_DONE $D/chain.out && break; sleep 20; done
source $D/lib245.sh
WARM=1 ab sweep4 "j45_rl_r0:o j45_rl_r1:o j45_rl_r2:o j45_rl_r3:o j45_rl_r4:o j45_rl_r5:o j45_lr_r0:o j45_lr_r1:o j45_lr_r2:o j45_lr_r3:o j45_lr_r4:o j45_lr_r5:o"
relaunch s4real real; WARM=1 ab sweep4real "j45_rl_r1:o j45_rl_r3:o j45_rl_r5:o j45_lr_r2:o j45_lr_r4:o"
relaunch s4end 30
echo SWEEP4_DONE >> $O
