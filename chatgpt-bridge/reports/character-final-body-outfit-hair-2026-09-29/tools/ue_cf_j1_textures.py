"""J1: import the authored textile textures with the legacy TextureFactory (no Interchange), set compression/sRGB."""
import unreal as u, pathlib, json
R = pathlib.Path(u.Paths.project_dir()).resolve(); T = R/'Saved/Codex/CharacterFinal_20260929/textures'
DEST = '/Game/Sphirus/CharacterLab/CharacterFinal_20260929/Outfit/Textures'
SPEC = {'T_Henley_BC': ('BC', True), 'T_Henley_N': ('N', False), 'T_Henley_RA': ('MASK', False), 'T_Shorts_BC': ('BC', True), 'T_Shorts_N': ('N', False), 'T_Shorts_RA': ('MASK', False), 'T_Detail_Jersey_N': ('N', False), 'T_Detail_Twill_N': ('N', False)}
tasks = []
for name in SPEC:
    t = u.AssetImportTask(); t.set_editor_property('filename', str(T/(name+'.png'))); t.set_editor_property('destination_path', DEST); t.set_editor_property('destination_name', name)
    t.set_editor_property('automated', True); t.set_editor_property('save', False); t.set_editor_property('replace_existing', True); t.set_editor_property('factory', u.TextureFactory())
    tasks.append(t)
u.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
out = {}
for name, (kind, srgb) in SPEC.items():
    tex = u.load_asset(f'{DEST}/{name}'); assert tex, name
    tex.set_editor_property('srgb', srgb)
    if kind == 'N': tex.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_NORMALMAP); tex.set_editor_property('lod_group', u.TextureGroup.TEXTUREGROUP_CHARACTER_NORMAL_MAP)
    elif kind == 'MASK': tex.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_MASKS); tex.set_editor_property('lod_group', u.TextureGroup.TEXTUREGROUP_CHARACTER_SPECULAR)
    else: tex.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_DEFAULT); tex.set_editor_property('lod_group', u.TextureGroup.TEXTUREGROUP_CHARACTER)
    if name.startswith('T_Detail'): tex.set_editor_property('lod_group', u.TextureGroup.TEXTUREGROUP_WORLD_NORMAL_MAP)
    ok = u.EditorAssetLibrary.save_loaded_asset(tex, False)
    out[name] = {'size': [tex.blueprint_get_size_x(), tex.blueprint_get_size_y()], 'srgb': tex.get_editor_property('srgb'), 'comp': str(tex.get_editor_property('compression_settings')), 'saved': ok}
print(json.dumps(out, indent=1))
