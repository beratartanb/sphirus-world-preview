"""build238_cutdb.py (editor job): V2.38 jog 90 cut database PSD_SHM238_JogCut (NEW asset) from the gen238_cut clips; schema / biases
copied from the bridge it replaces in the jog-lateral route (PSD_SHM_Redirect_JogLateral, the ABP SHM_RedirectDB_JL default); each clip gets a
full-window BranchIn (track SHME_V238_JogCut; full windows = entry-window trap). builtins.V238_CDB = {dry, clips, bias}. Prints CDB238 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
c = dict(getattr(builtins, 'V238_CDB', {})); DRY = bool(c.get('dry', True)); CLIPS = c.get('clips', [])
V = '/Game/GraceRanger/SHME/Animations/V238'; NAME = c.get('name', 'PSD_SHM238_JogCut'); path = V + '/' + NAME
seed = u.load_asset('' + c.get('seed', '/Game/GraceRanger/SHME/Animations/Redirect/PSD_SHM_Redirect_JogLateral') + ''); assert seed
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
    db = u.load_asset(path); tr = 'SHME_V238_JogCut'
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
print('CDB238 ' + json.dumps(out, default=str))
if not DRY and 'bias' in c:
    db = u.load_asset(path); db.set_editor_property('continuing_pose_cost_bias', float(c['bias'])); print('CDB238_BIAS', db.get_editor_property('continuing_pose_cost_bias'), EAL.save_asset(path, False))
