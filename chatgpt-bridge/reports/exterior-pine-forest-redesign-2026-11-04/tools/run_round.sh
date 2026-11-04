#!/bin/bash
# run_round.sh <variant> <tag> [skip_before] : one design round in the gated editor (owner pfr):
#   BEFORE stations (+top view) [unless skip_before] -> dryrun -> apply <variant> (all steps) -> top view -> AFTER stations -> walks A/B (csv)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V=${1:-p1}; TAG=${2:-$V}; SKIPB=${3:-0}
MY="/c/Users/berat/AppData/Local/Temp/claude/bbc6f8fdff1f8341/58bc34ab-b0fd-4574-9259-4850d781d32b/scratchpad"; D=Saved/Codex/PineForestRedesign_20261104; T=Tools/PineForestRedesign_20261104
export PFR_MANIFEST=Saved/Codex/SHME_V233_20261027/checkpoint/manifests/pfr_world.json
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
topview() { printf "import builtins\nbuiltins.PFR_TOP_TAG = '%s'\nexec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/PineForestRedesign_20261104/topview_pfr.py', encoding='utf-8').read(), 'topview_pfr.py', 'exec'), {'__name__': '__job__'})\n" "$1" > "$MY/top_$1.py"
  rm -f "$D/cap/top_$1/done.json"; bash $T/pfr_chain.sh "job:measure:$MY/top_$1.py:120" | tail -1; for i in $(seq 1 60); do [ -f "$D/cap/top_$1/done.json" ] && break; sleep 3; done; echo "topview $1: $(ls $D/cap/top_$1 | grep -c png) png"; }
echo "ROUND $V $TAG start $(date +%T)"
if [ "$SKIPB" != 1 ]; then
  bash $T/pfr_chain.sh views:before:lit:$D/data/stations_core.json | tail -3
  topview before
fi
for m in dryrun apply; do
  printf "import builtins\nbuiltins.PFR_MODE = '%s'\nbuiltins.PFR_VARIANT = '%s'\nexec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/PineForestRedesign_20261104/pfr_apply.py', encoding='utf-8').read(), 'pfr_apply.py', 'exec'), {'__name__': '__job__'})\n" "$m" "$V" > "$MY/apply_${m}_$V.py"
  rm -f "$D/design/$V/apply_$m.json"
  bash $T/pfr_chain.sh "job:write:$MY/apply_${m}_$V.py:900" | tail -2
  for i in $(seq 1 240); do [ -f "$D/design/$V/apply_$m.json" ] && break; sleep 5; done
  "$PY" -I -c "
import json,sys; d=json.load(open('$D/design/$V/apply_$m.json')); print('$m ok', d.get('ok'), 'problems', d['problems'][:6]); print(' log', d['log'][:8]); print(' newfol', json.dumps(d.get('newfol'))[:200]); print(' weights', d.get('weights_imported'), json.dumps(d.get('weights_readback'))[:300]); print(' actors', d.get('actors_spawned'), 'mats', d.get('mats'), 'look', d.get('look'), 'landscape', d.get('landscape'), 'dirty', len(d.get('dirty_after', [])))
sys.exit(0 if d.get('ok') else 1)" || { echo "ROUND STOP: $m failed $(date +%T)"; exit 1; }
done
topview "$TAG"
bash $T/pfr_chain.sh views:$TAG:lit:$D/data/stations_core.json "walk:${TAG}A:A:lit:1" "walk:${TAG}B:B:lit:1" | tail -6
echo "ROUND $V $TAG done $(date +%T)"
