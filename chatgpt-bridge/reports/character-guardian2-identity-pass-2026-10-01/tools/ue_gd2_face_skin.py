"""GUARDIAN-2 pass: import Saved/Codex/CharacterGuardian2_20261001/skin/T_LK_Head_BC_<TG>.png (4K, VT) into the Guardian-2 Skin folder and
create face MIs MI_LK_Face_<LOD>_VT_g2<TG> as children of the GUARDIAN c14s MIs (every c14s setting - seam shading, tint - carries over)
swapping only 'Basecolor Baked VT'. The c14s MIs / textures are referenced, never modified. builtins.GD2_CTAG = 'c15'."""
import unreal as u, json, pathlib, builtins
TG = getattr(builtins, 'GD2_CTAG', 'c15')
P = pathlib.Path(u.Paths.project_dir()).resolve(); SK = P/'Saved/Codex/CharacterGuardian2_20261001/skin'; F = '/Game/Sphirus/CharacterLab/CharacterGuardian2_20261001/Skin'
GD = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Skin'; EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); out = {}
name = 'T_LK_Head_BC_'+TG
t = u.AssetImportTask(); t.set_editor_property('filename', str(SK/(name+'.png'))); t.set_editor_property('destination_path', F+'/Textures'); t.set_editor_property('destination_name', name)
t.set_editor_property('automated', True); t.set_editor_property('save', False); t.set_editor_property('replace_existing', True); t.set_editor_property('factory', u.TextureFactory())
AT.import_asset_tasks([t]); x = u.load_asset(F+'/Textures/'+name); x.set_editor_property('srgb', True); x.set_editor_property('virtual_texture_streaming', True)
EAL.save_loaded_asset(x, False); out[name] = [x.blueprint_get_size_x(), x.blueprint_get_size_y()]; slots = {}
for idx, n in (('0', 'LOD0'), ('9', 'LOD1'), ('10', 'LOD2'), ('12', 'LOD3'), ('13', 'LOD4'), ('14', 'LOD5to7')):
    if n == 'LOD5to7': par = u.load_asset(f'{GD}/MI_LK_Face_{n}_VT_c14s'); mn = f'MI_LK_Face_{n}_VT_g2{TG}'; dst = F+'/'+mn; m = u.load_asset(dst) if EAL.does_asset_exist(dst) else AT.create_asset(mn, F, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew()); ME.set_material_instance_parent(m, par); ME.update_material_instance(m); EAL.save_loaded_asset(m, False); slots[idx] = dst; out[mn] = 'parent BC kept (own LOD5-7 texture)'; continue
    par = u.load_asset(f'{GD}/MI_LK_Face_{n}_VT_c14s'); mn = f'MI_LK_Face_{n}_VT_g2{TG}'; dst = F+'/'+mn
    m = u.load_asset(dst) if EAL.does_asset_exist(dst) else AT.create_asset(mn, F, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
    ME.set_material_instance_parent(m, par); cur = ME.get_material_instance_texture_parameter_value(par, 'Basecolor Baked VT')
    ok = ME.set_material_instance_texture_parameter_value(m, 'Basecolor Baked VT', x); ME.update_material_instance(m); EAL.save_loaded_asset(m, False)
    slots[idx] = dst; out[mn] = {'parent': par.get_name(), 'bc_was': cur.get_name() if cur else None, 'set': ok}
(P/f'Saved/Codex/CharacterGuardian2_20261001/face_slots_g2{TG}.json').write_text(json.dumps(slots, indent=1))
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('GD2_SKIN', json.dumps(out))
