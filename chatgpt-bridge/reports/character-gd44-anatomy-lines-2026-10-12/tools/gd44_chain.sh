#!/bin/bash
# gd44_chain.sh : GD44 body tone pass, UE side (ALL new assets in /Game/Sphirus/CharacterLab/GD44_Lines_20261012; LK / GD38 assets read-only)
# 1 SKM_GD44_BodyMesh + ABP_GD44_Body_PostProcess (duplicates of the LK body + ABP, always-on GD44_Body curve; skeleton curve metadata
#   added after a checkpoint)   2 bake morph_gd44_body_lod0..3.json (candidate dir $1) as morph GD44_Body   3 qa composition: GD38 face t38 +
#   GD38 bindings / looks, body = SKM_GD44_BodyMesh, NO garments (body first, clothes in a later pass)   4 captures: full / close / dfm
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD44_Lines_20261012; T=$N/tools; R=Tools/OutfitHome_20260929/run_of.sh
CAND=${1:-$N/data/A2}; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; C=Saved/Codex/CharacterLookdev_20260930/captures; Wp() { cygpath -w "$(pwd)/$1"; }
mkdir -p $N/jobs $N/ue; bash Saved/Codex/GD38_Identity_20261011/tools/gd38_memguard.sh 22 | tail -1
[ -f $N/qa_config_before_gd44.json ] || cp Saved/Codex/CharacterLookdev_20260930/qa_config.json $N/qa_config_before_gd44.json
if [ ! -e Content/Sphirus/CharacterLab/GD44_Lines_20261012/Body/SKM_GD44_BodyMesh.uasset ]; then
  echo "== SETUP"; MSYS_NO_PATHCONV=1 bash $R "$(Wp $T/ue_gd44_body_setup.py)" gd44-setup 900 | grep -oE 'GD44_BODY_SETUP.{0,600}|Traceback.*|AssertionError.*'; fi
[ -e Content/Sphirus/CharacterLab/GD44_Lines_20261012/Body/SKM_GD44_BodyMesh.uasset ] || { echo SETUP_GATE_STOP; exit 2; }
echo "== BAKE $CAND"; { echo "import builtins; builtins.GD44_BODY_DIR = r'$(Wp $CAND)'"; cat $T/ue_gd44_bake_body.py; } > $N/jobs/bake_body.py
MSYS_NO_PATHCONV=1 bash $R "$(Wp $N/jobs/bake_body.py)" gd44-bake 1800 | grep -oE 'GD44_BAKE_BODY.{0,700}|Traceback.*|AssertionError.*'
grep -q '"ok": true' $CAND/ue_bake_body.json 2>/dev/null || { echo BAKE_GATE_STOP; exit 3; }
echo "== COMP"; MSYS_NO_PATHCONV=1 "$PY" - <<'PYE'
import json
p = 'Saved/Codex/CharacterLookdev_20260930/qa_config.json'; d = json.load(open('Saved/Codex/GD38_Identity_20261011/qa_config_after_gd38_chain.json'))
d['body'] = '/Game/Sphirus/CharacterLab/GD44_Lines_20261012/Body/SKM_GD44_BodyMesh'; d['garments'] = {}; d['cloth_garments'] = {}
C = '/Game/Sphirus/CharacterLab/GD44_Lines_20261012'; d['save_prefixes'] = [C]; d['studio_folder'] = C+'/Studio'
json.dump(d, open(p, 'w'), indent=1); print('GD44_COMP', d['body'], d['face'], list(d['grooms']))
PYE
bash $R "Tools/CharacterLookdev_20260930/ue_lk_qa_setup.py" lk-setup 300 | tail -1 | cut -c1-200
run() { local set=$1; "$PY" $T/gd44_req.py $set ${PFX:-g44} $C/capture_request.json | tail -1; local lab=${PFX:-g44}_$set; rm -f "$C/${lab}_results.json" "$C/${lab}_error.txt"
  bash $R "$(cygpath -w "$(pwd)/Tools/CharacterLookdev_20260930/ue_lk_capture.py")" lk-cap 120 | tail -1 >/dev/null
  for i in $(seq 1 1500); do { [ -f "$C/${lab}_results.json" ] || [ -f "$C/${lab}_error.txt" ]; } && break; sleep 2; done
  [ -f "$C/${lab}_error.txt" ] && { echo "ERROR $lab"; head -c 600 "$C/${lab}_error.txt"; } || { [ -f "$C/${lab}_results.json" ] && echo "DONE $lab" || echo "TIMEOUT $lab"; }
  for f in $C/${PFX:-g44}_*.png; do [ -f "$f" ] || continue; cp "$f" $N/ue/ && cmp -s "$f" "$N/ue/$(basename "$f")" && rm -f "$f"; done; }
for s in ${SETS:-full close dfm}; do run $s; done
ls $N/ue | wc -l; df -h /c | tail -1; echo GD44_CHAIN_DONE
