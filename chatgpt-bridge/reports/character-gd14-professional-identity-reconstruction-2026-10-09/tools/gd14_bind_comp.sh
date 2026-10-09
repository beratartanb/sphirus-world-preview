#!/bin/bash
# gd14_bind_comp.sh <tag> : bind h75c hair + library M_SlightArch brows / S_Thin lashes onto GD14/Face/SKM_GD14_Face_<tag> (bindings in GD14/Face/Bindings;
# source grooms only referenced) unless NOBIND=1, then write the qa_config composition for that face and run the studio setup (save/studio -> GD14).
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; TAG=$1; W=Saved/Codex/GD14_Identity_20261009; T=Tools/CharacterLookdev_20260930; R=Tools/OutfitHome_20260929/run_of.sh; J=$W/jobs
G=/Game/Sphirus/CharacterLab/GD14_IdentityMaster_20261009; FACE=$G/Face/SKM_GD14_Face_$TAG; BF=$G/Face/Bindings; HD=/Game/Sphirus/CharacterLab/GD11_HairQ_20261006/Hair; HT=${HT:-h75c}; BROW=${BROW:-M_SlightArch}; BS=${TAG}${HT}
if [ -z "${NOBIND:-}" ]; then
  { echo "import builtins; builtins.FM_BIND = {'face': '$FACE', 'suffix': '$BS', 'prefix': 'GB_GD14', 'folder': '$BF', 'source': '/Game/Sphirus/CharacterLab/CharacterGuardian2_20261001/Face/SKM_GD_FaceMesh_p', 'grooms': {'HairMain': '$HD/GR_LK_Hair_Main_$HT', 'HairLoose': '$HD/GR_LK_Hair_Loose_$HT'}}"; cat $T/ue_fm_bind.py; } > $J/bind_$TAG.py
  bash $R $J/bind_$TAG.py gd14-bind-$TAG 900 | tail -1 | grep -oE '"dirty": \[[^]]*\]|Traceback.*|AssertionError.*'
  { echo "import builtins; builtins.GD_LB = {'face': '$FACE', 'suffix': '$TAG', 'bind_folder': '$BF', 'prefix': 'GB_GD14', 'items': [('Eyebrows', '$BROW'), ('Eyelashes', 'S_Thin')]}"; cat $T/ue_gd_lib_bind.py; } > $J/lb_$TAG.py
  bash $R $J/lb_$TAG.py gd14-lb-$TAG 1500 | grep -oE 'GD_LB.{0,160}|Traceback.*'
fi
MSYS_NO_PATHCONV=1 "/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" - "$FACE" "$BF" "$HD" "$HT" "$BS" "$TAG" "$BROW" <<'PYE'
import json, sys
face, bf, hd, ht, bs, tag, brow = sys.argv[1:8]; p = 'Saved/Codex/CharacterLookdev_20260930/qa_config.json'; d = json.load(open(p)); GD = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001'; Q = '/Game/Sphirus/CharacterLab/GD11_FaceR_20261006/Skin'
d['face'] = face; d['face_abp'] = '/MetaHumanCharacter/Face/ABP_Face.ABP_Face_C'
d['grooms'] = {'HairMain': {'groom': f'{hd}/GR_LK_Hair_Main_{ht}', 'binding': f'{bf}/GB_GD14_HairMain_{bs}', 'attach': 'Head'}, 'HairLoose': {'groom': f'{hd}/GR_LK_Hair_Loose_{ht}', 'binding': f'{bf}/GB_GD14_HairLoose_{bs}', 'attach': 'Head'},
               'Eyebrows': {'groom': f'{GD}/Grooms/GR_GD_Eyebrows_{brow}', 'binding': f'{bf}/GB_GD14_Eyebrows{brow}_{tag}', 'attach': 'Head'}, 'Eyelashes': {'groom': f'{GD}/Grooms/GR_GD_Eyelashes_S_Thin', 'binding': f'{bf}/GB_GD14_EyelashesS_Thin_{tag}', 'attach': 'Head'}}
for k, n in (('0', 'LOD0'), ('9', 'LOD1'), ('10', 'LOD2'), ('12', 'LOD3'), ('13', 'LOD4'), ('14', 'LOD5to7')): d['material_overrides']['Head'][k] = Q+f'/MI_LK_Face_{n}_VT_gqx19a'
d['material_overrides']['Head']['3'] = Q+'/MI_G11CC_EyeL_e3n'; d['material_overrides']['Head']['4'] = Q+'/MI_G11CC_EyeR_e3n'
d['material_overrides']['Body']['0'] = '/Game/Sphirus/CharacterLab/GD11_HeadRefinementC_20261004/Skin/MI_GC_Body_k10'
d['garments'] = {'Henley': GD+'/Outfit/SKM_LK_Henley_g17e', 'Shorts': '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Outfit/SKM_LK_Shorts_g16c'}
d['cloth_garments'] = {'Shorts': '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Cloth/CA_CR_Shorts_m1'}
CAND = '/Game/Sphirus/CharacterLab/GD14_IdentityMaster_20261009'; d['save_prefixes'] = [CAND]; d['studio_folder'] = CAND+'/Studio'
json.dump(d, open(p, 'w'), indent=1); print('GD14_COMP', face, ht, brow)
PYE
bash $R "$T/ue_lk_qa_setup.py" lk-setup 300 | tail -1 | cut -c1-300
