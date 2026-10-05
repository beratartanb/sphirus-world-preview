"""GD11 refinement O: import the PROCEDURAL eyebrow groom (brow_main.abc, authored in the face bind pose -> no source mesh) into the O candidate,
assign the GD eyebrow material, set strand width / shadow, no simulation, and create GroomBinding assets to the given face meshes.
builtins.G11RO_BROW = {'abc': <abs path>, 'tag': 'b1', 'faces': {'n1': '/Game/.../SKM_G11RN_Face_n1', ...}, 'width': 0.0045, 'shadow': 0.6, 'mi': '/Game/.../MI_GD_Eyebrows_Brown'}"""
import unreal as u, json, builtins, re
C = builtins.G11RO_BROW; DST = '/Game/Sphirus/CharacterLab/GD11_HeadRefinementO_20261005/Hair'; BD = '/Game/Sphirus/CharacterLab/GD11_HeadRefinementO_20261005/Face/Bindings'
EAL = u.EditorAssetLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); out = {'tag': C['tag']}; name = 'GR_O_Brow_'+C['tag']
t = u.AssetImportTask(); t.set_editor_property('filename', C['abc']); t.set_editor_property('destination_path', DST); t.set_editor_property('destination_name', name)
t.set_editor_property('automated', True); t.set_editor_property('save', False); t.set_editor_property('replace_existing', True); t.set_editor_property('factory', u.HairStrandsFactory()); t.set_editor_property('options', u.GroomImportOptions())
AT.import_asset_tasks([t]); g = u.load_asset(DST+'/'+name); assert g, 'brow import failed'
mi = u.load_asset(C.get('mi', '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Grooms/MI_GD_Eyebrows_Brown')); assert mi, 'brow MI missing'
m = u.HairGroupsMaterial(); m.set_editor_property('material', mi); m.set_editor_property('slot_name', 'Hair'); g.set_editor_property('hair_groups_materials', [m])
nr = []
for r in g.get_editor_property('hair_groups_rendering'):
    x = r.export_text().replace('MaterialSlotName=""', 'MaterialSlotName="Hair"'); x = re.sub(r'HairWidth=[0-9.]+', 'HairWidth=%f' % float(C.get('width', 0.0045)), x, 1).replace('HairWidth_Override=False', 'HairWidth_Override=True')
    x = re.sub(r'HairTipScale=[0-9.]+', 'HairTipScale=0.300000', x, 1); x = re.sub(r'HairShadowDensity=[0-9.]+', 'HairShadowDensity=%f' % float(C.get('shadow', 0.6)), x, 1); r.import_text(x); nr.append(r)
g.set_editor_property('hair_groups_rendering', nr)
npz = []
for q in g.get_editor_property('hair_groups_physics'): x = q.export_text().replace('EnableSimulation=True', 'EnableSimulation=False'); q.import_text(x); npz.append(q)
g.set_editor_property('hair_groups_physics', npz); EAL.save_loaded_asset(g, False); out['groom'] = g.get_path_name(); out['groups'] = len(nr)
out['bindings'] = {}
for suf, face in C['faces'].items():
    path = f'{BD}/GB_G11RO_EyebrowsCustom_{C["tag"]}_{suf}'   # brow-tag specific (b1/b2 bindings were overwriting each other)
    if EAL.does_asset_exist(path): EAL.delete_asset(path)
    b = u.GroomLibrary.create_new_groom_binding_asset_with_path(path, g, u.load_asset(face), 100, None, 0); assert b, path
    EAL.save_loaded_asset(b, False); out['bindings'][suf] = b.get_path_name()
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('G11RO_BROW', json.dumps(out))
