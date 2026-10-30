"""build239_jctk.py (editor job) - V2.39 candidate database PSD_SHM239_JogCutTk = a copy of the production cut database PSD_SHM238_JogCut
(duplicate_asset keeps its 48 entries, schema, bias -25) + the PREFIX takeover clips (each gets a full-window BranchIn on track
SHME_V239_JogCutTk). In ONE database motion matching itself chooses: without a new intent the running cut's future matches the query and
continuing (bias -25) wins; with a new intent the identical frame of the takeover clip of this source (same pose, same past) whose future
heads to the new input wins, and the divergence happens inside that clip at the next planned touchdown. Production is untouched (the
candidate points SHM_RedirectDB_JL at the copy). builtins.V239_JCTK = {'dry': bool, 'clips': [...]}. Prints JCTK239 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary
c = dict(getattr(builtins, 'V239_JCTK', {})); DRY = bool(c.get('dry', True)); CLIPS = c.get('clips', [])
SRC = '/Game/GraceRanger/SHME/Animations/V238/PSD_SHM238_JogCut'; DST = '/Game/GraceRanger/SHME/Animations/V239/PSD_SHM239_JogCutTk'; TR = 'SHME_V239_JogCutTk'
out = {'dry': DRY, 'missing': [x for x in CLIPS if not EAL.does_asset_exist(x)]}
if not DRY and not out['missing']:
    db = u.load_asset(DST) if EAL.does_asset_exist(DST) else EAL.duplicate_asset(SRC, DST); assert db
    assert EAL.save_asset(DST, False)
    for x in CLIPS:
        s = u.load_asset(x); names = [str(t) for t in L.get_animation_notify_track_names(s)]
        if TR in names: L.remove_animation_notify_track(s, TR)
        L.add_animation_notify_track(s, TR); ln = float(s.get_play_length())
        st = L.add_animation_notify_state_event(s, TR, 0.0, ln, u.AnimNotifyState_PoseSearchBranchIn)
        st.set_editor_property('database', db); assert EAL.save_asset(x, False), x
    assert EAL.save_asset(DST, False)
    db = u.load_asset(DST); ent = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
    out['entries'] = len(ent); out['cut'] = sum(e.startswith('SHM238_Cut_') for e in ent); out['tk'] = sum(e.startswith('SHM239_Tk_') for e in ent)
    out['bias'] = db.get_editor_property('continuing_pose_cost_bias'); out['schema'] = db.get_editor_property('schema').get_name()
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('JCTK239 ' + json.dumps(out, default=str))
