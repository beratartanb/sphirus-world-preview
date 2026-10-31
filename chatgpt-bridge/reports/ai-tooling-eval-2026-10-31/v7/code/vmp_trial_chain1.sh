#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad"
M="Saved/Codex/SHME_V233_20261027/checkpoint/manifests/vmp_map.json"
SHME_KIND=write SHME_OWNER=aitool SHME_MANIFEST="$M" bash Tools/SHME_V2_20261014/run_v2.sh "$SC/look_TRIAL_req.py" look_TRIAL 300 | tail -1 | cut -c1-200
SHME_KIND=write SHME_OWNER=aitool SHME_MANIFEST="$M" bash Tools/SHME_V2_20261014/run_v2.sh "$SC/vmp_build_req.py" vmp_build 600 | tail -1 | cut -c1-300
SHME_KIND=pie SHME_OWNER=aitool bash Tools/SHME_V2_20261014/run_v2.sh "$SC/stations_TRIAL_req.py" stations_TRIAL 120 | tail -1
S="$SC/vmp/TRIAL/stations_status.json"; for i in $(seq 1 300); do grep -q -E '"state": "(done|error)"' "$S" 2>/dev/null && break; sleep 5; done; cat "$S"; echo
echo CHAIN1_DONE
