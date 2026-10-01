"""GUARDIAN pass final QA composition: face <tag> + skin <skin> + SlightArch brows / S_Thin lashes + hair id18 + Henley g17e + Chaos shorts m1 + body MI t1"""
import json, sys
tag = sys.argv[1] if len(sys.argv) > 1 else 'h'; skin = sys.argv[2] if len(sys.argv) > 2 else 'c14s'; henley = sys.argv[3] if len(sys.argv) > 3 else '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Outfit/SKM_LK_Henley_g17e'
p = 'Saved/Codex/CharacterLookdev_20260930/qa_config.json'; d = json.load(open(p)); G = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001'; B = G+'/Face/Bindings/GB_GD'
d['face'] = G+f'/Face/SKM_GD_FaceMesh_{tag}'
d['grooms'] = {k: v for k, v in d['grooms'].items() if not (k.startswith('Brow') or k.startswith('Opt'))}
d['grooms']['HairMain'] = {'groom': G+'/Hair/GR_LK_Hair_Main_id18', 'binding': f'{B}_HairMain_{tag}', 'attach': 'Head'}
d['grooms']['HairLoose'] = {'groom': G+'/Hair/GR_LK_Hair_Loose_id18', 'binding': f'{B}_HairLoose_{tag}', 'attach': 'Head'}
d['grooms']['Eyebrows'] = {'groom': G+'/Grooms/GR_GD_Eyebrows_M_SlightArch', 'binding': f'{B}_EyebrowsM_SlightArch_{tag}', 'attach': 'Head'}
d['grooms']['Eyelashes'] = {'groom': G+'/Grooms/GR_GD_Eyelashes_S_Thin', 'binding': f'{B}_EyelashesS_Thin_{tag}', 'attach': 'Head'}
for k, n in (('0', 'LOD0'), ('9', 'LOD1'), ('10', 'LOD2'), ('12', 'LOD3'), ('13', 'LOD4'), ('14', 'LOD5to7')): d['material_overrides']['Head'][k] = G+f'/Skin/MI_LK_Face_{n}_VT_{skin}'
d['material_overrides']['Body']['0'] = G+'/Skin/MI_GD_Body_t1'
d['garments'] = {'Henley': henley, 'Shorts': '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Outfit/SKM_LK_Shorts_g16c'}
d['cloth_garments'] = {'Shorts': '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Cloth/CA_CR_Shorts_m1'}
json.dump(d, open(p, 'w'), indent=1); print('FINAL_COMP', tag, skin, henley.split('/')[-1])
