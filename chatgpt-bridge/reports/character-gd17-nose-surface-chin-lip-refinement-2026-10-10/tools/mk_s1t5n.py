import builtins; builtins.GD17_MK = [{"dst": "/Game/Sphirus/CharacterLab/GD17_IdentityMaster_20261010/Looks/MI_GD17_Face_LOD0_s1t5n", "parent": "/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks/MI_GD15_Face_LOD0_s1t5", "scalar": {"Nose Strength": 0.9, "Intensity Nose": 0.35}}, {"dst": "/Game/Sphirus/CharacterLab/GD17_IdentityMaster_20261010/Looks/MI_GD17_Face_LOD1_s1t5n", "parent": "/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks/MI_GD15_Face_LOD1_s1t5", "scalar": {"Nose Strength": 0.9, "Intensity Nose": 0.35}}, {"dst": "/Game/Sphirus/CharacterLab/GD17_IdentityMaster_20261010/Looks/MI_GD17_Face_LOD2_s1t5n", "parent": "/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks/MI_GD15_Face_LOD2_s1t5", "scalar": {"Nose Strength": 0.9, "Intensity Nose": 0.35}}, {"dst": "/Game/Sphirus/CharacterLab/GD17_IdentityMaster_20261010/Looks/MI_GD17_Face_LOD3_s1t5n", "parent": "/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks/MI_GD15_Face_LOD3_s1t5", "scalar": {"Nose Strength": 0.9, "Intensity Nose": 0.35}}, {"dst": "/Game/Sphirus/CharacterLab/GD17_IdentityMaster_20261010/Looks/MI_GD17_Face_LOD4_s1t5n", "parent": "/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks/MI_GD15_Face_LOD4_s1t5", "scalar": {"Nose Strength": 0.9, "Intensity Nose": 0.35}}, {"dst": "/Game/Sphirus/CharacterLab/GD17_IdentityMaster_20261010/Looks/MI_GD17_Face_LOD5to7_s1t5n", "parent": "/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks/MI_GD15_Face_LOD5to7_s1t5", "scalar": {"Nose Strength": 0.9, "Intensity Nose": 0.35}}]
"""GD17: create material instances (NEW names, GD17 folder only) from a parent MI with parameter overrides.
builtins.GD17_MK = [{'dst': '/Game/.../GD17_IdentityMaster_.../Looks/MI_x', 'parent': path, 'scalar': {n: v}, 'vector': {n: [r,g,b,a]}, 'texture': {n: path}}]"""
import unreal as u, builtins, json
EAL = u.EditorAssetLibrary; MEL = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); out = {}
for it in builtins.GD17_MK:
    d = it['dst']; assert d.startswith('/Game/Sphirus/CharacterLab/GD17_IdentityMaster_'), 'GD17 guard'
    if EAL.does_asset_exist(d): out[d] = 'EXISTS_SKIPPED'; continue
    folder, name = d.rsplit('/', 1); mi = AT.create_asset(name, folder, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
    MEL.set_material_instance_parent(mi, u.load_asset(it['parent'])); r = {}
    for n, v in it.get('scalar', {}).items(): r[n] = MEL.set_material_instance_scalar_parameter_value(mi, n, float(v))
    for n, v in it.get('vector', {}).items(): r[n] = MEL.set_material_instance_vector_parameter_value(mi, n, u.LinearColor(*v))
    for n, v in it.get('texture', {}).items(): r[n] = MEL.set_material_instance_texture_parameter_value(mi, n, u.load_asset(v))
    MEL.update_material_instance(mi); out[d] = {'set': r, 'saved': EAL.save_loaded_asset(mi, False)}
print('GD17_MK', json.dumps(out))
