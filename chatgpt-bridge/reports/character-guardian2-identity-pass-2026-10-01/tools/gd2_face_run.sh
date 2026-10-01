#!/bin/bash
# gd2_face_run.sh <tag> : GUARDIAN-2 face cycle for Saved/Codex/CharacterGuardian2_20261001/face/head<TAG>.npy (all new assets in CharacterGuardian2_20261001)
# + composition (Henley g17e, Chaos shorts m1, hair <HAIR|gd:id18>, skin <SKIN|c14s>, body MI t1) + face captures g2<tag>_{sets}
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; TAG=$1; T=Tools/CharacterLookdev_20260930; G=Saved/Codex/CharacterGuardian2_20261001; U=$(echo $TAG | tr a-z A-Z)
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; HAIR=${HAIR:-gd:id18}
[ -z "${NOCYCLE:-}" ] && bash $T/gd2_cycle.sh $TAG "$(cygpath -w "$(pwd)/$G/face/head$U.npy")" $HAIR
SC="C:/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/53df87b2-1800-4b0d-8cb5-35bc735c40a0/scratchpad"
G2C=/Game/Sphirus/CharacterLab/CharacterGuardian2_20261001
[ -z "${NOCYCLE:-}" ] && { { echo "import builtins; builtins.GD_LB = {'face': '$G2C/Face/SKM_GD_FaceMesh_$TAG', 'suffix': '$TAG', 'bind_folder': '$G2C/Face/Bindings', 'items': [('Eyebrows', 'M_SlightArch'), ('Eyelashes', 'S_Thin')]}"; cat $T/ue_gd_lib_bind.py; } > "$SC/gd2_lb_$TAG.py"
  bash Tools/OutfitHome_20260929/run_of.sh "$SC/gd2_lb_$TAG.py" gd2-lb-$TAG 1500 | grep -E "GD_LB|Traceback" | cut -c1-200; }
"$PY" - "$TAG" "${SKIN:-c14s}" "$HAIR" <<'PYE'
import json, sys, os
tag, skin, hair = sys.argv[1:4]; p = 'Saved/Codex/CharacterLookdev_20260930/qa_config.json'; d = json.load(open(p)); G2 = '/Game/Sphirus/CharacterLab/CharacterGuardian2_20261001'; GD = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001'
F = G2+'/Face/'; d['face'] = F+f'SKM_GD_FaceMesh_{tag}'; B = F+'Bindings/GB_GD'
hk, ht = hair.split(':'); H = {'gd': GD, 'g2': G2, 'cr': '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001'}[hk]+'/Hair/'
d['grooms']['HairMain'] = {'groom': H+f'GR_LK_Hair_Main_{ht}', 'binding': f'{B}_HairMain_{tag}', 'attach': 'Head'}; d['grooms']['HairLoose'] = {'groom': H+f'GR_LK_Hair_Loose_{ht}', 'binding': f'{B}_HairLoose_{tag}', 'attach': 'Head'}
d['grooms']['Eyebrows'] = {'groom': GD+'/Grooms/GR_GD_Eyebrows_M_SlightArch', 'binding': f'{B}_EyebrowsM_SlightArch_{tag}', 'attach': 'Head'}; d['grooms']['Eyelashes'] = {'groom': GD+'/Grooms/GR_GD_Eyelashes_S_Thin', 'binding': f'{B}_EyelashesS_Thin_{tag}', 'attach': 'Head'}
S = G2+'/Skin' if skin.startswith('g2') else GD+'/Skin'
d['material_overrides']['Body']['0'] = os.environ.get('BODYMI', GD+'/Skin/MI_GD_Body_t1')
for k, n in (('0', 'LOD0'), ('9', 'LOD1'), ('10', 'LOD2'), ('12', 'LOD3'), ('13', 'LOD4'), ('14', 'LOD5to7')): d['material_overrides']['Head'][k] = S+f'/MI_LK_Face_{n}_VT_{skin}'
d['garments'] = {'Henley': os.environ.get('HENLEY', GD+'/Outfit/SKM_LK_Henley_g17e'), 'Shorts': '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Outfit/SKM_LK_Shorts_g16c'}
d['cloth_garments'] = {'Shorts': '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Cloth/CA_CR_Shorts_m1'}
for k in [k for k in d['grooms'] if k.startswith('Brow') or k.startswith('Opt')]: d['grooms'].pop(k)
d['save_prefixes'] = [G2]; d['studio_folder'] = G2+'/Studio'
json.dump(d, open(p, 'w'), indent=1); print('COMP', tag, skin, hair)
PYE
bash $T/gd2_captures.sh g2$TAG ${SETS:-clay,real}
