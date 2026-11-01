#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V243_20261101
for i in $(seq 1 240); do grep -q DIAG243_DONE $D/chain.out 2>/dev/null && break; sleep 30; done; sleep 10
source $D/lib243.sh
WARM=1 ab reg "j42_lr_p10:all j41_rl_p04:all wdiag:o wdiag:all wstart:o wstart:all jstart:o jstart:all gait:o gait:all taps:o taps:all j38_c90r:o j38_c90r:all j40_rlw:o j40_rlw:all w42_id:all"
echo REG243_DONE >> $O
