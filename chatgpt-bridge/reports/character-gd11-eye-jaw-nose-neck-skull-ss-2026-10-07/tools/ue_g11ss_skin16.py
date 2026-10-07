"""GD11 pass SS: skin k16 = k15 (untouched) + subtle lived-in detail (regional baked-normal intensities only: forehead lines, crow's feet /
eyelids, nasolabial area, glabella). No tone, colour, pore or redness change. Static wrinkle-map weights are NOT used (the face ABP zeroes them)."""
import unreal as u, json
D = '/Game/Sphirus/CharacterLab/GD11_FaceR_20261006/Skin'; EAL = u.EditorAssetLibrary; MEL = u.MaterialEditingLibrary; out = {'before': {}, 'after': {}}
MUL = {'Intensity Forehead': 1.25, 'Intensity Glabellar': 1.15, 'Intensity Eyelids': 1.2, 'Intensity Maxilla': 1.3, 'Intensity Neutral': 1.1}
for n in ('LOD0', 'LOD1', 'LOD2', 'LOD3', 'LOD4', 'LOD5to7'):
    s, d = f'{D}/MI_LK_Face_{n}_VT_gqk15', f'{D}/MI_LK_Face_{n}_VT_gqk16'
    assert not EAL.does_asset_exist(d), 'k16 exists: ' + d
    m = EAL.duplicate_asset(s, d)
    for k, f in MUL.items():
        v = MEL.get_material_instance_scalar_parameter_value(m, k); MEL.set_material_instance_scalar_parameter_value(m, k, round(v*f, 4))
        if n == 'LOD0': out['before'][k] = v; out['after'][k] = round(v*f, 4)
    out[d] = EAL.save_loaded_asset(m, False)
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('SKIN_K16', json.dumps(out))
