#!/bin/bash
# run_promote.sh <variant> : SAVE step (write job under the pfr_world manifest): dry report first, then the real save; prints both results.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V=${1:-p3}; MY="/c/Users/berat/AppData/Local/Temp/claude/bbc6f8fdff1f8341/58bc34ab-b0fd-4574-9259-4850d781d32b/scratchpad"; D=Saved/Codex/PineForestRedesign_20261104; T=Tools/PineForestRedesign_20261104
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
export PFR_MANIFEST=Saved/Codex/SHME_V233_20261027/checkpoint/manifests/pfr_world.json
for dry in True False; do
  printf "import builtins\nbuiltins.PFR_VARIANT = '%s'\nbuiltins.PFR_PROMOTE_DRY = %s\nexec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/PineForestRedesign_20261104/promote_pfr.py', encoding='utf-8').read(), 'promote_pfr.py', 'exec'), {'__name__': '__job__'})\n" "$V" "$dry" > "$MY/promote_$dry.py"
  rm -f "$D/design/$V/promote.json"; bash $T/pfr_chain.sh "job:write:$MY/promote_$dry.py:900" | tail -1
  for i in $(seq 1 180); do [ -f "$D/design/$V/promote.json" ] && break; sleep 5; done
  "$PY" -I -c "
import json; r=json.load(open('$D/design/$V/promote.json'))
print('PROMOTE dry=%s' % r['dry'], 'problems', r['problems'], 'save_ok', r.get('save_ok'))
print(' planned', len(r['save_planned']), 'outside', r['outside_not_saved'], 'unused', r.get('unused_deleted') or r.get('unused_would_delete') or r.get('unused_kept'))
print(' map sha1', r['map_sha1_before'][:8], '->', r.get('map_sha1_after','-')[:8], r.get('map_mtime'), 'dirty_after', r.get('dirty_after'), 'reload', r.get('outside_reloaded'))"
  if [ "$dry" = True ]; then grep -q '"problems": \[\]' "$D/design/$V/promote.json" || { echo "PROMOTE STOP: dry run reported problems"; exit 1; }; fi
done
