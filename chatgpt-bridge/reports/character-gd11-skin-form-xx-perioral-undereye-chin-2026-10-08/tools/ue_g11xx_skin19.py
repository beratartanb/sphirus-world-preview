"""pass XX: import T_LK_Head_BC_x19.png (4K, sRGB, VT; new asset, assert not existing) and create face MIs from the k18 MIs (k18 untouched):
gqx19 = BC x19 only; gqx19a = BC x19 + Fake AO Strength 0.4 (k18: 1.0)."""
import unreal as u, json, pathlib
P = pathlib.Path(u.Paths.project_dir()).resolve(); SRC = P/'Saved/Codex/GD11_SkinFormXX_20261008/skin/T_LK_Head_BC_x19.png'
D = '/Game/Sphirus/CharacterLab/GD11_FaceR_20261006/Skin'; EAL = u.EditorAssetLibrary; MEL = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); out = {}
tn = 'T_LK_Head_BC_x19'; tp = f'{D}/Textures/{tn}'; assert not EAL.does_asset_exist(tp), 'texture exists'
t = u.AssetImportTask(); t.set_editor_property('filename', str(SRC)); t.set_editor_property('destination_path', f'{D}/Textures'); t.set_editor_property('destination_name', tn)
t.set_editor_property('automated', True); t.set_editor_property('save', False); t.set_editor_property('replace_existing', False); t.set_editor_property('factory', u.TextureFactory())
AT.import_asset_tasks([t]); x = u.load_asset(tp); x.set_editor_property('srgb', True); x.set_editor_property('virtual_texture_streaming', True); out[tn] = [x.blueprint_get_size_x(), x.blueprint_get_size_y(), EAL.save_loaded_asset(x, False)]
for key, params in (('gqx19', {}), ('gqx19a', {'Fake AO Strength': 0.4})):
    for n in ('LOD0', 'LOD1', 'LOD2', 'LOD3', 'LOD4', 'LOD5to7'):
        dst = f'{D}/MI_LK_Face_{n}_VT_{key}'; assert not EAL.does_asset_exist(dst), dst
        m = EAL.duplicate_asset(f'{D}/MI_LK_Face_{n}_VT_gqk18', dst)
        ok = MEL.set_material_instance_texture_parameter_value(m, 'Basecolor Baked VT', x)
        for k, v in params.items(): MEL.set_material_instance_scalar_parameter_value(m, k, v)
        MEL.update_material_instance(m); out[dst] = [ok, EAL.save_loaded_asset(m, False)]
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('G11XX_SKIN19', json.dumps(out))
