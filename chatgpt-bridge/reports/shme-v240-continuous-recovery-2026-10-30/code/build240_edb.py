"""build240_edb.py (editor job): V2.40 per-(source, target) takeover ENTRY databases (NEW assets, one per target: PSD_SHM239_Tk_Back / _Opp) from gen239_tk clips;
schema / biases copied from the V2.38 cut database PSD_SHM238_JogCut (bias -25); each clip gets a full-window BranchIn on track
SHME_V239_<db name> (full windows = entry-window trap). builtins.V240_EDB = {dry, name, clips, bias}. Prints EDB240 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
c = dict(getattr(builtins, 'V240_EDB', {})); DRY = bool(c.get('dry', True)); CLIPS = c.get('clips', [])
V = c.get('dir', '/Game/GraceRanger/SHME/Animations/V240'); NAME = c['name']; path = V + '/' + NAME
seed = u.load_asset('' + c.get('seed', '/Game/GraceRanger/SHME/Animations/V238/PSD_SHM238_JogCut') + ''); assert seed
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
    db = u.load_asset(path); tr = 'SHME_V240_E'
    for x in CLIPS:
        s = u.load_asset(x); names = [str(t) for t in L.get_animation_notify_track_names(s)]
        if tr in names: L.remove_animation_notify_track(s, tr)
        L.add_animation_notify_track(s, tr); ln = float(s.get_play_length())
        en = min(ln, float(c.get('wins', {}).get(x, ln))); s0 = max(0.0, float(c.get('wstart', {}).get(x, 0.0)))   # V2.40: [t_(K-1), t_K + 0.05]
        st = L.add_animation_notify_state_event(s, tr, s0, en - s0, u.AnimNotifyState_PoseSearchBranchIn)
        st.set_editor_property('database', db); assert EAL.save_asset(x, False), x
    assert EAL.save_asset(path, False)
    out['entries'] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
    out['schema'] = str(db.get_editor_property('schema'))[-60:]
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('EDB240 ' + json.dumps(out, default=str))
if not DRY and 'bias' in c:
    db = u.load_asset(path); db.set_editor_property('continuing_pose_cost_bias', float(c['bias'])); print('EDB240_BIAS', db.get_editor_property('continuing_pose_cost_bias'), EAL.save_asset(path, False))
