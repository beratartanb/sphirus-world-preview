"""GUARDIAN-3 Phase 4 skin: face MIs MI_LK_Face_<LOD>_VT_g3<tag> (children of the GUARDIAN-2 g2c17 face MIs) and body MI MI_GD3_Body_<tag>
(child of the GUARDIAN MI_GD_Body_t1) with the SAME multiplicative change of 'Basecolor Global Multiply Post-Bake' on face and body (keeps the
head/body seam ratio), optional extra scalar overrides on both. Parents are referenced, never modified.
builtins.GD3_SKIN = {'tag': 's1', 'factor': [r, g, b], 'scalars': {name: value}}"""
import unreal as u, json, builtins
C = builtins.GD3_SKIN; EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
F = '/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001/Skin'; G2 = '/Game/Sphirus/CharacterLab/CharacterGuardian2_20261001/Skin'; GD = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Skin'
PN = 'Basecolor Global Multiply Post-Bake'; f = C['factor']; out = {}
def child(name, parent):
    dst = F+'/'+name; m = u.load_asset(dst) if EAL.does_asset_exist(dst) else AT.create_asset(name, F, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
    ME.set_material_instance_parent(m, parent); v = ME.get_material_instance_vector_parameter_value(parent, PN)
    nv = u.LinearColor(v.r*f[0], v.g*f[1], v.b*f[2], v.a); ME.set_material_instance_vector_parameter_value(m, PN, nv)
    for k, val in C.get('scalars', {}).items():
        try: ME.set_material_instance_scalar_parameter_value(m, k, val)
        except Exception: pass
    ME.update_material_instance(m); EAL.save_loaded_asset(m, False); r = ME.get_material_instance_vector_parameter_value(m, PN)
    out[name] = {'parent': parent.get_name(), 'tint_parent': [round(v.r, 3), round(v.g, 3), round(v.b, 3)], 'tint': [round(r.r, 3), round(r.g, 3), round(r.b, 3)]}
for n in ('LOD0', 'LOD1', 'LOD2', 'LOD3', 'LOD4', 'LOD5to7'):
    child(f"MI_LK_Face_{n}_VT_g3{C['tag']}", u.load_asset(f'{G2}/MI_LK_Face_{n}_VT_g2c17'))
child(f"MI_GD3_Body_{C['tag']}", u.load_asset(f'{GD}/MI_GD_Body_t1'))
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('GD3_SKIN', json.dumps(out))
