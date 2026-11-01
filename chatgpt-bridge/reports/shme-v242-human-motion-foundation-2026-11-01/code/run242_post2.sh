#!/bin/bash
# run242_post2.sh : after run242_post.sh - production captures aligned with the idle captures (same CAP_START) for side-by-side videos.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V242_20261101
for i in $(seq 1 240); do grep -q POST242_DONE $D/chain.out 2>/dev/null && break; sleep 30; done
source $D/lib242.sh
CAP_START=5.2 CAP_SECS=9.0 ab r6cap "w42_id:oS w42_id:oG" $D/vars242_cap.sh
echo POST2_242_DONE >> $O
