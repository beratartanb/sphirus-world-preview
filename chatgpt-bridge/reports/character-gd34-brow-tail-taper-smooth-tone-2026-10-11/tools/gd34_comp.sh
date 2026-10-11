#!/bin/bash
# gd34_comp.sh <brow groom path> <brow binding path> : the GD31 final look (face G31 + n3 skin MIs + h6 eyes + body s1 + hair h75c + lashes
# S_Thin, all GD31 bindings, read-only) with the given brow; writes qa_config (snapshot: GD34/qa_config_before_gd34.json, restored at the end of the
# pass) and builds the QA studio. Brow colour variants are separate groom imports (the QA setup has no groom material override).
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD34_Identity_20261011
MSYS_NO_PATHCONV=1 "/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" - "$1" "$2" <<'PYE'
import json, sys
bg, bb = sys.argv[1:3]; p = 'Saved/Codex/CharacterLookdev_20260930/qa_config.json'; d = json.load(open(p))
G31 = '/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011'; L15 = '/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks'; HD = '/Game/Sphirus/CharacterLab/GD11_HairQ_20261006/Hair'
d['face'] = G31+'/Face/SKM_GD31_Face_g31'; d['face_abp'] = '/MetaHumanCharacter/Face/ABP_Face.ABP_Face_C'
d['grooms'] = {'HairMain': {'groom': HD+'/GR_LK_Hair_Main_h75c', 'binding': G31+'/Face/Bindings/GB_GD31_HairMain_g31cbh75c', 'attach': 'Head'},
               'HairLoose': {'groom': HD+'/GR_LK_Hair_Loose_h75c', 'binding': G31+'/Face/Bindings/GB_GD31_HairLoose_g31cbh75c', 'attach': 'Head'},
               'Eyebrows': {'groom': bg, 'binding': bb, 'attach': 'Head'},
               'Eyelashes': {'groom': G31+'/Grooms/GR_GD31_Eyelashes_S_Thin', 'binding': G31+'/Face/Bindings/GB_GD31_EyelashesS_Thin_g31cb', 'attach': 'Head'}}
for k, n in (('0', 'LOD0'), ('9', 'LOD1'), ('10', 'LOD2'), ('12', 'LOD3'), ('13', 'LOD4'), ('14', 'LOD5to7')): d['material_overrides']['Head'][k] = f'{G31}/Looks/MI_GD31_Face_{n}_s1t6n_n3'
d['material_overrides']['Head']['3'] = L15+'/MI_GD15_EyeL_h6'; d['material_overrides']['Head']['4'] = L15+'/MI_GD15_EyeR_h6'; d['material_overrides']['Body']['0'] = L15+'/MI_GD15_Body_s1'
d['garments'] = {'Henley': '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Outfit/SKM_LK_Henley_g17e', 'Shorts': '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Outfit/SKM_LK_Shorts_g16c'}
d['cloth_garments'] = {'Shorts': '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Cloth/CA_CR_Shorts_m1'}
C = '/Game/Sphirus/CharacterLab/GD34_IdentityMaster_20261011'; d['save_prefixes'] = [C]; d['studio_folder'] = C+'/Studio'
json.dump(d, open(p, 'w'), indent=1); print('GD34_COMP', bg.rsplit('/', 1)[-1])
PYE
bash Tools/OutfitHome_20260929/run_of.sh "Tools/CharacterLookdev_20260930/ue_lk_qa_setup.py" lk-setup 300 | tail -1 | cut -c1-160
