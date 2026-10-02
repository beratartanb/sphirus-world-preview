"""GUARDIAN-4 Phase E skin: import Saved/Codex/CharacterGuardian5_20261002/skin/T_LK_Head_{BC,N,SRMF}_<tex>.png (virtual textures) into the
G4 Skin/Textures folder; face MIs MI_LK_Face_<LOD>_VT_g4<tag> = children of the GUARDIAN-2 g2c17 face MIs (all parent settings carry over)
swapping 'Basecolor Baked VT' / 'Normal Baked VT' / 'SRMF Baked VT' where the parent uses a head texture (LOD5to7 keeps its own), and the
SAME multiplicative 'Basecolor Global Multiply Post-Bake' factor on face and body MI_GD5_Body_<tag> (child of MI_GD_Body_t1) so the
head/body ratio at the seam is unchanged. Parents / sources are referenced, never modified.
builtins.GD5_SKIN = {'tag': 'k1', 'tex': 'k1', 'factor': [r, g, b], 'scalars': {name: value}, 'body_scalars': {...}}"""
import unreal as u, json, pathlib, builtins
C = builtins.GD5_SKIN; EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
P = pathlib.Path(u.Paths.project_dir()).resolve(); SK = P/'Saved/Codex/CharacterGuardian5_20261002/skin'
F = '/Game/Sphirus/CharacterLab/CharacterGuardian5_20261002/Skin'; G2 = '/Game/Sphirus/CharacterLab/CharacterGuardian2_20261001/Skin'; GD = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Skin'
PN = 'Basecolor Global Multiply Post-Bake'; f = C['factor']; TX = C.get('tex', C['tag']); out = {'tex': {}, 'mi': {}}; tex = {}
for kind in ('BC', 'N', 'SRMF'):
    name = f'T_LK_Head_{kind}_{TX}'; dst = F+'/Textures/'+name
    if EAL.does_asset_exist(dst): x = u.load_asset(dst)
    else:
        t = u.AssetImportTask(); t.set_editor_property('filename', str(SK/(name+'.png'))); t.set_editor_property('destination_path', F+'/Textures'); t.set_editor_property('destination_name', name)
        t.set_editor_property('automated', True); t.set_editor_property('save', False); t.set_editor_property('replace_existing', True); t.set_editor_property('factory', u.TextureFactory())
        AT.import_asset_tasks([t]); x = u.load_asset(dst)
        if kind == 'N': x.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_NORMALMAP); x.set_editor_property('srgb', False)
        elif kind == 'SRMF': x.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_MASKS); x.set_editor_property('srgb', False)
        else: x.set_editor_property('srgb', True)
        x.set_editor_property('virtual_texture_streaming', True); EAL.save_loaded_asset(x, False)
    tex[kind] = x; out['tex'][name] = [x.blueprint_get_size_x(), x.blueprint_get_size_y()]
def child(name, parent, swap):
    dst = F+'/'+name; m = u.load_asset(dst) if EAL.does_asset_exist(dst) else AT.create_asset(name, F, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
    ME.set_material_instance_parent(m, parent); rep = {}
    if swap:
        for pn, kind in (('Basecolor Baked VT', 'BC'), ('Normal Baked VT', 'N'), ('SRMF Baked VT', 'SRMF')):
            cur = ME.get_material_instance_texture_parameter_value(parent, pn)
            if cur and 'Head' in cur.get_name(): ME.set_material_instance_texture_parameter_value(m, pn, tex[kind]); rep[pn] = cur.get_name()+' -> '+tex[kind].get_name()
            else: rep[pn] = 'kept '+(cur.get_name() if cur else 'None')
    v = ME.get_material_instance_vector_parameter_value(parent, PN); ME.set_material_instance_vector_parameter_value(m, PN, u.LinearColor(v.r*f[0], v.g*f[1], v.b*f[2], v.a))
    for k, val in C.get('body_scalars' if not swap else 'scalars', {}).items():
        ME.set_material_instance_scalar_parameter_value(m, k, val)
    ME.update_material_instance(m); EAL.save_loaded_asset(m, False); r = ME.get_material_instance_vector_parameter_value(m, PN)
    out['mi'][name] = {'parent': parent.get_name(), 'swap': rep, 'tint_parent': [round(v.r, 3), round(v.g, 3), round(v.b, 3)], 'tint': [round(r.r, 3), round(r.g, 3), round(r.b, 3)]}
for n in ('LOD0', 'LOD1', 'LOD2', 'LOD3', 'LOD4', 'LOD5to7'):
    child(f"MI_LK_Face_{n}_VT_g5{C['tag']}", u.load_asset(f'{G2}/MI_LK_Face_{n}_VT_g2c17'), n != 'LOD5to7')
child(f"MI_GD5_Body_{C['tag']}", u.load_asset(f'{GD}/MI_GD_Body_t1'), False)
bm = u.load_asset(F+'/MI_GD5_Body_'+C['tag']); bsr = SK/f'T_LK_Body_SRMF_{TX}.png'
if bsr.exists():
    name = f'T_LK_Body_SRMF_{TX}'; dst = F+'/Textures/'+name
    if not EAL.does_asset_exist(dst):
        t = u.AssetImportTask(); t.set_editor_property('filename', str(bsr)); t.set_editor_property('destination_path', F+'/Textures'); t.set_editor_property('destination_name', name)
        t.set_editor_property('automated', True); t.set_editor_property('save', False); t.set_editor_property('replace_existing', True); t.set_editor_property('factory', u.TextureFactory()); AT.import_asset_tasks([t])
        x = u.load_asset(dst); x.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_MASKS); x.set_editor_property('srgb', False); x.set_editor_property('virtual_texture_streaming', True); EAL.save_loaded_asset(x, False)
    ME.set_material_instance_texture_parameter_value(bm, 'SRMF Baked VT', u.load_asset(dst)); out['body_srmf'] = name
for k, val in C.get('body_scalars', {}).items(): ME.set_material_instance_scalar_parameter_value(bm, k, val)
ME.update_material_instance(bm); EAL.save_loaded_asset(bm, False)
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('GD5_SKIN', json.dumps(out))
