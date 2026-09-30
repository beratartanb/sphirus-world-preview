#!/bin/bash
# fm_skin_captures.sh <prefix> <body MI name> [face MI tag] : head/body SKIN-CONTINUITY diagnostics (face -> neck -> clavicle ->
# upper chest -> shoulder), garments hidden, hair on, under studio / grazing / interior / gameplay; front, 3/4 and side cams.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; P=$1; BM=$2; FT=${3:-c3}; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; C=Saved/Codex/CharacterLookdev_20260930/captures
"$PY" - "$BM" "$FT" <<'PYE'
import json, sys
bm, ft = sys.argv[1], sys.argv[2]; p = 'Saved/Codex/CharacterLookdev_20260930/qa_config.json'; d = json.load(open(p)); S = '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Skin/'
d['material_overrides']['Body']['0'] = S+bm
for k, n in (('0', 'LOD0'), ('9', 'LOD1'), ('10', 'LOD2'), ('12', 'LOD3'), ('13', 'LOD4'), ('14', 'LOD5to7')): d['material_overrides']['Head'][k] = S+f'MI_LK_Face_{n}_VT_{ft}'
json.dump(d, open(p, 'w'), indent=1); print('QA skin ->', bm, ft)
PYE
bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_lk_qa_setup.py" lk-setup 300 | tail -1
"$PY" -c "import json; S=[dict(name='${P}_'+l+'_'+k, view='custom', cam=c, fov=f, garments=False, materials='real', light=l, animation=None, time=0, light_target_z=150) for l in ('studio', 'grazing', 'interior', 'gameplay') for k, (c, f) in {'front': ([0, 105, 151, -90, 0], 22), '3q': ([-70, 76, 151, -47, 0], 22), 'side': ([105, 2, 151, 180, 0], 22)}.items()]; json.dump({'label': '${P}_skin', 'cases': S}, open('$C/capture_request.json', 'w'), indent=1)"
rm -f "$C/${P}_skin_results.json" "$C/${P}_skin_error.txt"
bash Tools/OutfitHome_20260929/run_of.sh "$(cygpath -w "$(pwd)/$T/ue_lk_capture.py")" lk-cap 120 | tail -1 >/dev/null
until [ -f "$C/${P}_skin_results.json" ] || [ -f "$C/${P}_skin_error.txt" ]; do sleep 2; done; [ -f "$C/${P}_skin_error.txt" ] && { echo "ERROR"; head -c 600 "$C/${P}_skin_error.txt"; } || echo "DONE ${P}_skin"
