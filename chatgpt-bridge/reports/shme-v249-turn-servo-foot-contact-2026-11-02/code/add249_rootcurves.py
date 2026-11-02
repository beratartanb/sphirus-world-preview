"""add249_rootcurves.py (editor job, write manifest = the six cropped turn clips): ROOT POSITION curves for the V2.49 capsule servo.
  SHM249_RX = root displacement since frame 0 along the frame-0 root FORWARD (actor X; mesh +Y), cm
  SHM249_RY = root displacement since frame 0 along the frame-0 root RIGHT (actor Y; mesh -X), cm
(SHM241_SYaw = root yaw since frame 0 and SHM226_W = 1 are already on the crops.) Root motion settings untouched.
builtins.V249_RC = {'dry': bool}. Prints ROOTCURVES249 {...}."""
import unreal as u, json, builtins, math
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V249_RC', {})); DRY = bool(cfg.get('dry', True))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
V = '/Game/GraceRanger/SHME/Animations/V248/'; DT = 1.0 / 30.0
out = {'dry': DRY, 'clips': {}, 'saved': 0}
for s in ('L', 'R'):
    for d in ('090', '135', '180'):
        p = V + 'SHM248_Jog_Start_Turn%s%s_crop' % (s, d); seq = u.load_asset(p); assert seq, p
        T = float(seq.get_play_length()); n = int(round(T / DT)); ts = [min(T, k * DT) for k in range(n + 1)]
        P = []; Y = []
        for t in ts:
            tr = AL.get_bone_pose_for_time(seq, 'root', t, False); P.append((float(tr.translation.x), float(tr.translation.y))); Y.append(float(tr.rotation.rotator().yaw))
        y0 = math.radians(Y[0]); c, sn = math.cos(-y0), math.sin(-y0)
        fx = []; ry = []
        for (x, y) in P:
            dx, dy = x - P[0][0], y - P[0][1]; mx, my = dx * c - dy * sn, dx * sn + dy * c   # into the frame-0 root frame (mesh axes)
            fx.append(my); ry.append(-mx)                                                    # actor forward = mesh +Y, actor right = mesh -X
        out['clips'][p.split('/')[-1]] = {'n': n + 1, 'fwd_end': round(fx[-1], 1), 'right_end': round(ry[-1], 1), 'fwd_mid': round(fx[n // 2], 1), 'right_mid': round(ry[n // 2], 1)}
        if not DRY:
            for name, keys in (('SHM249_RX', fx), ('SHM249_RY', ry)):
                if AL.does_curve_exist(seq, name, u.RawCurveTrackTypes.RCT_FLOAT): AL.remove_curve(seq, name, False)
                AL.add_curve(seq, name, u.RawCurveTrackTypes.RCT_FLOAT); AL.add_float_curve_keys(seq, name, ts, keys)
            assert EAL.save_asset(p, False), p; out['saved'] += 1
            out['clips'][p.split('/')[-1]]['curves'] = [str(x) for x in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('ROOTCURVES249 ' + json.dumps(out, default=str))
