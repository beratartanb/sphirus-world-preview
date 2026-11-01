#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V242_20261101
for i in $(seq 1 120); do grep -q POST7_DONE $D/chain.out 2>/dev/null && break; sleep 30; done
source $D/lib242.sh
WARM=1 ab r8 "w42_id:idlh w42_id:oh"
echo POST8_DONE >> $O
