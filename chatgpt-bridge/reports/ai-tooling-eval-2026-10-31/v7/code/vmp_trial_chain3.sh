#!/bin/bash
# chain3: remove v2 props -> build v2 spec with build v2 rules (slope align, soft no-collision, short decals) -> stations -> walk (look stays TRIAL2)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad"
M="Saved/Codex/SHME_V233_20261027/checkpoint/manifests/vmp_map.json"
W() { SHME_KIND=write SHME_OWNER=aitool SHME_MANIFEST="$M" bash Tools/SHME_V2_20261014/run_v2.sh "$SC/$1" $2 600 | tail -1 | cut -c1-300; }
WAIT() { for i in $(seq 1 $2); do grep -q -E '"state": "(done|error)"' "$1" 2>/dev/null && break; sleep 5; done; cat "$1"; echo; sleep 10; }
W vmp_remove_req.py vmp_remove
W vmp_build2_req.py vmp_build2
rm -f "$SC/vmp/TRIAL3/stations_status.json" "$SC/vmp/walk_vmp_trial3/trailwalk_status.json"
SHME_KIND=pie SHME_OWNER=aitool bash Tools/SHME_V2_20261014/run_v2.sh "$SC/stations_TRIAL3_req.py" stations_TRIAL3 120 | tail -1
WAIT "$SC/vmp/TRIAL3/stations_status.json" 300
SHME_KIND=pie SHME_OWNER=aitool bash Tools/SHME_V2_20261014/run_v2.sh "$SC/trailwalk_vmp_trial3_req.py" walk_trial3 120 | tail -1
WAIT "$SC/vmp/walk_vmp_trial3/trailwalk_status.json" 400
echo CHAIN3_DONE
