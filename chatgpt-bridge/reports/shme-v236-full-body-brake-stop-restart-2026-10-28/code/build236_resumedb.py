"""build236_resumedb.py (editor job): V2.36 candidate 'resume' database PSD_SHM236_JogResume = duplicate of PSD_CP2_JogStart (the vendor
start, same schema / biases) + the production jog loop A_CT_Jog_Fwd (full-window BranchIn, track SHME_V236_JogResume): a re-press while the
stop is still moving can continue the jog cadence from the current support instead of entering a start-from-rest mid-stride.
builtins.V236_RES = {'dry': bool}. Prints RESDB236 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary
DRY = bool(dict(getattr(builtins, 'V236_RES', {})).get('dry', True))
SRC = '/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogStart'; DST = '/Game/GraceRanger/SHME/Animations/V236/PSD_SHM236_JogResume'
CLIPS = ['/Game/GraceRanger/Animations/Continuity/A_CT_Jog_Fwd']
out = {'dry': DRY}
if not DRY:
    if not EAL.does_asset_exist(DST): assert EAL.duplicate_asset(SRC, DST)
    db = u.load_asset(DST); tr = 'SHME_V236_JogResume'
    for c in CLIPS:
        s = u.load_asset(c); names = [str(t) for t in L.get_animation_notify_track_names(s)]
        if tr in names: L.remove_animation_notify_track(s, tr)
        L.add_animation_notify_track(s, tr); ln = float(s.get_play_length())
        st = L.add_animation_notify_state_event(s, tr, 0.0, ln, u.AnimNotifyState_PoseSearchBranchIn); st.set_editor_property('database', db)
        assert EAL.save_asset(c, False), c
    assert EAL.save_asset(DST, False)
    out['entries'] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('RESDB236 ' + json.dumps(out, default=str))
