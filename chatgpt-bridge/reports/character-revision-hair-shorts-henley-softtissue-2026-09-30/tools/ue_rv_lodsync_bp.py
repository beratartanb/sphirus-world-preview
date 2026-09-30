"""Runtime LODSync pairing test with a single test actor: BP_RV_LODSyncTest (candidate folder only) = Face (Drive) + Body /
Henley / Shorts (Passive, explicit mappings) + LODSyncComponent. Spawned in the QA editor world; the face is stepped
through forced LODs and every component's predicted LOD is read back. Writes lodsync_check.json."""
import unreal as u, json, pathlib
O = pathlib.Path(u.Paths.project_dir()).resolve()/'Saved/Codex/CharacterRevision_20260930'; F = '/Game/Sphirus/CharacterLab/CharacterRevision_20260930'
EAL = u.EditorAssetLibrary; path = F+'/Test/BP_RV_LODSyncTest'
if EAL.does_asset_exist(path): EAL.delete_asset(path)
fac = u.BlueprintFactory(); fac.set_editor_property('parent_class', u.Actor)
bp = u.AssetToolsHelpers.get_asset_tools().create_asset('BP_RV_LODSyncTest', F+'/Test', u.Blueprint, fac)
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); root = sds.k2_gather_subobject_data_for_blueprint(bp)[0]
BFL = u.SubobjectDataBlueprintFunctionLibrary
def add(cls, name, parent):
    h, fail = sds.add_new_subobject(u.AddNewSubobjectParams(parent_handle=parent, new_class=cls, blueprint_context=bp))
    sds.rename_subobject(h, u.Text(name)); return h, BFL.get_object(BFL.get_data(h))
MESH = {'Body': F+'/Body/SKM_RV_BodyMesh', 'Face': F+'/Body/SKM_RV_FaceMesh', 'Henley': F+'/Outfit/SKM_RV_Henley', 'Shorts': F+'/Outfit/SKM_RV_Shorts'}
hb, body = add(u.SkeletalMeshComponent, 'Body', root); body.set_editor_property('skeletal_mesh_asset', u.load_asset(MESH['Body']))
for n in ('Face', 'Henley', 'Shorts'):
    h, c = add(u.SkeletalMeshComponent, n, hb); c.set_editor_property('skeletal_mesh_asset', u.load_asset(MESH[n]))
hl, ls = add(u.LODSyncComponent, 'LODSync', root)
syncs = []
for n, opt in (('Face', u.SyncOption.DRIVE), ('Body', u.SyncOption.PASSIVE), ('Henley', u.SyncOption.PASSIVE), ('Shorts', u.SyncOption.PASSIVE)):
    cs = u.ComponentSync(); cs.set_editor_property('name', n); cs.set_editor_property('sync_option', opt); syncs.append(cs)
ls.set_editor_property('components_to_sync', syncs); ls.set_editor_property('num_lods', 8)
MAP = {'Body': [0, 0, 1, 1, 2, 2, 3, 3], 'Henley': [0, 0, 1, 1, 2, 2, 2, 2], 'Shorts': [0, 0, 1, 1, 2, 2, 2, 2]}
cm = {}
for n, m in MAP.items():
    md = u.LODMappingData(); md.set_editor_property('mapping', m); cm[n] = md
ls.set_editor_property('custom_lod_mapping', cm)
u.BlueprintEditorLibrary.compile_blueprint(bp); EAL.save_loaded_asset(bp, False)
world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
a = u.get_editor_subsystem(u.EditorActorSubsystem).spawn_actor_from_object(bp, u.Vector(300, 0, 0))
comps = {c.get_name(): c for c in a.get_components_by_class(u.SkeletalMeshComponent)}
info = {'components': sorted(comps), 'mapping': MAP, 'rows': []}
face = comps.get('Face'); lsc = a.get_component_by_class(u.LODSyncComponent)
nat = {n: c.get_predicted_lod_level() for n, c in comps.items()}
for c in comps.values(): c.set_update_animation_in_editor(True)
st = {'k': 0, 'lod': 0}
def tick(dt):
    try:
        st['k'] += 1
        if st['k'] == 1: info['natural_before_forcing'] = {n: c.get_predicted_lod_level() for n, c in comps.items()}
        if st['k'] % 15 == 1: lsc.set_editor_property('forced_lod', st['lod'])
        if st['k'] % 15 == 14:
            row = {'lodsync_forced': st['lod']}
            for n, c in comps.items(): row[n] = c.get_predicted_lod_level()
            info['rows'].append(row); st['lod'] += 1
            if st['lod'] == 8:
                u.unregister_slate_post_tick_callback(hd); u.get_editor_subsystem(u.EditorActorSubsystem).destroy_actor(a)
                (O/'lodsync_check.json').write_text(json.dumps(info, indent=1, default=str))
    except Exception as e:
        u.unregister_slate_post_tick_callback(hd); info['error'] = repr(e); (O/'lodsync_check.json').write_text(json.dumps(info, indent=1, default=str))
hd = u.register_slate_post_tick_callback(tick); print('LODSYNC_BP_STARTED', sorted(comps))
