#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V243_20261101
for i in $(seq 1 240); do grep -q REG243_DONE $D/chain.out 2>/dev/null && break; sleep 30; done; sleep 10
source $D/lib243.sh
CAP_START=10.8 CAP_SECS=3.2 ab t4cap "j41_rl_p04:latglS j41_rl_p04:latglG" $D/vars243_cap.sh
echo T4_DONE >> $O
