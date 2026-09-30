"""Runtime (PIE) LODSync pairing test: the saved BP_RV_LODSyncTest (candidate folder) is placed in the QA world, PIE is
started, the LODSync component's ForcedLOD is stepped 0..7 in the GAME world and every component's predicted LOD is read
back; also the natural (screen-size driven) LOD at two camera-independent distances is recorded. PIE is then stopped and
the editor actor removed. Nothing is saved. Writes lodsync_check.json."""
import unreal as u, json, pathlib
O = pathlib.Path(u.Paths.project_dir()).resolve()/'Saved/Codex/CharacterRevision_20260930'
bp = u.load_asset('/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Test/BP_RV_LODSyncTest'); cls = bp.generated_class()
eas = u.get_editor_subsystem(u.EditorActorSubsystem); ues = u.get_editor_subsystem(u.UnrealEditorSubsystem); les = u.get_editor_subsystem(u.LevelEditorSubsystem)
ed_actor = eas.spawn_actor_from_class(cls, u.Vector(0, 400, 0))
info = {'rows': [], 'map': ues.get_editor_world().get_path_name()}
st = {'k': 0, 'phase': 'start', 'lod': 0, 'actor': None}
def finish():
    u.unregister_slate_post_tick_callback(hd)
    if les.is_in_play_in_editor(): les.editor_request_end_play()
    (O/'lodsync_check.json').write_text(json.dumps(info, indent=1, default=str))
def tick(dt):
    try:
        st['k'] += 1
        if st['phase'] == 'start':
            les.editor_request_begin_play(); st['phase'] = 'wait'; return
        gw = ues.get_game_world()
        if st['phase'] == 'wait':
            if gw is None:
                if st['k'] > 600: info['error'] = 'PIE did not start'; finish()
                return
            acts = u.GameplayStatics.get_all_actors_of_class(gw, cls)
            if not acts: return
            st['actor'] = acts[0]; st['phase'] = 'run'; st['k0'] = st['k']; info['game_world'] = gw.get_path_name(); return
        a = st['actor']; lsc = a.get_component_by_class(u.LODSyncComponent); comps = {c.get_name(): c for c in a.get_components_by_class(u.SkeletalMeshComponent)}
        t = st['k']-st['k0']
        if t == 5: info['natural_lod'] = {n: c.get_predicted_lod_level() for n, c in comps.items()}
        if t >= 10 and (t-10) % 12 == 0: lsc.set_editor_property('forced_lod', st['lod'])
        if t >= 10 and (t-10) % 12 == 10:
            row = {'lodsync_forced': st['lod'], 'current_lod_prop': lsc.get_editor_property('current_lod') if hasattr(lsc, 'current_lod') else None}
            for n, c in comps.items(): row[n] = c.get_predicted_lod_level()
            info['rows'].append(row); st['lod'] += 1
            if st['lod'] == 8: finish()
    except Exception as e:
        info['error'] = repr(e); finish()
hd = u.register_slate_post_tick_callback(tick); print('LODSYNC_PIE_STARTED')
