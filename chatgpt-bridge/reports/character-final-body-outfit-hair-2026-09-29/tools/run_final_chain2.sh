#!/bin/bash
# Serialized CharacterFinal chain (captures must not overlap runner jobs). usage: run_final_chain.sh <steps...>
# steps: j4 setup_final neutral closeups deform gameplay lods clay shc hair audit_a6 body_dfm eval boards
set -u
P="/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; H="$P/Tools/CharacterFinal_20260929"; R="$P/Tools/OutfitHome_20260929/run_of.sh"; C="$P/Saved/Codex/CharacterFinal_20260929/captures"; E="$P/Saved/Codex/CharacterFinal_20260929"
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
W() { cygpath -w "$1"; }
wait_capture() { local label="$1"; local to="${2:-2400}"; for i in $(seq 1 $to); do
  if [ -f "$C/${label}_results.json" ]; then echo "capture $label done"; return 0; fi
  if [ -f "$C/${label}_error.txt" ]; then echo "capture $label ERROR"; cat "$C/${label}_error.txt"; return 1; fi; sleep 2; done; echo "capture $label TIMEOUT"; return 1; }
cap_set() { local set="$1"; local pfx="${2:-cf}"; rm -f "$C/${pfx}_${set}_results.json" "$C/${pfx}_${set}_error.txt"; "$PY" "$H/make_cf_request.py" "$set" "$pfx" | head -1; bash "$R" "$H/ue_cf_capture.py" "cfcap-$set-$RANDOM" 120 | head -2; wait_capture "${pfx}_$set"; }
step_ok() { local out="$1"; echo "$out" | tail -6; if echo "$out" | grep -qE "Traceback|AssertionError|^ERROR|TIMEOUT"; then echo "STEP FAILED -> abort chain"; echo CHAIN_ABORT; exit 1; fi; }
for s in "$@"; do echo "=== $s ($(date +%H:%M:%S))"; case $s in
  j4) { echo "import builtins; builtins.OF_GEO_FILE = 'outfit_v2_build_c/outfit_geometry.json.gz'; builtins.OF_WEIGHTS_FILE = 'outfit_v2_build_c/outfit_weights.json.gz'"; cat "$H/ue_cf_j4_meshes.py"; } > "$H/_cf_j4_run.py"; step_ok "$(bash "$R" "$H/_cf_j4_run.py" "cf-j4-$RANDOM" 1800)" ;;
  setup_final) cp "$E/qa_config_final.json" "$E/qa_config.json"; step_ok "$(bash "$R" "$H/ue_cf_qa_setup.py" "cf-setupF-$RANDOM" 300)" ;;
  setup_body) "$PY" -c "import json,sys;e=sys.argv[1];c=json.load(open(e+'/qa_config_final.json'));c['garments']={};c['grooms']={};json.dump(c,open(e+'/qa_config.json','w'))" "$(W "$E")"; step_ok "$(bash "$R" "$H/ue_cf_qa_setup.py" "cf-setupB-$RANDOM" 300)" ;;
  audit_a6) cap_set audit a6 ;;
  body_dfm) cap_set body_dfm cf ;;
  neutral|closeups|deform|gameplay|lods|clay|shc|hair) cap_set "$s" cf ;;
  eval) for lab in cf_deform cf_gameplay cf_lods cf_neutral cf_shc; do [ -f "$C/${lab}_results.json" ] && "$BL" -b --factory-startup --python "$(W "$H/blender_outfit_v2_eval.py")" -- "$(W "$C")" "$lab" "$(W "$C/eval_${lab}.json")" 2>&1 | grep -E "^cf_|EVAL_OK|Error|Traceback"; done ;;
  boards) for b in final deform gameplay lods hair closeups; do "$PY" "$H/make_cf_boards.py" $b cf | cut -c1-50; done; "$PY" "$H/make_cf_boards.py" audit_ab a5 a6 "BR v5" "CF v6" | cut -c1-40; "$PY" "$H/make_cf_boards.py" body_dfm cf | cut -c1-40 ;;
  hairalts) for st in Hair_S_PulledBack Hair_S_SweptUp Hair_S_LowPonytail; do
      "$PY" -c "import json,sys;e=sys.argv[1];c=json.load(open(e+'/qa_config_final.json'));c['grooms']={'Hair':{'groom':'/MetaHumanCharacter/Optional/Grooms/GroomAssets/Hair/$st/$st','binding':'/Game/Sphirus/CharacterLab/CharacterFinal_20260929/Hair/QA_${st}_Binding','attach':'Head'}};json.dump(c,open(e+'/qa_config.json','w'))" "$(W "$E")"
      step_ok "$(bash "$R" "$H/ue_cf_qa_setup.py" "cf-setupH-$RANDOM" 300)"; cap_set hairalt "alt_${st#Hair_S_}"; done; cp "$E/qa_config_final.json" "$E/qa_config.json"; step_ok "$(bash "$R" "$H/ue_cf_qa_setup.py" "cf-setupF-$RANDOM" 300)" ;;
  *) echo "unknown step $s" ;; esac; done
echo CHAIN_DONE
