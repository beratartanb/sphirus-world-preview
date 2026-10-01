"""GUARDIAN face pass: common warm / tan skin tint for head AND body (same multiplicative factor on both 'Basecolor Global Multiply
Post-Bake' values, so the calibrated head/body seam ratio is kept), saturation + matte roughness offsets.
builtins.GD_TINT = {'face_slots': json path, 'k': [r,g,b], 'sat': d, 'rough': d, 'body_src': MI path, 'body_name': name}"""
import unreal as u, builtins, json
C = builtins.GD_TINT; EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); F = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Skin'; out = {}
def tint(m):
    v = ME.get_material_instance_vector_parameter_value(m, 'Basecolor Global Multiply Post-Bake'); k = C['k']
    ME.set_material_instance_vector_parameter_value(m, 'Basecolor Global Multiply Post-Bake', u.LinearColor(v.r*k[0], v.g*k[1], v.b*k[2], 1.0))
    s = ME.get_material_instance_scalar_parameter_value(m, 'Basecolor Global Saturation Post-Bake'); ME.set_material_instance_scalar_parameter_value(m, 'Basecolor Global Saturation Post-Bake', s+C['sat'])
    r = ME.get_material_instance_scalar_parameter_value(m, 'Roughness Global Offset Post-Bake'); ME.set_material_instance_scalar_parameter_value(m, 'Roughness Global Offset Post-Bake', r+C['rough'])
    ME.update_material_instance(m); EAL.save_loaded_asset(m, False); w = ME.get_material_instance_vector_parameter_value(m, 'Basecolor Global Multiply Post-Bake'); return [round(w.r, 3), round(w.g, 3), round(w.b, 3)]
for idx, p in json.load(open(C['face_slots'])).items(): out[p.split('/')[-1]] = tint(u.load_asset(p))
bp = F+'/'+C['body_name']; b = u.load_asset(bp) if EAL.does_asset_exist(bp) else AT.create_asset(C['body_name'], F, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
ME.set_material_instance_parent(b, u.load_asset(C['body_src']))
src = u.load_asset(C['body_src'])
for n in ('Basecolor Global Multiply Post-Bake',): ME.set_material_instance_vector_parameter_value(b, n, ME.get_material_instance_vector_parameter_value(src, n))
for n in ('Basecolor Global Saturation Post-Bake', 'Roughness Global Offset Post-Bake'): ME.set_material_instance_scalar_parameter_value(b, n, ME.get_material_instance_scalar_parameter_value(src, n))
out[C['body_name']] = tint(b); out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('GD_TINT', json.dumps(out))
