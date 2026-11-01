"""build245_walkdb.py (editor job, write manifest): V2.45 project walk-loop database PSD_SHM245_WalkLoops = project COPIES of the 8 vendor
A_LB_Walk_* loops (SHM245_LB_Walk_<dir>, duplicate_asset; the vendor clips are not touched) with the forward loop replaced by the
gen245_walk candidate SHM245_Walk_Fwd; schema / biases copied from the project PSD_LB_WalkLoops; full-window BranchIn (track
SHME_V245_Walk). builtins.V245_WDB = {'dry': bool, 'fwd': path of the candidate forward loop}. Prints WDB245 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
c = dict(getattr(builtins, 'V245_WDB', {})); DRY = bool(c.get('dry', True)); FWD = c.get('fwd', '/Game/GraceRanger/SHME/Animations/V245/SHM245_Walk_Fwd')
V = '/Game/GraceRanger/SHME/Animations/V245'; NAME = c.get('name', 'PSD_SHM245_WalkLoops'); path = V + '/' + NAME
SRC = '/Game/GraceRanger/Animations/LocomotionBehavior/'; DIRS = ['FwdLeft', 'Left', 'BwdLeft', 'Bwd', 'BwdRight', 'Right', 'FwdRight']
seed = u.load_asset('/Game/GraceRanger/Animations/LocomotionBehavior/PSD_LB_WalkLoops'); assert seed
out = {'dry': DRY, 'db': path, 'copies': []}
clips = []
for d in DIRS:
    s = SRC + 'A_LB_Walk_' + d; t = V + '/SHM245_LB_Walk_' + d
    if not DRY and not EAL.does_asset_exist(t): assert EAL.duplicate_asset(s, t), t; out['copies'].append(d)
    clips.append(t)
assert EAL.does_asset_exist(FWD) or DRY, FWD; clips.append(FWD)
out['clips'] = clips; out['missing'] = [x for x in clips if not EAL.does_asset_exist(x)]
if not DRY and not out['missing']:
    if not EAL.does_asset_exist(path):
        f = u.DataAssetFactory(); f.set_editor_property('data_asset_class', u.PoseSearchDatabase)
        db = AT.create_asset(NAME, V, u.PoseSearchDatabase, f); assert db
        db.set_editor_property('schema', seed.get_editor_property('schema'))
        for k in ('base_cost_bias', 'continuing_pose_cost_bias', 'looping_cost_bias', 'normalization_set'):
            try: db.set_editor_property(k, seed.get_editor_property(k))
            except Exception as e: out.setdefault('prop_err', []).append([k, str(e)[:80]])
        assert EAL.save_asset(path, False)
    db = u.load_asset(path); tr = 'SHME_V245_Walk'
    for x in clips:
        s = u.load_asset(x); names = [str(t) for t in L.get_animation_notify_track_names(s)]
        if tr in names: L.remove_animation_notify_track(s, tr)
        L.add_animation_notify_track(s, tr); ln = float(s.get_play_length())
        st = L.add_animation_notify_state_event(s, tr, 0.0, ln, u.AnimNotifyState_PoseSearchBranchIn); st.set_editor_property('database', db)
        try: s.set_editor_property('loop', True)   # the loops must loop (the seed DB entries are looping walk cycles)
        except Exception: pass
        assert EAL.save_asset(x, False), x
    assert EAL.save_asset(path, False)
    out['entries'] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('WDB245 ' + json.dumps(out, default=str))
