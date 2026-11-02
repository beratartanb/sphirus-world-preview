"""add248_turncurves.py (editor job; dry = measure, write = manifest of the six project turning-start copies): V2.48 clip-bound contract
curves on SHM_JogQ_af_Loco_Jog_Start_Turn{L,R}{090,135,180}_{L,R}foot_AAMS (project copies, only in PSD_SHM248_JogStartT_*).
Measured (v248tsreal j45_sl ts r2/r3): the turning start plays in place while the capsule accelerates on the CMC ramp (4 -> 113 cm/s in
0.6 s) and the pawn yaw slews 48 deg instead of 135 -> the planted foot drags 31-39 cm. The capsule must follow the clip's own root path:
  SHM226_V    = signed planar root speed along the root's current forward (cm/s; central difference at 30 Hz) -> V2.28 ClipSpeed
  SHM226_W    = 1 (blend-weight witness)
  SHM238_Turn = root yaw progress NORMALISED to 90 at the clip end (yaw(t)-yaw(0)) * 90 / (yaw(end)-yaw(0)) -> V2.38 Cmd = Yaw0 + Delta*T/90
                ends exactly at the REQUESTED heading whatever the clip's own turn (135 clip for a 138 request, 180 for 162)
  SHM238_W    = 1
builtins.V248_CURVES = {'dry': bool}. Prints TURNCURVES248 {...} (per clip: length, root distance, root yaw change, speed samples)."""
import unreal as u, json, builtins, math
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V248_CURVES', {})); DRY = bool(cfg.get('dry', True))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
J = '/Game/GraceRanger/SHME/Animations/Starts/Jog/'
CLIPS = [J + 'SHM_JogQ_af_Loco_Jog_Start_Turn%s%s_%sfoot_AAMS' % (s, d, s) for s in ('L', 'R') for d in ('090', '135', '180')]
DT = 1.0 / 30.0
out = {'dry': DRY, 'clips': {}, 'saved': 0}
def wrap(a): return (a + 180.0) % 360.0 - 180.0
for path in CLIPS:
    seq = u.load_asset(path); nm = path.rsplit('/', 1)[-1]
    if not seq: out['clips'][nm] = 'missing'; continue
    T = float(seq.get_play_length()); n = max(2, int(round(T / DT)))
    ts = [min(T, k * DT) for k in range(n + 1)]
    P = []; Y = []
    for t in ts:
        tr = AL.get_bone_pose_for_time(seq, 'root', t, False)
        P.append((float(tr.translation.x), float(tr.translation.y))); Y.append(float(tr.rotation.rotator().yaw))
    yaw_rel = [0.0]
    for k in range(1, n + 1): yaw_rel.append(yaw_rel[-1] + wrap(Y[k] - Y[k - 1]))
    total = yaw_rel[-1]
    vs = []
    for k in range(n + 1):
        a, b = max(0, k - 1), min(n, k + 1); dt = ts[b] - ts[a]
        vx, vy = (P[b][0] - P[a][0]) / dt, (P[b][1] - P[a][1]) / dt
        # forward of the root frame: the clips travel along +y in the clip frame at yaw 0 (project convention); rotate by the root yaw
        yr = math.radians(Y[k]); fx, fy = -math.sin(yr), math.cos(yr)
        sp = math.hypot(vx, vy); sgn = 1.0 if (vx * fx + vy * fy) >= 0 else -1.0
        vs.append(sgn * sp)
    dist = sum(math.hypot(P[k][0] - P[k - 1][0], P[k][1] - P[k - 1][1]) for k in range(1, n + 1))
    # v2: SIGNED progress (L clips -90, R clips +90 at the end): with Delta := |Delta| on the V2.48 rising edge (install248_turnbind3.py) the
    # capsule turns the way the CLIP turns - a 180 request has no sign of its own (v248tereal j45_sl2 ts r3: 85 cm slide on TurnL180)
    turn = [(yr_ * 90.0 / abs(total)) if abs(total) > 5.0 else 0.0 for yr_ in yaw_rel]
    d = {'len': round(T, 3), 'root_dist': round(dist, 1), 'root_yaw_total': round(total, 1), 'v_samples': [round(v) for v in vs[::max(1, n // 8)]], 'turn_samples': [round(x) for x in turn[::max(1, n // 8)]],
         'curves_before': [str(c) for c in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]}
    if not DRY:
        assert abs(total) > 5.0, (nm, 'no root yaw')
        for name, keys in (('SHM226_V', vs), ('SHM226_W', [1.0] * len(ts)), ('SHM238_Turn', turn), ('SHM238_W', [1.0] * len(ts))):
            if AL.does_curve_exist(seq, name, u.RawCurveTrackTypes.RCT_FLOAT): AL.remove_curve(seq, name, False)
            AL.add_curve(seq, name, u.RawCurveTrackTypes.RCT_FLOAT); AL.add_float_curve_keys(seq, name, ts, keys)
        assert EAL.save_asset(path, False), path; out['saved'] += 1
        d['curves_after'] = [str(c) for c in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]
    out['clips'][nm] = d
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('TURNCURVES248 ' + json.dumps(out, default=str))
