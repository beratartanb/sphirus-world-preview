#!/bin/bash
# chain: for each variant apply look (write, manifest vmp_map) -> PIE stations (forward only) -> wait done; finally restore look.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad"
M="Saved/Codex/SHME_V233_20261027/checkpoint/manifests/vmp_map.json"
for v in V1 V2 V3; do
  SHME_KIND=write SHME_OWNER=aitool SHME_MANIFEST="$M" bash Tools/SHME_V2_20261014/run_v2.sh "$SC/look_${v}_req.py" look_$v 300 | tail -1 | cut -c1-300
  SHME_KIND=pie SHME_OWNER=aitool bash Tools/SHME_V2_20261014/run_v2.sh "$SC/stations_${v}_req.py" stations_$v 120 | tail -1
  S="$SC/vmp/$v/stations_status.json"
  for i in $(seq 1 200); do grep -q -E '"state": "(done|error)"' "$S" 2>/dev/null && break; sleep 5; done; cat "$S"; echo
done
SHME_KIND=write SHME_OWNER=aitool SHME_MANIFEST="$M" bash Tools/SHME_V2_20261014/run_v2.sh "$SC/look_restore_req.py" look_restore 300 | tail -1 | cut -c1-300
echo CHAIN_DONE
