"""IDENTITY pass: body skin MI with a replaced baked texture (e.g. the seam-blended normal map). builtins.ID_BMI = {'name', 'parent',
'textures': {param: png path}}; textures imported into the isolated Identity Skin folder (VT), parent MI referenced read-only."""
import unreal as u, builtins, json, pathlib
C = builtins.ID_BMI; EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); F = '/Game/Sphirus/CharacterLab/CharacterIdentity_20260930/Skin'; out = {}
m = u.load_asset(F+'/'+C['name']) if EAL.does_asset_exist(F+'/'+C['name']) else AT.create_asset(C['name'], F, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
ME.set_material_instance_parent(m, u.load_asset(C['parent']))
for pn, png in C['textures'].items():
    nm = pathlib.Path(png).stem; t = u.AssetImportTask(); t.set_editor_property('filename', png); t.set_editor_property('destination_path', F+'/Textures'); t.set_editor_property('destination_name', nm)
    t.set_editor_property('automated', True); t.set_editor_property('save', False); t.set_editor_property('replace_existing', True); t.set_editor_property('factory', u.TextureFactory()); AT.import_asset_tasks([t])
    x = u.load_asset(F+'/Textures/'+nm)
    if 'Normal' in pn: x.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_NORMALMAP); x.set_editor_property('srgb', False)
    x.set_editor_property('virtual_texture_streaming', True); EAL.save_loaded_asset(x, False); ME.set_material_instance_texture_parameter_value(m, pn, x); out[pn] = nm
ME.update_material_instance(m); out['saved'] = EAL.save_loaded_asset(m, False); out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('ID_BMI', json.dumps(out))
