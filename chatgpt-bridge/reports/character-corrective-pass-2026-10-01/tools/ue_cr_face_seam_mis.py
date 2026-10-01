"""CORRECTIVE pass: face MIs '<tag>' = children of the c12 face MIs that swap only the seam-shading textures (SRMF + normal, from
blender_cr_seam_shading.py). Parents / source textures untouched. Writes face_slots_<tag>.json"""
import unreal as u, json, pathlib, builtins
TG = getattr(builtins, 'CR_SEAM_TAG', 'c12s'); SRC = getattr(builtins, 'CR_SEAM_SRC', 'c12')
P = pathlib.Path(u.Paths.project_dir()).resolve(); K = P/'Saved/Codex/CharacterCorrective_20261001'; SK = K/'skin'; F = '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Skin'
EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); out = {'tex': {}, 'mi': {}}; tex = {}
for name in ('T_LK_Head_SRMF_'+TG, 'T_LK_Head_N_'+TG):
    t = u.AssetImportTask(); t.set_editor_property('filename', str(SK/(name+'.png'))); t.set_editor_property('destination_path', F+'/Textures'); t.set_editor_property('destination_name', name)
    t.set_editor_property('automated', True); t.set_editor_property('save', False); t.set_editor_property('replace_existing', True); t.set_editor_property('factory', u.TextureFactory()); AT.import_asset_tasks([t])
    x = u.load_asset(F+'/Textures/'+name)
    if '_N_' in name: x.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_NORMALMAP)
    else: x.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_MASKS)
    x.set_editor_property('srgb', False); x.set_editor_property('virtual_texture_streaming', True); EAL.save_loaded_asset(x, False); tex[name] = x; out['tex'][name] = [x.blueprint_get_size_x(), x.blueprint_get_size_y()]
slots = json.loads((K/f'face_slots_{SRC}.json').read_text()); new = {}
for idx, path in slots.items():
    par = u.load_asset(path); name = par.get_name().replace('_'+SRC, '_'+TG); dst = F+'/'+name
    m = u.load_asset(dst) if EAL.does_asset_exist(dst) else AT.create_asset(name, F, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
    ME.set_material_instance_parent(m, par); rep = {}
    for pn, key, src in (('SRMF Baked VT', 'T_LK_Head_SRMF_'+TG, 'T_LK_Head_SRMF_v2'), ('Normal Baked VT', 'T_LK_Head_N_'+TG, 'T_LK_Head_N_'+SRC)):
        cur = ME.get_material_instance_texture_parameter_value(par, pn)
        if cur and cur.get_name() == src: ME.set_material_instance_texture_parameter_value(m, pn, tex[key]); rep[pn] = key
        else: rep[pn] = 'kept '+(cur.get_name() if cur else 'None')
    ME.update_material_instance(m); EAL.save_loaded_asset(m, False); new[idx] = m.get_path_name().split('.')[0]; out['mi'][name] = rep
(K/f'face_slots_{TG}.json').write_text(json.dumps(new, indent=1))
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('FACE_SEAM_MIS', json.dumps(out))
