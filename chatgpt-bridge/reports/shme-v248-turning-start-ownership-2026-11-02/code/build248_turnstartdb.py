"""build248_turnstartdb.py (editor job; dry = measure job, build = write job with manifest = the project start clips that get a new BranchIn
track, --new the two databases). V2.48 TURNING-START databases: PSD_SHM248_JogStartT_L / _R = every entry of the production jog start
databases (ABP SHM_JogStartDB_L / _R = PSD_SHM237_JogStartS_L / _R) EXCEPT the backward starts (name contains 'Bwd'), joined by a
full-window PoseSearchBranchIn on the per-database track SHME_V248_T<side> (V2.37 method; a clip in two databases carries two tracks).
install248_turnstart.py searches them instead of the full start database when the request points BEHIND the body but NOT behind the look:
Motion Matching then has to take a turning start (af_Loco_Jog_Start_TurnL/R 135/180) instead of jogging backward (V2.46/47 real-time
j45_sl: af_Loco_Jog_Bwd_Start at body-relative 138-170 deg, 22-26 + 36-41 cm foot pivot). Only /Game/GraceRanger/SHME clips are
modified (a foreign entry aborts the build). builtins.V248_DB = {'dry': bool}. Prints DB248 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V248_DB', {})); DRY = bool(cfg.get('dry', True))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
V = '/Game/GraceRanger/SHME/Animations/V248/'
bp = u.load_asset(AP); cdo = u.get_default_object(bp.generated_class())
out = {'dry': DRY, 'sides': {}}
for side in ('L', 'R'):
    src = cdo.get_editor_property('SHM_JogStartDB_' + side); assert src, side
    sp = src.get_path_name().split('.')[0]; n = src.get_num_animation_assets()
    ents = [src.get_animation_asset(i) for i in range(n)]
    names = [e.get_name() for e in ents]; paths = [e.get_path_name().split('.')[0] for e in ents]
    keep = [(p, nm) for p, nm in zip(paths, names) if 'Bwd' not in nm]; drop = [nm for nm in names if 'Bwd' in nm]
    # the production start databases carry only the 045 turning starts: a request behind the body needs the 090 / 135 / 180 turning starts
    # (project copies SHM_JogQ_af_Loco_Jog_Start_Turn<side><deg>_<side>foot_AAMS, v139 copies of the AAMS starts, same skeleton) -> added here only
    # v2 (v248tereal j45_sl2 ts r1: StartSide R + a LEFT-behind request picked TurnR180 = the wrong way round): BOTH directions in each database,
    # Motion Matching chooses the turn direction from the trajectory, the stepping foot stays a secondary cost
    extra = list(cfg.get('extra') or ['/Game/GraceRanger/SHME/Animations/Starts/Jog/SHM_JogQ_af_Loco_Jog_Start_Turn%s%s_%sfoot_AAMS' % (sd, deg, sd) for sd in ('L', 'R') for deg in ('090', '135', '180')])   # v3: builtins override = the cropped turn clips
    extra = [e for e in extra if EAL.does_asset_exist(e) and e not in paths]
    keep += [(e, e.split('/')[-1]) for e in extra]
    foreign = [p for p, _ in keep if not p.startswith('/Game/GraceRanger/SHME/')]
    dst = V + 'PSD_SHM248_JogStartT%s_%s' % (cfg.get('suffix', ''), side)
    d = {'src': sp, 'n': n, 'drop': drop, 'extra': extra, 'keep': [p for p, _ in keep], 'foreign': foreign, 'dst': dst, 'dst_exists': EAL.does_asset_exist(dst)}
    if not DRY:
        assert not foreign, foreign; assert drop, 'no backward start in ' + sp; assert keep
        if not EAL.does_asset_exist(dst):
            fac = u.DataAssetFactory(); fac.set_editor_property('data_asset_class', u.PoseSearchDatabase)
            db = u.AssetToolsHelpers.get_asset_tools().create_asset(dst.rsplit('/', 1)[1], dst.rsplit('/', 1)[0], u.PoseSearchDatabase, fac); assert db, dst
        else: db = u.load_asset(dst)
        for k in ('schema', 'normalization_set', 'base_cost_bias', 'continuing_pose_cost_bias', 'looping_cost_bias', 'exclude_from_database_parameters', 'pose_search_mode', 'kdtree_max_leaf_size', 'kdtree_query_num_neighbors', 'skip_search_if_possible'):
            try: db.set_editor_property(k, src.get_editor_property(k))
            except Exception: d.setdefault('prop_skip', []).append(k)
        tr = 'SHME_V248_T' + side
        for p, nm in keep:
            s = u.load_asset(p); tn = [str(t) for t in L.get_animation_notify_track_names(s)]
            if tr in tn: L.remove_animation_notify_events_by_track(s, tr); L.remove_animation_notify_track(s, tr)
            L.add_animation_notify_track(s, tr); ln = float(s.get_play_length())
            st = L.add_animation_notify_state_event(s, tr, 0.0, ln - 0.001, u.AnimNotifyState_PoseSearchBranchIn)
            st.set_editor_property('database', db); assert EAL.save_asset(p, False), p
        assert EAL.save_asset(dst, False)
        db = u.load_asset(dst); d['entries'] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
        d['schema'] = str(db.get_editor_property('schema')).split('/')[-1][:60]
    out['sides'][side] = d
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('DB248 ' + json.dumps(out, default=str))
