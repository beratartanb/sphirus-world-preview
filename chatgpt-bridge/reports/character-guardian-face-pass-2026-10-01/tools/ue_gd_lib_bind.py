"""GUARDIAN face pass: bind MetaHumanCharacter LIBRARY grooms (authored on SKM_Groom_Head_Legacy01/02) to the candidate face with the
library groom head as SOURCE mesh (root transfer). Grooms duplicated into the Guardian folder (library assets untouched).
builtins.GD_LB = {'face', 'suffix', 'items': [(kind 'Eyebrows'|'Eyelashes', style)]}"""
import unreal as u, builtins, json
C = builtins.GD_LB; EAL = u.EditorAssetLibrary; F = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Grooms'; B = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Face/Bindings'
face = u.load_asset(C['face']); out = {}
SRC = {'Eyebrows': ('/MetaHumanCharacter/Optional/Grooms/GroomMesh/SKM_Groom_Head_Legacy01', 0), 'Eyelashes': ('/MetaHumanCharacter/Optional/Grooms/GroomMesh/SKM_Groom_Head_Legacy02', 8)}
for kind, st in C['items']:
    src = f'/MetaHumanCharacter/Optional/Grooms/GroomAssets/{kind}/{kind}_{st}/{kind}_{st}'; dst = f'{F}/GR_GD_{kind}_{st}'
    if not EAL.does_asset_exist(dst): assert EAL.duplicate_asset(src, dst), src
    g = u.load_asset(dst); sm, sec = SRC[kind]; bp = f'{B}/GB_GD_{kind}{st}_{C["suffix"]}'
    if EAL.does_asset_exist(bp): EAL.delete_asset(bp)   # own (Guardian) binding asset, rebuilt with the correct source mesh
    b = u.GroomLibrary.create_new_groom_binding_asset_with_path(bp, g, face, 100, u.load_asset(sm), sec)
    out[f'{kind}_{st}'] = bool(b) and EAL.save_loaded_asset(b, False)
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('GD_LB', json.dumps(out))
