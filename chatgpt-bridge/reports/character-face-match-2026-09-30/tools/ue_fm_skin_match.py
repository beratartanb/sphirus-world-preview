"""FACE-MATCH pass: head/body skin MATERIAL match. Face (MI_LK_Face_*_c3) and body (MI_LK_Body_Baked_C) share the same master
(M_skin_unified_baked) and subsurface profile; the mismatch comes from their post-bake parameters:
  basecolor multiply (0.93,0.88,0.80) vs (0.92,0.855,0.765) + saturation -0.04 vs -0.09  -> body yellower / darker
  roughness offset 0 vs +0.1, specular multiply 1.0 vs 0.85, concavity multipliers         -> body flatter / less glossy
  micro-normal tiling 44 vs 70 over UV spaces of 46 cm vs 141 cm per unit                   -> body pores ~1.9x larger
Creates MI_LK_Body_Baked_<tag> (child of C) with the body brought into the face's family (values from builtins.FM_SKIN overrides).
builtins.FM_SKIN = {'tag': 'D', 'scalars': {...}, 'vectors': {...}}"""
import unreal as u, json, builtins
CFG = builtins.FM_SKIN; EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); F = '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Skin'
name = 'MI_LK_Body_Baked_'+CFG['tag']; path = F+'/'+name
m = u.load_asset(path) if EAL.does_asset_exist(path) else AT.create_asset(name, F, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
ME.set_material_instance_parent(m, u.load_asset(F+'/'+CFG.get('parent', 'MI_LK_Body_Baked_C')))
SN = {str(x) for x in ME.get_scalar_parameter_names(m)}; VN = {str(x) for x in ME.get_vector_parameter_names(m)}   # guard: unknown names would be stored and read back silently (MI D, 2026-09-30)
bad = [k for k in CFG.get('scalars', {}) if k not in SN]+[k for k in CFG.get('vectors', {}) if k not in VN]; assert not bad, ('unknown parameter names', bad)
for k, v in CFG.get('scalars', {}).items(): ME.set_material_instance_scalar_parameter_value(m, k, float(v))
for k, v in CFG.get('vectors', {}).items(): ME.set_material_instance_vector_parameter_value(m, k, u.LinearColor(*v, 1))
ME.update_material_instance(m); ok = EAL.save_loaded_asset(m, False)
print('FM_SKIN', name, ok, {k: round(ME.get_material_instance_scalar_parameter_value(m, k), 3) for k in CFG.get('scalars', {})})
