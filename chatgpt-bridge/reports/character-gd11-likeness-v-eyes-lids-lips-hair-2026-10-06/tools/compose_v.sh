#!/bin/bash
# compose_v.sh <label> <face tag in GD11_FaceR> <hair tag in GD11_HairQ> : pass-V composition; env SKINK (gqk13), BROWV (M_SlightArch | /Game/... custom groom),
# EYEMI (path with {s}; default e2), BODYMI (default k10 by skin key). Bindings: <face>h48a (brow/lash), <face><hair> (hair). Writes provenance to pass-V prov/.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; L=$1; FK=$2; HT=$3; T=Tools/CharacterLookdev_20260930; R=Saved/Codex/GD11_LikenessV_20261006; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/b05832b1-23f7-44dd-a92f-e1907201ea47/scratchpad"
F=/Game/Sphirus/CharacterLab/GD11_FaceR_20261006/Face/SKM_G11RR_Face_$FK; BP=/Game/Sphirus/CharacterLab/GD11_FaceR_20261006/Face/Bindings/GB_G11RR
MSYS_NO_PATHCONV=1 BROW=${BROWV:-M_SlightArch} FACE=$F NOBIND=1 BINDPFX=$BP BSUF=${FK}h48a HAIR=gm:h48a SKIN=${SKINK:-gqk13} GD3_EYES_TAG=e2 EYE_MI=${EYEMI:-} BODY_MI=${BODYMI:-} SETS=none CAPP=x bash $T/gd11rr_face_run.sh x >/dev/null
MSYS_NO_PATHCONV=1 "$PY" - "$HT" "$BP" "$FK$HT" <<'PYE'
import json, sys, os
p = 'Saved/Codex/CharacterLookdev_20260930/qa_config.json'; d = json.load(open(p)); t, hb, hs = sys.argv[1:4]; V = '/Game/Sphirus/CharacterLab/GD11_HairQ_20261006'
for part in ('Main', 'Loose'): d['grooms']['Hair'+part].update(groom=V+'/Hair/GR_LK_Hair_%s_%s' % (part, t), binding='%s_Hair%s_%s' % (hb, part, hs))
d['save_prefixes'] = ['/Game/Sphirus/CharacterLab/GD11_FaceR_20261006']; d['studio_folder'] = '/Game/Sphirus/CharacterLab/GD11_FaceR_20261006/Studio'
paths = [x for v in d['grooms'].values() for x in (v['binding'], v['groom'])] + [d['face']] + [v for v in list(d['material_overrides']['Head'].values())+list(d['material_overrides']['Body'].values()) if isinstance(v, str)]
bad = [x for x in paths if x.startswith('/Game/') and not os.path.exists(x.split('.')[0].replace('/Game/', 'Content/')+'.uasset')]
json.dump(d, open(p, 'w'), indent=1); print('QA', 'OK' if not bad else 'MISSING '+str(bad), d['face'].split('/')[-1], d['material_overrides']['Head'].get('0', '').split('_')[-1], d['material_overrides']['Head'].get('3', '').split('/')[-1], d['material_overrides']['Body'].get('0', '').split('/')[-1], {k: v['binding'].split('/')[-1] for k, v in d['grooms'].items()})
PYE
bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_lk_qa_setup.py" lk-setup 300 | tail -1 >/dev/null
mkdir -p $R/prov; { echo "import builtins; builtins.G11RO_PROV = {'label': '$L', 'candidate': '$FK + ${BROWV:-M_SlightArch} + $HT + ${SKINK:-gqk13} + ${EYEMI:-e2} + ${BODYMI:-k10}', 'out': r'$(cygpath -w "$(pwd)/$R/prov/$L.json")'}"; cat $T/ue_g11ro_provenance.py; } > "$SC/prov_$L.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/prov_$L.py" prov 300 | grep -o "G11RO_PROV" | head -1
