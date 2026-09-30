"""FACE-MATCH §5: import T_LK_Head_BC_c4 (4K) / T_LK_Head_N_c4 (1K) as virtual textures into the lookdev Skin folder and create
face MIs '_c4' (children of the c3 MIs: every c3 setting carries over) that swap only the base-colour / normal textures where the
c3 slot used the v2 ones. c3 MIs and all source textures untouched. Writes lk_face_slots_'+TG+'.json."""
import unreal as u, json, pathlib, builtins
TG = getattr(builtins, 'FM_CTAG', 'c4')
P = pathlib.Path(u.Paths.project_dir()).resolve(); SK = P/'Saved/Codex/CharacterFaceMatch_20260930/skin_c4'; F = '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Skin'
EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); out = {}; tex = {}
for name, kind in (('T_LK_Head_BC_'+TG, 'srgb'), ('T_LK_Head_N_'+TG, 'n')):
    t = u.AssetImportTask(); t.set_editor_property('filename', str(SK/(name+'.png'))); t.set_editor_property('destination_path', F+'/Textures'); t.set_editor_property('destination_name', name)
    t.set_editor_property('automated', True); t.set_editor_property('save', False); t.set_editor_property('replace_existing', True); t.set_editor_property('factory', u.TextureFactory())
    AT.import_asset_tasks([t]); x = u.load_asset(F+'/Textures/'+name)
    if kind == 'n': x.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_NORMALMAP); x.set_editor_property('srgb', False)
    else: x.set_editor_property('srgb', True)
    x.set_editor_property('virtual_texture_streaming', True); EAL.save_loaded_asset(x, False); tex[name] = x; out[name] = [x.blueprint_get_size_x(), x.blueprint_get_size_y()]
c3 = json.loads((P/'Saved/Codex/CharacterLookdev_20260930/lk_face_slots_c3.json').read_text()); slots = {}
for idx, path in c3.items():
    par = u.load_asset(path); name = par.get_name().replace('_c3', '_'+TG); dst = F+'/'+name
    m = u.load_asset(dst) if EAL.does_asset_exist(dst) else AT.create_asset(name, F, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
    ME.set_material_instance_parent(m, par); rep = {}
    for pn, key, src in (('Basecolor Baked VT', 'T_LK_Head_BC_'+TG, 'T_LK_Head_BC_v2'), ('Normal Baked VT', 'T_LK_Head_N_'+TG, 'T_LK_Head_N_v2')):
        cur = ME.get_material_instance_texture_parameter_value(par, pn)
        if cur and cur.get_name() == src: ME.set_material_instance_texture_parameter_value(m, pn, tex[key]); rep[pn] = key
    ME.update_material_instance(m); EAL.save_loaded_asset(m, False); slots[idx] = m.get_path_name().split('.')[0]; out[name] = rep
(P/('Saved/Codex/CharacterLookdev_20260930/lk_face_slots_'+TG+'.json')).write_text(json.dumps(slots, indent=1))
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('FACE_'+TG, json.dumps(out))
