#!/bin/bash
# usage: run_chain.sh <build_dir_name> [steps]   steps default: meshes lods setup neutral closeups deform gameplay lods_cap clay eval
set -u
P="/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; H="$P/Tools/OutfitHome_20260929"; C="$P/Saved/Codex/OutfitHome_20260929/captures"
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
BUILD="$1"; shift; STEPS="${@:-meshes lods setup neutral closeups deform gameplay lods_cap clay eval}"
W() { cygpath -w "$1"; }
wait_capture() { local label="$1"; local to="${2:-1800}"; for i in $(seq 1 $to); do
  if [ -f "$C/${label}_results.json" ]; then echo "capture $label done"; return 0; fi
  if [ -f "$C/${label}_error.txt" ]; then echo "capture $label ERROR"; cat "$C/${label}_error.txt"; return 1; fi; sleep 2; done; echo "capture $label TIMEOUT"; return 1; }
cap_set() { local set="$1"; rm -f "$C/of_${set}_results.json" "$C/of_${set}_error.txt"; "$PY" "$H/make_of_request.py" "$set" | head -1; bash "$H/run_of.sh" "$H/ue_of_capture.py" "cap-$set-$RANDOM" 120 | head -3; wait_capture "of_$set"; }
step_ok() { local out="$1"; echo "$out" | tail -8; if echo "$out" | grep -qE "Traceback|AssertionError|ERROR [0-9]|TIMEOUT"; then echo "STEP FAILED -> abort chain"; echo CHAIN_ABORT; exit 1; fi; }
for s in $STEPS; do echo "=== $s ($(date +%H:%M:%S))"; case $s in
  meshes) { echo "import builtins; builtins.OF_GEO_FILE = '$BUILD/outfit_geometry.json.gz'"; cat "$H/ue_of_j4_meshes.py"; } > "$H/_j4_run.py"; step_ok "$(bash "$H/run_of.sh" "$H/_j4_run.py" "j4-$RANDOM" 1200)" ;;
  lods) step_ok "$(bash "$H/run_of.sh" "$H/ue_of_j5_lods.py" "j5-$RANDOM" 900)" ;;
  setup) step_ok "$(bash "$H/run_of.sh" "$H/ue_of_qa_setup.py" "qa-setup-$RANDOM" 300)" ;;
  neutral|closeups|deform|gameplay|clay|shc) cap_set "$s" ;;
  lods_cap) cap_set lods ;;
  eval) for lab in of_deform of_gameplay of_lods of_neutral; do [ -f "$C/${lab}_results.json" ] && "$BL" -b --factory-startup --python "$(W "$H/blender_outfit_eval.py")" -- "$(W "$C")" "$lab" "$(W "$C/eval_${lab}.json")" 2>&1 | grep -E "^of_|EVAL_OK|Error|Traceback"; done ;;
  *) echo "unknown step $s" ;; esac; done
echo CHAIN_DONE
