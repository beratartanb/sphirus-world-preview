"""CORRECTIVE pass seam diagnosis: isolated child MIs that equalize the head / body shader switches at the neck seam
(both use M_skin_unified_baked; measured 2026-10-01: body Micro Skin Details ON / head OFF, head Bent Normal + Material AO ON / body OFF,
specular / concavity multipliers differ). Parents are referenced read-only. -> CharacterCorrective_20261001/Skin/Seam"""
import unreal as u, json
EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); F = '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Skin/Seam'; out = {}
SPECS = {
 'MI_CR_Face_LOD0_c12_sqA': ('/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Skin/MI_LK_Face_LOD0_VT_c12', {'Use Bent Normal': False, 'Use Material AO': False}, {}),
 'MI_CR_Face_LOD0_c12_sqB': ('/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Skin/MI_LK_Face_LOD0_VT_c12', {'Use Bent Normal': False, 'Use Material AO': False, 'Use Micro Skin Details': True}, {}),
 'MI_CR_Body_G_sqA': ('/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Skin/MI_LK_Body_Baked_G', {'Use Micro Skin Details': False}, {'Specular Global Multiply Post-Bake': 1.0, 'Specular Concavity Multiply': 0.6, 'Roughness Concavity Multiply': 1.4}),
 'MI_CR_Body_G_sqB': ('/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Skin/MI_LK_Body_Baked_G', {}, {'Specular Global Multiply Post-Bake': 1.0, 'Specular Concavity Multiply': 0.6, 'Roughness Concavity Multiply': 1.4}),
 'MI_CR_Face_LOD0_c12_sqN': ('/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Skin/MI_LK_Face_LOD0_VT_c12', {}, {'Normal Global Strength Post-Bake': 0.0}),
 'MI_CR_Body_G_sqN': ('/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Skin/MI_LK_Body_Baked_G', {'Use Micro Skin Details': False}, {'Normal Global Strength Post-Bake': 0.0}),
 'MI_CR_Body_H_sqB': ('/Game/Sphirus/CharacterLab/CharacterIdentity_20260930/Skin/MI_ID_Body_Baked_H', {}, {'Specular Global Multiply Post-Bake': 1.0, 'Specular Concavity Multiply': 0.6, 'Roughness Concavity Multiply': 1.4}),
}
for name, (par, sw, sc) in SPECS.items():
    p = F+'/'+name; m = u.load_asset(p) if EAL.does_asset_exist(p) else AT.create_asset(name, F, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
    ME.set_material_instance_parent(m, u.load_asset(par)); names_sw = [str(n) for n in ME.get_static_switch_parameter_names(m)]; names_sc = [str(n) for n in ME.get_scalar_parameter_names(m)]
    for k, v in sw.items(): assert k in names_sw, k; ME.set_material_instance_static_switch_parameter_value(m, k, v)
    for k, v in sc.items(): assert k in names_sc, k; ME.set_material_instance_scalar_parameter_value(m, k, v)
    ME.update_material_instance(m); EAL.save_loaded_asset(m, False)
    out[name] = {'parent': par.split('/')[-1], 'sw': {k: ME.get_material_instance_static_switch_parameter_value(m, k) for k in sw}, 'sc': {k: ME.get_material_instance_scalar_parameter_value(m, k) for k in sc}}
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('SEAM_MIS', json.dumps(out))
