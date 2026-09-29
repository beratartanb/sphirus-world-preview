import unreal as u, json
T = '/Game/Sphirus/CharacterLab/Outfit_Home_20260929/Textures'; out = {}
for n in ['T_Henley_BC', 'T_Henley_N', 'T_Henley_RA', 'T_Trousers_BC', 'T_Trousers_RA', 'T_Detail_Jersey_N']:
    t = u.load_asset(T+'/'+n)
    out[n] = {'srgb': t.get_editor_property('srgb'), 'comp': str(t.get_editor_property('compression_settings')), 'size': [t.blueprint_get_size_x(), t.blueprint_get_size_y()], 'lodgroup': str(t.get_editor_property('lod_group')), 'flip': str(t.get_editor_property('flip_green_channel')) if hasattr(t, 'flip_green_channel') else None}
    try: out[n]['source'] = str(t.get_editor_property('asset_import_data').get_first_filename())
    except Exception as e: out[n]['source'] = str(e)[:80]
mi = u.load_asset('/Game/Sphirus/CharacterLab/Outfit_Home_20260929/Materials/MI_Home_Henley')
out['MI_Henley_params'] = {p: str(u.MaterialEditingLibrary.get_material_instance_texture_parameter_value(mi, p)).split("'")[1] for p in ['BaseColorTex', 'NormalTex', 'RoughAOTex', 'DetailNormalTex']}
out['MI_Henley_tint'] = str(u.MaterialEditingLibrary.get_material_instance_vector_parameter_value(mi, 'Tint'))
print(json.dumps(out, indent=1))
