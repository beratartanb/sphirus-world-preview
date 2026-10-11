#!/bin/bash
# gd36_look.sh <face asset path> <binding tag> : GD31 look composition for the QA studio. Binds (unless NOBIND=1) hair (BINDHAIR=1, h75c by
# default, P face as source) and library brows / lashes (duplicated into GD31/Grooms with an optional GD31 brow material), then writes
# qa_config: face + grooms + material overrides (face LOD skin MIs, eye MIs, body MI) and runs the studio setup. ALL writes in GD31 folders.
# env: CUSTOMBROW + CUSTOMBROW_BIND (GD31 custom brow groom + binding paths; replaces the library brow in the composition)
#      BROW (library style, default M_SlightArch) BROWMAT (MI path, '' = library default) BROWDS (dup suffix for the material variant)
#      LASH (S_Thin) EYE ('{s}' pattern MI path; default e3n) SKIN ('{lod}' pattern MI path; default gqx19a) BODY (MI path; default GC k10)
#      HT (hair tag, default h75c) HD (hair folder) HAIRMAT_MAIN / HAIRMAT_LOOSE (optional groom component material overrides)
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; FACE=$1; TAG=$2; W=Saved/Codex/GD36_Identity_20261011; T=Tools/CharacterLookdev_20260930; R=Tools/OutfitHome_20260929/run_of.sh; J=$W/jobs
G=/Game/Sphirus/CharacterLab/GD36_IdentityMaster_20261011; BF=$G/Face/Bindings; GF=$G/Grooms; HD=${HD:-/Game/Sphirus/CharacterLab/GD11_HairQ_20261006/Hair}; HT=${HT:-h75c}
BROW=${BROW:-M_SlightArch}; BROWMAT=${BROWMAT:-}; BROWDS=${BROWDS:-}; LASH=${LASH:-S_Thin}; Q=/Game/Sphirus/CharacterLab/GD11_FaceR_20261006/Skin
DEYE="$Q/MI_G11CC_Eye{s}_e3n"; DSKIN="$Q/MI_LK_Face_{lod}_VT_gqx19a"; EYE="${EYE:-$DEYE}"; SKIN="${SKIN:-$DSKIN}"; BODY=${BODY:-/Game/Sphirus/CharacterLab/GD11_HeadRefinementC_20261004/Skin/MI_GC_Body_k10}
if [ -z "${NOBIND:-}" ]; then
  if [ "${BINDHAIR:-1}" = 1 ]; then
    { echo "import builtins; builtins.FM_BIND = {'face': '$FACE', 'suffix': '${TAG}${HT}', 'prefix': 'GB_GD36', 'folder': '$BF', 'source': '/Game/Sphirus/CharacterLab/CharacterGuardian2_20261001/Face/SKM_GD_FaceMesh_p', 'grooms': {'HairMain': '$HD/GR_LK_Hair_Main_$HT', 'HairLoose': '$HD/GR_LK_Hair_Loose_$HT'}}"; cat $T/ue_fm_bind.py; } > $J/bind_$TAG.py
    bash $R $J/bind_$TAG.py gd31-bind-$TAG 900 | tail -1 | grep -oE '"saved": (true|false)|Traceback.*|AssertionError.*' | sort | uniq -c | tr '\n' ' '; echo
  fi
  BSH=""; [ -n "${BROWSRC_D:-}" ] && BSH=", {'d': $BROWSRC_D, 'tag': '${BROWSRC_TAG:-p}'}"   # optional brow source-proxy shift (cm, < 0 raises)
  MATS="None"; [ -n "$BROWMAT" ] && MATS="{'MI_Facial_Hair': '$BROWMAT', 'MI_Hair': '$BROWMAT'}"
  { echo "import builtins; builtins.GD17_LB = {'face': '$FACE', 'suffix': '$TAG', 'bind_folder': '$BF', 'groom_folder': '$GF', 'prefix': 'GB_GD36', 'items': [('Eyebrows', '$BROW', $MATS, '$BROWDS'$BSH), ('Eyelashes', '$LASH', None, '')]}"; cat $W/tools/ue_gd36_lib_bind.py; } > $J/lb_$TAG.py
  bash $R $J/lb_$TAG.py gd31-lb-$TAG 1500 | grep -oE '"ok": (true|false)|Traceback.*|AssertionError.*' | tr '\n' ' '; echo
fi
MSYS_NO_PATHCONV=1 "/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" - "$FACE" "$BF" "$GF" "$HD" "$HT" "$TAG" "$BROW$BROWDS" "$LASH" "$EYE" "$SKIN" "$BODY" "${HAIRMAT_MAIN:-}" "${HAIRMAT_LOOSE:-}" <<'PYE'
import json, sys
face, bf, gf, hd, ht, tag, brow, lash, eye, skin, body, hm, hl = sys.argv[1:14]; p = 'Saved/Codex/CharacterLookdev_20260930/qa_config.json'; d = json.load(open(p)); GD = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001'
d['face'] = face; d['face_abp'] = '/MetaHumanCharacter/Face/ABP_Face.ABP_Face_C'
d['grooms'] = {'HairMain': {'groom': f'{hd}/GR_LK_Hair_Main_{ht}', 'binding': f'{bf}/GB_GD36_HairMain_{tag}{ht}', 'attach': 'Head'}, 'HairLoose': {'groom': f'{hd}/GR_LK_Hair_Loose_{ht}', 'binding': f'{bf}/GB_GD36_HairLoose_{tag}{ht}', 'attach': 'Head'},
               'Eyebrows': {'groom': f'{gf}/GR_GD36_Eyebrows_{brow}', 'binding': f'{bf}/GB_GD36_Eyebrows{brow}_{tag}', 'attach': 'Head'}, 'Eyelashes': {'groom': f'{gf}/GR_GD36_Eyelashes_{lash}', 'binding': f'{bf}/GB_GD36_Eyelashes{lash}_{tag}', 'attach': 'Head'}}
import os
if os.environ.get('CUSTOMBROW'):   # GD31: custom (reference-curve) brow groom bound straight to the face (no source mesh)
    d['grooms']['Eyebrows'] = {'groom': os.environ['CUSTOMBROW'], 'binding': os.environ['CUSTOMBROW_BIND'], 'attach': 'Head'}
if hm: d['grooms']['HairMain']['material'] = hm
if hl: d['grooms']['HairLoose']['material'] = hl
for k, n in (('0', 'LOD0'), ('9', 'LOD1'), ('10', 'LOD2'), ('12', 'LOD3'), ('13', 'LOD4'), ('14', 'LOD5to7')): d['material_overrides']['Head'][k] = skin.replace('{lod}', n)
d['material_overrides']['Head']['3'] = eye.replace('{s}', 'L'); d['material_overrides']['Head']['4'] = eye.replace('{s}', 'R'); d['material_overrides']['Body']['0'] = body
d['garments'] = {'Henley': GD+'/Outfit/SKM_LK_Henley_g17e', 'Shorts': '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Outfit/SKM_LK_Shorts_g16c'}
d['cloth_garments'] = {'Shorts': '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Cloth/CA_CR_Shorts_m1'}
CAND = '/Game/Sphirus/CharacterLab/GD36_IdentityMaster_20261011'; d['save_prefixes'] = [CAND]; d['studio_folder'] = CAND+'/Studio'
json.dump(d, open(p, 'w'), indent=1); print('GD36_COMP', face.rsplit('/', 1)[-1], brow, eye.rsplit('/', 1)[-1], skin.rsplit('/', 1)[-1])
PYE
bash $R "$T/ue_lk_qa_setup.py" lk-setup 300 | tail -1 | cut -c1-160
