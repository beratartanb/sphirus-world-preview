#!/bin/bash
# gd3_face_run.sh <tag> : GUARDIAN-3 face composition + captures for the auto-rigged face CharacterGuardian3/Face/SKM_GD3_Face_<tag> (NEW DNA, plugin face
# skeleton + plugin ABP_Face / ABP_Face_PostProcess). Binds grooms (hair <HAIR|gd2:id20>, SlightArch brows, S_Thin lashes) unless NOBIND, sets qa_config
# (skin <SKIN|g2c17>, Henley g17e, Chaos shorts m1, body MI t1) and captures g3<tag>_{SETS}.
set -u; BS=${BSUF:-$1}; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; TAG=$1; T=Tools/CharacterLookdev_20260930; R=Tools/OutfitHome_20260929/run_of.sh
SC="C:/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/53df87b2-1800-4b0d-8cb5-35bc735c40a0/scratchpad"
G3=/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001; G4=/Game/Sphirus/CharacterLab/CharacterGuardian8_20261002; GD=/Game/Sphirus/CharacterLab/CharacterGuardian_20261001; G2=/Game/Sphirus/CharacterLab/CharacterGuardian2_20261001; G4R=/Game/Sphirus/CharacterLab/CharacterGuardian4_20261002; G5R=/Game/Sphirus/CharacterLab/CharacterGuardian5_20261002
HAIR=${HAIR:-g2:id20}; HK=${HAIR%%:*}; HT=${HAIR#*:}; case $HK in g2) HD=$G2/Hair;; g3) HD=$G3/Hair;; g4) HD=$G4R/Hair;; g5) HD=$G5R/Hair;; g6) HD=/Game/Sphirus/CharacterLab/CharacterGuardian6_20261002/Hair;; g7) HD=/Game/Sphirus/CharacterLab/CharacterGuardian7_20261002/Hair;; g8) HD=$G4/Hair;; gd) HD=$GD/Hair;; esac
if [ -z "${NOBIND:-}" ]; then
  { echo "import builtins; builtins.FM_BIND = {'face': '/Game/Sphirus/CharacterLab/CharacterGuardian7_20261002/Face/SKM_GD7_Face_$TAG', 'suffix': '$BS', 'prefix': 'GB_GD8', 'folder': '$G4/Face/Bindings', 'source': '${HAIRSRC:-/Game/Sphirus/CharacterLab/CharacterGuardian2_20261001/Face/SKM_GD_FaceMesh_p}', 'grooms': {'HairMain': '$HD/GR_LK_Hair_Main_$HT', 'HairLoose': '$HD/GR_LK_Hair_Loose_$HT'}}"; cat $T/ue_fm_bind.py; } > "$SC/gd4bind_$TAG.py"
  bash $R "$SC/gd4bind_$TAG.py" gd4bind-$TAG 900 | tail -1 | grep -o '"dirty": \[[^]]*\]'
  { echo "import builtins; builtins.GD_LB = {'face': '/Game/Sphirus/CharacterLab/CharacterGuardian7_20261002/Face/SKM_GD7_Face_$TAG', 'suffix': '$BS', 'bind_folder': '$G4/Face/Bindings', 'prefix': 'GB_GD8', 'items': [('Eyebrows', '${BROW:-M_SlightArch}'), ('Eyelashes', 'S_Thin')]}"; cat $T/ue_gd_lib_bind.py; } > "$SC/gd4_lb_$TAG.py"
  bash $R "$SC/gd4_lb_$TAG.py" gd4-lb-$TAG 1500 | grep -E "GD_LB|Traceback" | cut -c1-200
fi
MSYS_NO_PATHCONV=1 "/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" - "$TAG" "${SKIN:-g2c17}" "$HD" "$HT" "$BS" <<'PYE'
import json, sys, os
tag, skin, hd, ht, bs = sys.argv[1:6]; p = 'Saved/Codex/CharacterLookdev_20260930/qa_config.json'; d = json.load(open(p)); G3 = '/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001'; G4 = '/Game/Sphirus/CharacterLab/CharacterGuardian8_20261002'; GD = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001'; G2 = '/Game/Sphirus/CharacterLab/CharacterGuardian2_20261001'
d['face'] = '/Game/Sphirus/CharacterLab/CharacterGuardian7_20261002/Face/SKM_GD7_Face_'+tag; d['face_abp'] = '/MetaHumanCharacter/Face/ABP_Face.ABP_Face_C'; B = G4+'/Face/Bindings/GB_GD8'
d['grooms'] = {'HairMain': {'groom': hd+f'/GR_LK_Hair_Main_{ht}', 'binding': f'{B}_HairMain_{bs}', 'attach': 'Head'}, 'HairLoose': {'groom': hd+f'/GR_LK_Hair_Loose_{ht}', 'binding': f'{B}_HairLoose_{bs}', 'attach': 'Head'},
               'Eyebrows': {'groom': GD+'/Grooms/GR_GD_Eyebrows_'+os.environ.get('BROW', 'M_SlightArch'), 'binding': f'{B}_Eyebrows'+os.environ.get('BROW', 'M_SlightArch')+f'_{bs}', 'attach': 'Head'}, 'Eyelashes': {'groom': GD+'/Grooms/GR_GD_Eyelashes_S_Thin', 'binding': f'{B}_EyelashesS_Thin_{bs}', 'attach': 'Head'}}
G4R = '/Game/Sphirus/CharacterLab/CharacterGuardian4_20261002'; S = {'g2': G2+'/Skin', 'g3': G3+'/Skin', 'g4': G4R+'/Skin', 'g5': '/Game/Sphirus/CharacterLab/CharacterGuardian5_20261002/Skin', 'g6': '/Game/Sphirus/CharacterLab/CharacterGuardian6_20261002/Skin', 'g7': G4+'/Skin'}.get(skin[:2], GD+'/Skin'); sk = skin
for k, n in (('0', 'LOD0'), ('9', 'LOD1'), ('10', 'LOD2'), ('12', 'LOD3'), ('13', 'LOD4'), ('14', 'LOD5to7')): d['material_overrides']['Head'][k] = S+f'/MI_LK_Face_{n}_VT_{sk}'
E = os.environ.get('GD3_EYES_TAG'); E4 = os.environ.get('GD8_EYES_TAG')
if E: d['material_overrides']['Head']['3'] = G3+f'/Skin/MI_GD3_EyeL_{E}'; d['material_overrides']['Head']['4'] = G3+f'/Skin/MI_GD3_EyeR_{E}'
if E4: d['material_overrides']['Head']['3'] = G4+f'/Skin/MI_GD8_EyeL_{E4}'; d['material_overrides']['Head']['4'] = G4+f'/Skin/MI_GD8_EyeR_{E4}'
d['material_overrides']['Body']['0'] = {'g3': G3+'/Skin/MI_GD3_Body_'+skin[2:], 'g4': G4R+'/Skin/MI_GD4_Body_'+skin[2:], 'g5': '/Game/Sphirus/CharacterLab/CharacterGuardian5_20261002/Skin/MI_GD5_Body_'+skin[2:], 'g6': '/Game/Sphirus/CharacterLab/CharacterGuardian6_20261002/Skin/MI_GD6_Body_'+skin[2:], 'g7': G4+'/Skin/MI_GD8_Body_'+skin[2:]}.get(skin[:2], GD+'/Skin/MI_GD_Body_t1')
d['garments'] = {'Henley': GD+'/Outfit/SKM_LK_Henley_g17e', 'Shorts': '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Outfit/SKM_LK_Shorts_g16c'}
d['cloth_garments'] = {'Shorts': '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Cloth/CA_CR_Shorts_m1'}
d['save_prefixes'] = [G4]; d['studio_folder'] = G4+'/Studio'
json.dump(d, open(p, 'w'), indent=1); print('COMP4', tag, skin, ht)
PYE
bash $T/gd2_captures.sh g4$TAG ${SETS:-clay,real}
