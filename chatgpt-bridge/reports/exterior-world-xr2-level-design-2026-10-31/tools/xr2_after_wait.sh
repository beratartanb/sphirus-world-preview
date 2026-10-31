#!/bin/bash
# xr2_after_wait.sh <status.json> <chain jobs...> : wait for a running probe/views job to finish, then run the chain
for i in $(seq 1 1000); do grep -q -E '"state": "(done|error)"' "$1" 2>/dev/null && break; sleep 5; done; cat "$1"; echo; sleep 10; shift
bash "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/ExteriorWorld_XR2_20261031/xr2_chain.sh" "$@"
