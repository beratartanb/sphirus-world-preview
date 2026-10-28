"""build236_startdbs.py (editor job): V2.36 candidate jog start databases = DUPLICATES of the production PSD_SHM_JogStartS_L / _R (same
entries, schema, biases; production assets untouched) + the V2.36 straight starts (gen236_start.py) joined by a full-window BranchIn
(track SHME_V236_JogStartS_<side>). A/B: abp_flags SHM_JogStartDB_L / _R -> the copies. builtins.V236_SDB = {'dry': bool}. Prints STDB236 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary
DRY = bool(dict(getattr(builtins, 'V236_SDB', {})).get('dry', True))
S = '/Game/GraceRanger/SHME/Animations/Starts/'; V = '/Game/GraceRanger/SHME/Animations/V236/'
PLAN = {'L': (S + 'PSD_SHM_JogStartS_L', V + 'PSD_SHM236_JogStartS_L', [V + 'SHM236_JogStart_F_Lfoot']),
        'R': (S + 'PSD_SHM_JogStartS_R', V + 'PSD_SHM236_JogStartS_R', [V + 'SHM236_JogStart_F_Rfoot'])}
out = {'dry': DRY}
for side, (src, dst, clips) in PLAN.items():
    d = {'src_n': u.load_asset(src).get_num_animation_assets(), 'missing': [c for c in clips if not EAL.does_asset_exist(c)]}
    if not DRY and not d['missing']:
        if not EAL.does_asset_exist(dst): assert EAL.duplicate_asset(src, dst), dst
        db = u.load_asset(dst); tr = 'SHME_V236_JogStartS_' + side
        for c in clips:
            s = u.load_asset(c); names = [str(t) for t in L.get_animation_notify_track_names(s)]
            if tr in names: L.remove_animation_notify_track(s, tr)
            L.add_animation_notify_track(s, tr); ln = float(s.get_play_length())
            st = L.add_animation_notify_state_event(s, tr, 0.0, ln - 0.001, u.AnimNotifyState_PoseSearchBranchIn)
            st.set_editor_property('database', db); assert EAL.save_asset(c, False), c
        assert EAL.save_asset(dst, False)
        d['entries'] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
    out[side] = d
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('STDB236 ' + json.dumps(out, default=str))
