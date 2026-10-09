"""GD16: import a CUSTOM eyebrow groom (gd16_brow.py Alembic, authored on the face bind pose -> no source mesh) into the GD16 folder, assign the
MI_Hair-based brow material, strand width / tip / shadow, no simulation, and create a GroomBinding to the given face (brow-tag specific name).
builtins.GD16_BROW = {'abc': abs path, 'tag': 'c1', 'face': face path, 'facetag': 'b3', 'width': 0.0055, 'shadow': 0.6, 'mi': MI path}"""
import unreal as u, json, builtins, re
C = builtins.GD16_BROW; G = '/Game/Sphirus/CharacterLab/GD16_IdentityMaster_20261010'; DST = G+'/Grooms'; BD = G+'/Face/Bindings'
EAL = u.EditorAssetLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); out = {'tag': C['tag']}; name = 'GR_GD16_BrowCustom_'+C['tag']
if not EAL.does_asset_exist(DST+'/'+name):
    t = u.AssetImportTask(); t.set_editor_property('filename', C['abc']); t.set_editor_property('destination_path', DST); t.set_editor_property('destination_name', name)
    t.set_editor_property('automated', True); t.set_editor_property('save', False); t.set_editor_property('replace_existing', False); t.set_editor_property('factory', u.HairStrandsFactory()); t.set_editor_property('options', u.GroomImportOptions())
    AT.import_asset_tasks([t])
g = u.load_asset(DST+'/'+name); assert g, 'brow import failed'
mi = u.load_asset(C['mi']); assert mi, 'brow MI missing'
m = u.HairGroupsMaterial(); m.set_editor_property('material', mi); m.set_editor_property('slot_name', 'Hair'); g.set_editor_property('hair_groups_materials', [m])
nr = []
for r in g.get_editor_property('hair_groups_rendering'):
    x = r.export_text().replace('MaterialSlotName=""', 'MaterialSlotName="Hair"'); x = re.sub(r'HairWidth=[0-9.]+', 'HairWidth=%f' % float(C.get('width', 0.0055)), x, 1).replace('HairWidth_Override=False', 'HairWidth_Override=True')
    x = re.sub(r'HairTipScale=[0-9.]+', 'HairTipScale=%f' % float(C.get('tip', 0.6)), x, 1); x = re.sub(r'HairShadowDensity=[0-9.]+', 'HairShadowDensity=%f' % float(C.get('shadow', 1.0)), x, 1)
    # 2026-10-10: like the MetaHuman library brows - stable rasterization keeps sub-pixel strands visible at normal viewing distance (else only the densest core renders as a thin line)
    x = x.replace('bUseStableRasterization=False', 'bUseStableRasterization=True'); x = re.sub(r'HairRaytracingRadiusScale=[0-9.]+', 'HairRaytracingRadiusScale=0.500000', x, 1); r.import_text(x); nr.append(r)
g.set_editor_property('hair_groups_rendering', nr)
npz = []
for q in g.get_editor_property('hair_groups_physics'): x = q.export_text().replace('EnableSimulation=True', 'EnableSimulation=False'); q.import_text(x); npz.append(q)
g.set_editor_property('hair_groups_physics', npz); EAL.save_loaded_asset(g, False); out['groom'] = g.get_path_name(); out['groups'] = len(nr)
path = f"{BD}/GB_GD16_EyebrowsCustom_{C['tag']}_{C['facetag']}"
assert path.startswith(G)
if EAL.does_asset_exist(path): EAL.delete_asset(path)
b = u.GroomLibrary.create_new_groom_binding_asset_with_path(path, g, u.load_asset(C['face']), 100, None, 0); assert b, path
EAL.save_loaded_asset(b, False); out['binding'] = b.get_path_name()
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('GD16_BROW', json.dumps(out))
