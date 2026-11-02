"""add248_turncrop.py (editor job, write manifest --new the six cropped clips; sources untouched): CROPPED turning-start clips.
Measured (v248tk60 / v248threal): the 2.3 s AAMS turning starts carry two run-up strides after the turn; Motion Matching keeps the
continuing pose to the clip end (1.2-1.9 s: 20-31 cm planted-foot drags under the clip-bound capsule), then picks ANOTHER start clip
(SHM237_JogStart_F @1.15) before a loop (30-47 cm hand-over slip). Route patches (post-turn loop search) cannot override the
continuing-pose preference. Fix at the content: SHM248_Jog_Start_Turn<L|R><deg>_crop = the project copy cut at the end of its turn
(+SHM248_CROP_TAIL s): the clip ENDS where the turn ends, Motion Matching must leave into a phase-matched run loop by its own cost.
Curves recomputed on the crop: SHM226_V / SHM226_VL / SHM226_W (clip-bound speed), SHM238_Turn (signed, 90 at the end) / SHM238_W,
SHM241_SYaw / SHM241_SW. Notify tracks removed (build248_turnstartdb.py v3 registers the crops in PSD_SHM248_JogStartT2_*).
builtins.V248_CROP = {'dry': bool, 'tail': 0.25}. Prints TURNCROP248 {...}."""
import unreal as u, json, builtins, math, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V248_CROP', {})); DRY = bool(cfg.get('dry', True)); TAIL = float(cfg.get('tail', 0.25))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
J = '/Game/GraceRanger/SHME/Animations/Starts/Jog/'; V = '/Game/GraceRanger/SHME/Animations/V248/'
DT = 1.0 / 30.0; out = {'dry': DRY, 'clips': {}, 'saved': 0}
def wrap(a): return (a + 180.0) % 360.0 - 180.0
for s in ('L', 'R'):
    for d in ('090', '135', '180'):
        srcp = J + 'SHM_JogQ_af_Loco_Jog_Start_Turn%s%s_%sfoot_AAMS' % (s, d, s); dst = V + 'SHM248_Jog_Start_Turn%s%s_crop' % (s, d)
        seq = u.load_asset(srcp); assert seq, srcp
        nf = ae.num_frames(seq); tracks = [str(t) for t in AL.get_animation_track_names(seq)]
        local = ae.read_local(seq, tracks, list(range(nf)))
        Y = []; P = []
        for f in range(nf):
            t_, q_, _ = local['root'][f]; P.append((t_[0], t_[1]))
            Y.append(u.Quat(q_[0], q_[1], q_[2], q_[3]).rotator().yaw)
        yr = [0.0]
        for f in range(1, nf): yr.append(yr[-1] + wrap(Y[f] - Y[f - 1]))
        total = yr[-1]; assert abs(total) > 60, (srcp, total)
        f_end = next(f for f in range(nf) if abs(yr[f]) >= 0.97 * abs(total))
        n = min(nf, f_end + 1 + int(round(TAIL / DT)))
        ts = [f * DT for f in range(n)]
        vs = []; vl = []
        for k in range(n):
            a, b = max(0, k - 1), min(n - 1, k + 1); dt = (b - a) * DT
            vx, vy = (P[b][0] - P[a][0]) / dt, (P[b][1] - P[a][1]) / dt
            r = math.radians(Y[k]); fx, fy = -math.sin(r), math.cos(r); rx, ry = -math.cos(r), -math.sin(r)
            sp = math.hypot(vx, vy); vs.append((1.0 if vx * fx + vy * fy >= 0 else -1.0) * sp); vl.append(vx * rx + vy * ry)
        turn = [yr[k] * 90.0 / abs(total) for k in range(n)]
        info = {'src_frames': nf, 'turn_end_frame': f_end, 'crop_frames': n, 'len': round((n - 1) * DT, 3), 'turn_end': round(turn[-1], 1), 'v_end': round(vs[-1]), 'tracks': len(tracks)}
        if not DRY:
            dup = u.load_asset(dst) if EAL.does_asset_exist(dst) else EAL.duplicate_asset(srcp, dst); assert dup, dst
            for tr in [str(t) for t in AL.get_animation_notify_track_names(dup)]:
                AL.remove_animation_notify_events_by_track(dup, tr)
                try: AL.remove_animation_notify_track(dup, tr)
                except Exception: pass
            c = ae.controller(dup)
            try: c.open_bracket(u.Text('SHME V2.48 turn crop'), True)
            except Exception: c.open_bracket('SHME V2.48 turn crop', True)
            try:
                c.set_number_of_frames(u.FrameNumber(n - 1), True)
                for b in tracks:
                    ks = local[b][:n]
                    if not c.set_bone_track_keys(b, [u.Vector(*k[0]) for k in ks], [u.Quat(k[1][0], k[1][1], k[1][2], k[1][3]) for k in ks], [u.Vector(*k[2]) for k in ks], True): raise RuntimeError('keys ' + b)
            finally: c.close_bracket(True)
            for cn in [str(x) for x in AL.get_animation_curve_names(dup, u.RawCurveTrackTypes.RCT_FLOAT)]: AL.remove_curve(dup, cn, False)
            for cn, vals in (('SHM226_V', vs), ('SHM226_VL', vl), ('SHM226_W', [1.0] * n), ('SHM238_Turn', turn), ('SHM238_W', [1.0] * n), ('SHM241_SYaw', yr[:n]), ('SHM241_SW', [1.0] * n)):
                AL.add_curve(dup, cn, u.RawCurveTrackTypes.RCT_FLOAT, False); AL.add_float_curve_keys(dup, cn, ts, vals)
            try: dup.set_editor_property('loop', False)
            except Exception: pass
            assert EAL.save_loaded_asset(dup, False), dst; out['saved'] += 1
            info['len_after'] = round(float(dup.get_play_length()), 3); info['curves'] = [str(x) for x in AL.get_animation_curve_names(dup, u.RawCurveTrackTypes.RCT_FLOAT)]
        out['clips'][dst.split('/')[-1]] = info
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('TURNCROP248 ' + json.dumps(out, default=str))
