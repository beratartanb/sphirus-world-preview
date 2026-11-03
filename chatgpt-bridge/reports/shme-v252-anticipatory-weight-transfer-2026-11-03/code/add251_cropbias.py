"""add251_cropbias.py (dry = measure job, write = manifest of the 6 crops): V2.51 keep Motion Matching on the turning-start crop until the turn
is done. Measured (v250d60 / v251a60 jstart -90 request, TurnR180_crop): at clip time 0.84 of 1.13 s, 6 deg before the turn ends, Motion
Matching left the crop for one frame of TurnR135_crop @0.83 and then SHM_JogQ_A_CP2_Jog_Fwd_Start @0.73 (all inside PSD_SHM248_JogStartT2_R):
three samples entered the blend stack in two frames -> shoulder 77 m/s2 / 1.64 cm in one 60 FPS frame (the yaw hand-over SHM251_YawSlew
removed the 6.4 deg capsule snap but not this pose pop). The database continuing-pose bias (-2.0) is not enough once the run-up trajectory
of the other clips matches better.
Patch: a PoseSearch 'Override Continuing Pose Cost Bias' notify state (track SHME_V251_Hold) from 0 to len - SHM251_TAIL (0.12 s) with
CostAddend (UI 'Modifier') = builtins V251_CB['bias'] (default -6). The release itself is unchanged: when the V2.49 owner ends (TurnDone) the database change
interrupts the continuing pose, so control response is not delayed. builtins.V251_CB = {'dry': bool, 'bias': float}. Prints CROPBIAS251 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V251_CB', {})); DRY = bool(cfg.get('dry', True)); BIAS = float(cfg.get('bias', -6.0)); TAIL = float(cfg.get('tail', 0.12))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
V = '/Game/GraceRanger/SHME/Animations/V248/'; TR = 'SHME_V251_Hold'
out = {'dry': DRY, 'bias': BIAS, 'clips': {}, 'saved': 0}
cls = getattr(u, 'AnimNotifyState_PoseSearchOverrideContinuingPoseCostBias', None); out['class'] = str(cls)
assert cls is not None, 'notify class missing'
for s in 'LR':
    for d in ('090', '135', '180'):
        p = V + 'SHM248_Jog_Start_Turn%s%s_crop' % (s, d); seq = u.load_asset(p); ln = seq.get_play_length()
        tracks = [str(t) for t in L.get_animation_notify_track_names(seq)]; rec = {'len': round(ln, 3), 'had_track': TR in tracks}
        if not DRY:
            if TR in tracks: L.remove_animation_notify_events_by_track(seq, TR)
            else: L.add_animation_notify_track(seq, TR)
            st = L.add_animation_notify_state_event(seq, TR, 0.0, max(0.1, ln - TAIL), cls)
            try: st.set_editor_property('cost_addend', BIAS)
            except Exception as e: rec['set_err'] = str(e)[:120]
            try: rec['cost_addend'] = float(st.get_editor_property('cost_addend'))
            except Exception as e: rec['get_err'] = str(e)[:80]
            assert EAL.save_asset(p, False), p; out['saved'] += 1
        out['clips'][p.split('/')[-1]] = rec
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('CROPBIAS251 ' + json.dumps(out, default=str))
