"""build236_stopdb.py (editor job): V2.36 candidate jog-stop database PSD_SHM236_JogStop (NEW asset) from the gen236_stop clips; schema /
biases copied from the production PSD_CP2_JogStop; each clip gets a full-window BranchIn (track SHME_V236_JogStop) - full windows
(entry-window trap). builtins.V236_DB = {'dry': bool, 'clips': [paths]}. Prints SDB236 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
c = dict(getattr(builtins, 'V236_DB', {})); DRY = bool(c.get('dry', True)); CLIPS = c.get('clips', [])
V = '/Game/GraceRanger/SHME/Animations/V236'; NAME = c.get('name', 'PSD_SHM236_JogStop'); path = V + '/' + NAME
seed = u.load_asset('/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogStop'); assert seed
out = {'dry': DRY, 'db': path, 'missing': [x for x in CLIPS if not EAL.does_asset_exist(x)]}
if not DRY and not out['missing']:
    if not EAL.does_asset_exist(path):
        f = u.DataAssetFactory(); f.set_editor_property('data_asset_class', u.PoseSearchDatabase)
        db = AT.create_asset(NAME, V, u.PoseSearchDatabase, f); assert db
        db.set_editor_property('schema', seed.get_editor_property('schema'))
        for k in ('base_cost_bias', 'continuing_pose_cost_bias', 'looping_cost_bias', 'normalization_set'):
            try: db.set_editor_property(k, seed.get_editor_property(k))
            except Exception as e: out.setdefault('prop_err', []).append([k, str(e)[:80]])
        assert EAL.save_asset(path, False)
    db = u.load_asset(path); tr = 'SHME_V236_JogStop'
    for x in CLIPS:
        s = u.load_asset(x); names = [str(t) for t in L.get_animation_notify_track_names(s)]
        if tr in names: L.remove_animation_notify_track(s, tr)
        L.add_animation_notify_track(s, tr); ln = float(s.get_play_length())
        st = L.add_animation_notify_state_event(s, tr, 0.0, ln, u.AnimNotifyState_PoseSearchBranchIn)
        st.set_editor_property('database', db); assert EAL.save_asset(x, False), x
    assert EAL.save_asset(path, False)
    out['entries'] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
    out['schema'] = str(db.get_editor_property('schema'))[-60:]
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('SDB236 ' + json.dumps(out, default=str))
