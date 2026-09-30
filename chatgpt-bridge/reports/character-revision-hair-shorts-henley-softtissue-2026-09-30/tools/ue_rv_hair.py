"""RV hair: import the custom Alembic grooms (HairStrandsFactory, no conversion: the builder writes UE component-space cm),
auburn M_hair_v4 instances (strands / cards / helmet), strand width, simulation on the loose groom only, and GroomBindings
to the revision face mesh (authored on its bind pose -> no source mesh). Config: builtins.RV_HAIR = {'dir': <abs dir>, 'tag': 'v1'}"""
import unreal as u, pathlib, json, builtins
P = pathlib.Path(u.Paths.project_dir()).resolve(); S = P/'Saved/Codex/CharacterRevision_20260930'
CFG = getattr(builtins, 'RV_HAIR', {}); SRC = pathlib.Path(CFG['dir']); TAG = CFG.get('tag', 'v1')
DST = '/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Hair'; FACE = '/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Body/SKM_RV_FaceMesh'
EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); out = {'tag': TAG}
AUBURN = {'hairMelanin': float(CFG.get('melanin', 0.66)), 'hairRedness': float(CFG.get('redness', 0.86)), 'RedVariation': 0.18, 'MelaninVariationFine': 0.8, 'MelaninVariationRough': 0.5,
          'Desat': 0.08, 'RoughnessOverall': 0.62, 'HairRoughness': 0.47, 'Roughness': 0.68, 'Scraggle': 0.25, 'Spec0': 0.35, 'Spec1': 0.55, 'LightAmount': 0.3}
def mi(name, parent):
    path = DST+'/'+name
    m = u.load_asset(path) if EAL.does_asset_exist(path) else AT.create_asset(name, DST, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
    ME.set_material_instance_parent(m, u.load_asset(parent))
    for k, v in AUBURN.items(): ME.set_material_instance_scalar_parameter_value(m, k, v)
    EAL.save_loaded_asset(m, False); return m
MI_STRANDS = mi('MI_RV_Hair_Auburn', '/MetaHumanCharacter/Materials/MI_Hair')
def import_groom(abc, name):
    t = u.AssetImportTask(); t.set_editor_property('filename', str(abc)); t.set_editor_property('destination_path', DST); t.set_editor_property('destination_name', name)
    t.set_editor_property('automated', True); t.set_editor_property('save', False); t.set_editor_property('replace_existing', True); t.set_editor_property('factory', u.HairStrandsFactory())
    t.set_editor_property('options', u.GroomImportOptions())
    AT.import_asset_tasks([t]); g = u.load_asset(DST+'/'+name); assert g, ('groom import failed', abc); return g
def setup(g, width, simulate):
    mats = []
    m = u.HairGroupsMaterial(); m.set_editor_property('material', MI_STRANDS); m.set_editor_property('slot_name', 'Hair'); mats.append(m)
    g.set_editor_property('hair_groups_materials', mats)
    import re as _re
    rend = g.get_editor_property('hair_groups_rendering'); nr = []
    for r in rend:
        t = r.export_text(); t = t.replace('MaterialSlotName=""', 'MaterialSlotName="Hair"')
        t = _re.sub(r'HairWidth=[0-9.]+', 'HairWidth=%f' % width, t, 1).replace('HairWidth_Override=False', 'HairWidth_Override=True')
        t = _re.sub(r'HairTipScale=[0-9.]+', 'HairTipScale=0.450000', t, 1); r.import_text(t); nr.append(r)
    g.set_editor_property('hair_groups_rendering', nr)
    phys = g.get_editor_property('hair_groups_physics'); npz = []
    for q in phys:
        t = q.export_text().replace('EnableSimulation=False', 'EnableSimulation=%s' % ('True' if simulate else 'False'))
        if simulate:
            t = _re.sub(r'BendStiffness=[0-9.]+', 'BendStiffness=0.050000', t, 1); t = _re.sub(r'BendDamping=[0-9.]+', 'BendDamping=0.020000', t, 1)
            t = _re.sub(r'AirDrag=[0-9.]+', 'AirDrag=0.150000', t, 1); t = _re.sub(r'SubSteps=[0-9]+', 'SubSteps=3', t, 1)
        q.import_text(t); npz.append(q)
    g.set_editor_property('hair_groups_physics', npz)
    try: g.set_editor_property('enable_simulation_cache', False)
    except Exception: pass
    EAL.save_loaded_asset(g, False)
def bind(g, name):
    path = DST+'/'+name
    if EAL.does_asset_exist(path): EAL.delete_asset(path)
    b = u.GroomLibrary.create_new_groom_binding_asset_with_path(path, g, u.load_asset(FACE), 100, None, 0); assert b, name
    EAL.save_loaded_asset(b, False); return b.get_path_name()
g_main = import_groom(SRC/'hair_main.abc', f'GR_RV_Hair_Main_{TAG}'); setup(g_main, float(CFG.get('width_main', 0.0065)), False)
g_loose = import_groom(SRC/'hair_loose.abc', f'GR_RV_Hair_Loose_{TAG}'); setup(g_loose, float(CFG.get('width_loose', 0.0055)), False)   # simulation is enabled later (ue_rv_hair_sim.py) once the groom data is built
out['main'] = g_main.get_path_name(); out['loose'] = g_loose.get_path_name()
out['bind_main'] = bind(g_main, f'GR_RV_Hair_Main_{TAG}_Binding'); out['bind_loose'] = bind(g_loose, f'GR_RV_Hair_Loose_{TAG}_Binding')
out['groups'] = {'main': len(g_main.get_editor_property('hair_groups_rendering')), 'loose': len(g_loose.get_editor_property('hair_groups_rendering'))}
out['loose_sim'] = [p.get_editor_property('solver_settings').get_editor_property('enable_simulation') for p in g_loose.get_editor_property('hair_groups_physics')]
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(S/f'rv_hair_{TAG}.json').write_text(json.dumps(out, indent=1, default=str)); print(json.dumps(out, indent=1, default=str))
