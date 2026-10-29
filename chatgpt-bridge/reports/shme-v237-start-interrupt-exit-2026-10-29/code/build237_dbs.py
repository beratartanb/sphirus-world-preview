"""build237_dbs.py (editor job): V2.37 candidate databases = DUPLICATES of production databases (production assets untouched) + V2.37 clips
joined by a full-window BranchIn on a per-database notify track (a clip in two databases carries two tracks).
  start_L / start_R : PSD_SHM_JogStartS_L / _R (vendor start DBs, NOT the V2.36 copies) + SHM237_JogStart_F_L/Rfoot  (ABP SHM_JogStartDB_L / _R)
  resume            : PSD_CP2_JogStart (the CP start route = ABP SHM236_DB_JogResume) + both SHM237 starts (the search keeps the start after
                      the start family ends at StartTransferMaxTime) + the SHM237 re-push links (a re-press inside a jog stop)
builtins.V237_DB = {'dry': bool, 'groups': [...], 'repush': [clip paths]}. Prints DB237 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V237_DB', {})); DRY = bool(cfg.get('dry', True))
S = '/Game/GraceRanger/SHME/Animations/Starts/'; V = '/Game/GraceRanger/SHME/Animations/V237/'
ST = [V + 'SHM237_JogStart_F_Lfoot', V + 'SHM237_JogStart_F_Rfoot']
PLAN = {'start_L': (S + 'PSD_SHM_JogStartS_L', V + 'PSD_SHM237_JogStartS_L', [ST[0]]),
        'start_R': (S + 'PSD_SHM_JogStartS_R', V + 'PSD_SHM237_JogStartS_R', [ST[1]]),
        'resume': ('/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogStart', V + 'PSD_SHM237_JogResume', ST + list(cfg.get('repush', [])))}
out = {'dry': DRY}
for g in cfg.get('groups', list(PLAN)):
    src, dst, clips = PLAN[g]
    d = {'src_n': u.load_asset(src).get_num_animation_assets(), 'missing': [c for c in clips if not EAL.does_asset_exist(c)], 'dst_exists': EAL.does_asset_exist(dst)}
    if not DRY and not d['missing']:
        if not EAL.does_asset_exist(dst): assert EAL.duplicate_asset(src, dst), dst
        db = u.load_asset(dst); tr = 'SHME_V237_' + dst.split('/')[-1].replace('PSD_SHM237_', '')
        for c in clips:
            s = u.load_asset(c); names = [str(t) for t in L.get_animation_notify_track_names(s)]
            if tr in names: L.remove_animation_notify_events_by_track(s, tr); L.remove_animation_notify_track(s, tr)
            L.add_animation_notify_track(s, tr); ln = float(s.get_play_length())
            st = L.add_animation_notify_state_event(s, tr, 0.0, ln - 0.001, u.AnimNotifyState_PoseSearchBranchIn)
            st.set_editor_property('database', db); assert EAL.save_asset(c, False), c
        if 'bias' in cfg and g in cfg['bias']: db.set_editor_property('continuing_pose_cost_bias', float(cfg['bias'][g]))
        assert EAL.save_asset(dst, False)
        d['entries'] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
        d['bias'] = db.get_editor_property('continuing_pose_cost_bias')
    out[g] = d
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('DB237 ' + json.dumps(out, default=str))
