"""build255_db.py (editor job): V2.55 turn databases (NEW assets, names contain SHM254 so the V2.54 route hold owns them) from the gen255 clips; schema / biases
copied from the sprint reversal bridge. Each clip gets a full-window BranchIn. builtins.V255_DB = {'dbs': {name: [clip paths]}, 'bias': -25}. Prints DB255 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
c = dict(getattr(builtins, 'V255_DB', {})); V = c.get('dir', '/Game/GraceRanger/SHME/Animations/V255')
seed = u.load_asset(c.get('seed', '/Game/GraceRanger/SHME/Animations/Redirect/PSD_SHM_Redirect_SprintReversal')); assert seed
out = {}
for NAME, CLIPS in c.get('dbs', {}).items():
    path = V + '/' + NAME
    if not EAL.does_asset_exist(path):
        f = u.DataAssetFactory(); f.set_editor_property('data_asset_class', u.PoseSearchDatabase)
        db = AT.create_asset(NAME, V, u.PoseSearchDatabase, f); assert db
        db.set_editor_property('schema', seed.get_editor_property('schema'))
        for k in ('base_cost_bias', 'continuing_pose_cost_bias', 'looping_cost_bias', 'normalization_set'):
            try: db.set_editor_property(k, seed.get_editor_property(k))
            except Exception as e: out.setdefault('prop_err', []).append([k, str(e)[:80]])
        assert EAL.save_asset(path, False)
    db = u.load_asset(path); tr = 'SHME_V255_' + NAME[-6:]
    for x in CLIPS:
        s = u.load_asset(x); names = [str(t) for t in L.get_animation_notify_track_names(s)]
        if tr in names: L.remove_animation_notify_track(s, tr)
        L.add_animation_notify_track(s, tr); ln = float(s.get_play_length())
        st = L.add_animation_notify_state_event(s, tr, 0.0, ln, u.AnimNotifyState_PoseSearchBranchIn)
        st.set_editor_property('database', db); assert EAL.save_asset(x, False), x
    if 'bias' in c: db.set_editor_property('continuing_pose_cost_bias', float(c['bias']))
    assert EAL.save_asset(path, False)
    out[NAME] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('DB255 ' + json.dumps(out, default=str))
