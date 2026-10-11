import builtins; builtins.LK_IMPORT = [{'file': r'C:\Users\berat\OneDrive\Documents\Unreal Projects\ActionAdventureMovementS\Saved\Codex\GD31_Identity_20261011\tex\T_GD31_Head_BC_n3.png', 'dest': '/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Looks/Textures', 'name': 'T_GD31_Head_BC_n3', 'srgb': True, 'vt': True}]
"""Import authored lookdev textures (PNG) into the lookdev folder. builtins.LK_IMPORT = [{'file', 'dest', 'name', 'srgb', 'normal', 'vt'}]"""
import unreal as u, builtins, json
AT = u.AssetToolsHelpers.get_asset_tools(); out = {}
for it in builtins.LK_IMPORT:
    t = u.AssetImportTask(); t.set_editor_property('filename', it['file']); t.set_editor_property('destination_path', it['dest']); t.set_editor_property('destination_name', it['name'])
    t.set_editor_property('automated', True); t.set_editor_property('save', False); t.set_editor_property('replace_existing', True); t.set_editor_property('factory', u.TextureFactory())
    AT.import_asset_tasks([t]); tex = u.load_asset(it['dest']+'/'+it['name'])
    if it.get('normal'): tex.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_NORMALMAP); tex.set_editor_property('srgb', False); tex.set_editor_property('flip_green_channel', bool(it.get('flip_green', False)))
    elif it.get('mask'): tex.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_MASKS); tex.set_editor_property('srgb', False)
    else: tex.set_editor_property('srgb', bool(it.get('srgb', True)))
    tex.set_editor_property('virtual_texture_streaming', bool(it.get('vt', False)))
    u.EditorAssetLibrary.save_loaded_asset(tex, False); out[it['name']] = [tex.blueprint_get_size_x(), tex.blueprint_get_size_y()]
print('IMPORTED', json.dumps(out))
