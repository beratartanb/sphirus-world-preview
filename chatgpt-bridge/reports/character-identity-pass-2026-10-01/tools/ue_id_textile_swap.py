"""IDENTITY pass: pattern-space textile textures for a NEW garment pattern (g15a) without touching the tuned final-art look:
import the PNGs as T_LK_*<suffix>, DUPLICATE the tuned MI_LK_*_v2 instances as MI_LK_*<suffix> (same parent / parameters) and swap
only their pattern textures (BaseColorTex / NormalTex / MaskTex; the tiled detail normal stays), then assign them to the new
garment meshes. builtins.ID_TEX = {'tex_dir': <abs>, 'suffix': '_g15a', 'meshes': {'Henley': path, 'Shorts': path}}"""
import unreal as u, builtins, json, os
C = builtins.ID_TEX; EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
D = '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Outfit'; TX, MD = D+'/Textures', D+'/Materials'; S = C['suffix']; out = {'tex': {}, 'mi': {}}
KIND = {'_BC': 'c', '_N': 'n', '_M': 'm'}
for base in ('T_LK_Henley', 'T_LK_HenleyTrim', 'T_LK_Shorts', 'T_LK_ShortsTrim'):
    for k, kind in KIND.items():
        nm = base+k; t = u.AssetImportTask(); t.set_editor_property('filename', os.path.join(C['tex_dir'], nm+'.png')); t.set_editor_property('destination_path', TX); t.set_editor_property('destination_name', nm+S)
        t.set_editor_property('automated', True); t.set_editor_property('save', False); t.set_editor_property('replace_existing', True); t.set_editor_property('factory', u.TextureFactory()); AT.import_asset_tasks([t])
        x = u.load_asset(TX+'/'+nm+S)
        if kind == 'n': x.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_NORMALMAP); x.set_editor_property('srgb', False)
        elif kind == 'm': x.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_MASKS); x.set_editor_property('srgb', False)
        else: x.set_editor_property('srgb', True)
        x.set_editor_property('never_stream', True); EAL.save_loaded_asset(x, False); out['tex'][nm+S] = [x.blueprint_get_size_x(), x.blueprint_get_size_y()]
MAP = {'MI_LK_Henley': 'T_LK_Henley', 'MI_LK_Henley_Trim': 'T_LK_HenleyTrim', 'MI_LK_Buttons': 'T_LK_HenleyTrim', 'MI_LK_Shorts': 'T_LK_Shorts', 'MI_LK_Shorts_Trim': 'T_LK_ShortsTrim', 'MI_LK_Drawstring': 'T_LK_ShortsTrim'}
for mi0, tb in MAP.items():
    src, dst = MD+'/'+mi0+'_v2', MD+'/'+mi0+S
    if not EAL.does_asset_exist(dst): assert EAL.duplicate_asset(src, dst)
    m = u.load_asset(dst)
    for pn, k in (('BaseColorTex', '_BC'), ('NormalTex', '_N'), ('MaskTex', '_M')): ME.set_material_instance_texture_parameter_value(m, pn, u.load_asset(TX+'/'+tb+k+S))
    ME.update_material_instance(m); EAL.save_loaded_asset(m, False); out['mi'][mi0+S] = m.get_editor_property('parent').get_name()
SLOTS = {'Henley': ['MI_LK_Henley', 'MI_LK_Henley_Trim', 'MI_LK_Buttons'], 'Shorts': ['MI_LK_Shorts', 'MI_LK_Shorts_Trim', 'MI_LK_Drawstring']}
for g, path in C['meshes'].items():
    mesh = u.load_asset(path); mats = mesh.get_editor_property('materials')
    for i, sm in enumerate(mats): sm.set_editor_property('material_interface', u.load_asset(MD+'/'+SLOTS[g][i]+S))
    mesh.set_editor_property('materials', mats); out[g] = [str(sm.get_editor_property('material_interface').get_name()) for sm in mesh.get_editor_property('materials')]; EAL.save_loaded_asset(mesh, False)
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('ID_TEX', json.dumps(out))
