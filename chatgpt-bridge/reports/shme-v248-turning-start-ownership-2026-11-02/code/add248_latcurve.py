"""add248_latcurve.py (editor job, write manifest = the six project turning-start copies): LATERAL root speed curve for the V2.48 clip-bound
contract. Measured (authdrift248 vs contact231 v248tc60/tbreal): the authored planted foot of TurnL135 moves 0.0-0.4 cm in its first
0.43 s, in game it drifts 20-25 cm: the V2.28 contract writes Velocity = Forward * V only, the root of a turning start also moves
SIDEWAYS (root path (0,0) -> (22,-19) cm in 0.5 s while the body is still turning) and that lateral part was lost.
  SHM226_VL = root planar velocity projected on the root's RIGHT axis (mesh +Y forward, mesh -X right; cm/s, central difference 30 Hz)
Consumer: install248_latvel.py (component ClipSpeedLat -> BP_GR_Player Velocity = Forward * V + Right * VL). Existing curves untouched
(names may re-list lower-case: FName compare is case-insensitive). builtins.V248_LAT = {'dry': bool}. Prints LATCURVE248 {...}."""
import unreal as u, json, builtins, math
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V248_LAT', {})); DRY = bool(cfg.get('dry', True))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
J = '/Game/GraceRanger/SHME/Animations/Starts/Jog/'
CLIPS = [J + 'SHM_JogQ_af_Loco_Jog_Start_Turn%s%s_%sfoot_AAMS' % (s, d, s) for s in ('L', 'R') for d in ('090', '135', '180')]
DT = 1.0 / 30.0; out = {'dry': DRY, 'clips': {}, 'saved': 0}
for path in CLIPS:
    seq = u.load_asset(path); nm = path.rsplit('/', 1)[-1]
    T = float(seq.get_play_length()); n = max(2, int(round(T / DT))); ts = [min(T, k * DT) for k in range(n + 1)]
    P = []; Y = []
    for t in ts:
        tr = AL.get_bone_pose_for_time(seq, 'root', t, False); P.append((float(tr.translation.x), float(tr.translation.y))); Y.append(float(tr.rotation.rotator().yaw))
    vl = []
    for k in range(n + 1):
        a, b = max(0, k - 1), min(n, k + 1); dt = ts[b] - ts[a]
        vx, vy = (P[b][0] - P[a][0]) / dt, (P[b][1] - P[a][1]) / dt
        yr = math.radians(Y[k]); rx, ry = -math.cos(yr), -math.sin(yr)        # mesh right (-X at yaw 0) rotated by the root yaw
        vl.append(vx * rx + vy * ry)
    d = {'len': round(T, 3), 'vl_samples': [round(v) for v in vl[::max(1, n // 8)]]}
    if not DRY:
        for name, keys in (('SHM226_VL', vl),):
            if AL.does_curve_exist(seq, name, u.RawCurveTrackTypes.RCT_FLOAT): AL.remove_curve(seq, name, False)
            AL.add_curve(seq, name, u.RawCurveTrackTypes.RCT_FLOAT); AL.add_float_curve_keys(seq, name, ts, keys)
        assert EAL.save_asset(path, False), path; out['saved'] += 1
        d['curves_after'] = [str(c) for c in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]
    out['clips'][nm] = d
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('LATCURVE248 ' + json.dumps(out, default=str))
