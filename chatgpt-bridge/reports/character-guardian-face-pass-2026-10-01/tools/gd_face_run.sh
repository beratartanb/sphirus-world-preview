#!/bin/bash
# gd_face_run.sh <tag> : GUARDIAN face cycle for Saved/Codex/CharacterGuardian_20261001/face/head<TAG>.npy + composition (final garments, hair id17, skin <SKIN|c12s>) + face captures g<tag>_{clay,real,hair}
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; TAG=$1; T=Tools/CharacterLookdev_20260930; G=Saved/Codex/CharacterGuardian_20261001; U=$(echo $TAG | tr a-z A-Z)
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
bash $T/gd_cycle.sh $TAG "$(cygpath -w "$(pwd)/$G/face/head$U.npy")" cr:id17
SC="C:/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/53df87b2-1800-4b0d-8cb5-35bc735c40a0/scratchpad"
{ echo "import builtins; builtins.GD_LB = {'face': '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Face/SKM_GD_FaceMesh_$TAG', 'suffix': '$TAG', 'items': [('Eyebrows', 'M_SlightArch'), ('Eyelashes', 'S_Thin')]}"; cat $T/ue_gd_lib_bind.py; } > "$SC/gd_lb_$TAG.py"
bash Tools/OutfitHome_20260929/run_of.sh "$SC/gd_lb_$TAG.py" gd-lb-$TAG 1500 | grep -E "GD_LB|Traceback" | cut -c1-200
BODYMI=${BODYMI:-/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Skin/MI_GD_Body_t1} "$PY" - "$TAG" "${SKIN:-c13s}" <<'PYE'
import json, sys
tag, skin = sys.argv[1], sys.argv[2]; p = 'Saved/Codex/CharacterLookdev_20260930/qa_config.json'; d = json.load(open(p)); F = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Face/'
d['face'] = F+f'SKM_GD_FaceMesh_{tag}'; B = F+'Bindings/GB_GD'; H = '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Hair/'
d['grooms']['HairMain'] = {'groom': H+'GR_LK_Hair_Main_id17', 'binding': f'{B}_HairMain_{tag}', 'attach': 'Head'}; d['grooms']['HairLoose'] = {'groom': H+'GR_LK_Hair_Loose_id17', 'binding': f'{B}_HairLoose_{tag}', 'attach': 'Head'}
d['grooms']['Eyebrows'] = {'groom': '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Grooms/GR_GD_Eyebrows_M_SlightArch', 'binding': f'{B}_EyebrowsM_SlightArch_{tag}', 'attach': 'Head'}; d['grooms']['Eyelashes'] = {'groom': '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Grooms/GR_GD_Eyelashes_S_Thin', 'binding': f'{B}_EyelashesS_Thin_{tag}', 'attach': 'Head'}
S = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Skin' if skin.startswith('c13') or skin.startswith('c14') or skin.startswith('c15') else '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Skin'
import os
if os.environ.get('BODYMI'): d['material_overrides']['Body']['0'] = os.environ['BODYMI']
for k, n in (('0', 'LOD0'), ('9', 'LOD1'), ('10', 'LOD2'), ('12', 'LOD3'), ('13', 'LOD4'), ('14', 'LOD5to7')): d['material_overrides']['Head'][k] = S+f'/MI_LK_Face_{n}_VT_{skin}'
O = '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Outfit/'; CL = '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Cloth/'
d['garments'] = {'Henley': O+'SKM_LK_Henley_g16c', 'Shorts': O+'SKM_LK_Shorts_g16c'}; d['cloth_garments'] = {'Shorts': CL+'CA_CR_Shorts_m1'}
for k in [k for k in d['grooms'] if k.startswith('Brow') or k.startswith('Opt')]: d['grooms'].pop(k)
json.dump(d, open(p, 'w'), indent=1); print('COMP', tag, skin)
PYE
bash $T/gd_captures.sh g$TAG ${SETS:-clay,real,hair}
