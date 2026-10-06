"""GD11 pass V: material-instance variants by duplication (sources untouched). builtins.G11RV_MI = [{'src', 'dst', 'scalar': {}, 'vector': {}}]
every parameter name is asserted to exist (silent-name trap); read back after save."""
import unreal as u, builtins, json
EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; out = {}
for J in builtins.G11RV_MI:
    m = EAL.load_asset(J['dst']) if EAL.does_asset_exist(J['dst']) else EAL.duplicate_asset(J['src'], J['dst']); assert m, J['dst']
    sn = [str(x) for x in ME.get_scalar_parameter_names(m)]; vn = [str(x) for x in ME.get_vector_parameter_names(m)]
    for k, v in J.get('scalar', {}).items(): assert k in sn, k; ME.set_material_instance_scalar_parameter_value(m, k, v)
    for k, c in J.get('vector', {}).items(): assert k in vn, k; ME.set_material_instance_vector_parameter_value(m, k, u.LinearColor(c[0], c[1], c[2], 1))
    ME.update_material_instance(m); ok = EAL.save_loaded_asset(m, False)
    rb = {k: round(ME.get_material_instance_scalar_parameter_value(m, k), 3) for k in J.get('scalar', {})}
    rb.update({k: [round(x, 3) for x in (lambda c: (c.r, c.g, c.b))(ME.get_material_instance_vector_parameter_value(m, k))] for k in J.get('vector', {})})
    out[J['dst'].split('/')[-1]] = {'saved': ok, 'rb': rb}
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('G11RV_MI', json.dumps(out))
