#!/bin/bash
# run_lookcmp.sh <variant> : with the world applied, capture the 24 places under the XR5 FINAL v2 light (look restored) for the
# look decision, then re-apply the design look. Output cap/views_<variant>_xr5 ; the PF look set is the round's cap/views_after_<variant>.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V=${1:-p1}; MY="/c/Users/berat/AppData/Local/Temp/claude/bbc6f8fdff1f8341/58bc34ab-b0fd-4574-9259-4850d781d32b/scratchpad"; D=Saved/Codex/PineForestRedesign_20261104; T=Tools/PineForestRedesign_20261104
export PFR_MANIFEST=Saved/Codex/SHME_V233_20261027/checkpoint/manifests/pfr_world.json
for m in restore apply; do
  printf "import builtins\nbuiltins.PFR_MODE = '%s'\nbuiltins.PFR_VARIANT = '%s'\nbuiltins.PFR_STEPS = ['look']\nexec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/PineForestRedesign_20261104/pfr_apply.py', encoding='utf-8').read(), 'pfr_apply.py', 'exec'), {'__name__': '__job__'})\n" "$m" "$V" > "$MY/look_${m}_$V.py"
done
rm -f "$D/design/$V/apply_restore.json"; bash $T/pfr_chain.sh "job:write:$MY/look_restore_$V.py:300" | tail -1
for i in $(seq 1 40); do [ -f "$D/design/$V/apply_restore.json" ] && break; sleep 3; done; head -c 300 "$D/design/$V/apply_restore.json"; echo
bash $T/pfr_chain.sh "views:${V}_xr5:lit:$D/data/stations_places.json" | tail -2
rm -f "$D/design/$V/apply_apply.json"; bash $T/pfr_chain.sh "job:write:$MY/look_apply_$V.py:300" | tail -1
for i in $(seq 1 40); do [ -f "$D/design/$V/apply_apply.json" ] && break; sleep 3; done; head -c 300 "$D/design/$V/apply_apply.json"; echo
echo LOOKCMP_DONE
