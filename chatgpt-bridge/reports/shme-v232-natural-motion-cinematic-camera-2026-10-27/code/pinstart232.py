"""pinstart232.py (editor job) - V2.32 C: start-from-stand clips that begin from the character's OWN idle stance. The owned JogQ start clips
(AAMS starts) begin in another stance than the production idle (af_Stand_Idle_NaturalBaseline_Ph, the pose every start blends from): the
idle -> start blend moved both planted feet 82-145 cm/s for 0.1 s and the start's feet sat ~5 cm lower (j30_slow / jback / d_back 33-38 cm,
jstart 33-49 cm). Per clip and foot, in CLIP space (component space incl. the root track: a planted foot is still there):
  pinned phase  frame 0 -> the foot's first lift (ball rises LIFT_Z over its start level or moves LIFT_D horizontally): the BALL stays at
                the IDLE ball position (clip rotation kept -> turn starts pivot on the ball, no heel slide)
  hand-over     lift -> lift + HAND s (or the next landing): the pin offset fades (minimum-jerk) into the clip's own swing, so the first
                step lands where the clip puts it
The leg is solved with v137_animedit.solve_leg (bone lengths, knee hinge; leg_guard on write), ik_foot_* re-derived. Pelvis / trunk /
arms / root / curves untouched. builtins.PS232 = {'dry': True, 'clips': [...] (default: the owned JogQ starts), 'idle_t': 68.4,
'lift_z': 2.0, 'lift_d': 3.0, 'hand': 0.30}. Prints PS232 {...}: per clip and foot the stance offset idle -> start (cm), the planted drift
of the clip itself before its first lift, the lift time, and (write) the foot error after the solve."""
import unreal as u, json, math, builtins, pathlib, importlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary; AR = u.AssetRegistryHelpers.get_asset_registry()
cfg = getattr(builtins, 'PS232', {}); DRY = bool(cfg.get('dry', True))
IDLE = cfg.get('idle', '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/Phase275Support/Idle/af_Stand_Idle_NaturalBaseline_Phase275'); IDLE_T = float(cfg.get('idle_t', 68.4))
LIFT_Z = float(cfg.get('lift_z', 2.0)); LIFT_D = float(cfg.get('lift_d', 3.0)); HAND = float(cfg.get('hand', 0.30)); FPS = 30.0
clips = cfg.get('clips')
if not clips:
    clips = [str(a.package_name) for a in AR.get_assets_by_path('/Game/GraceRanger/SHME/Animations/Starts', recursive=True)
             if str(a.asset_class_path.asset_name) == 'AnimSequence' and str(a.asset_name).startswith('SHM_JogQ_')]
out = {'dry': DRY, 'cfg': {k: v for k, v in cfg.items() if k != 'clips'}, 'clips': {}}
BONES = ['ball_l', 'ball_r', 'foot_l', 'foot_r', 'calf_l', 'calf_r', 'thigh_l', 'thigh_r', 'pelvis', 'root']
# idle stance (component space, root at the origin): ball positions of the production idle at IDLE_T
ip = IDLE
if not EAL.does_asset_exist(ip):
    hits = [str(a.package_name) for a in AR.get_assets_by_path('/Game/GraceRanger', recursive=True) if str(a.asset_name) == 'af_Stand_Idle_NaturalBaseline_Ph']
    ip = hits[0] if hits else None
out['idle'] = ip
iseq = u.load_asset(ip); ic = ae.Clip(iseq, BONES)
fi = min(ic.nf - 1, int(round(IDLE_T * FPS)))
IB = {s: ic.comp('ball_' + s, fi)[0] for s in 'lr'}
out['idle_frame'] = fi
for path in clips:
    info = {}
    try:
        seq = u.load_asset(path)
        try: clip = ae.Clip(seq, BONES + ['ik_foot_l', 'ik_foot_r', 'ik_foot_root'])
        except Exception: clip = ae.Clip(seq, BONES)
        N = clip.nf; local = {b: list(v) for b, v in clip.local.items()}
        for s in 'lr':
            Bc = [clip.comp('ball_' + s, f)[0] for f in range(N)]
            b0 = Bc[0]; lift = None
            for f in range(1, N):
                if Bc[f][2] - b0[2] > LIFT_Z or math.hypot(Bc[f][0] - b0[0], Bc[f][1] - b0[1]) > LIFT_D: lift = f; break
            lift = lift if lift is not None else N - 1
            pre_drift = max(math.hypot(Bc[f][0] - b0[0], Bc[f][1] - b0[1]) for f in range(0, lift + 1))
            off = (IB[s][0] - b0[0], IB[s][1] - b0[1], IB[s][2] - b0[2])
            fh = min(N - 1, lift + int(round(HAND * FPS)))
            info[s] = {'stance_off': [round(x, 1) for x in off], 'stance_off_cm': round(math.sqrt(sum(x * x for x in off)), 1), 'pre_lift_drift': round(pre_drift, 1),
                       'lift_t': round(lift / FPS, 2), 'hand_end_t': round(fh / FPS, 2)}
            if DRY: continue
            err = 0.0
            for f in range(0, fh + 1):
                w = 1.0 if f <= lift else 1.0 - (lambda x: x * x * x * (10 - 15 * x + 6 * x * x))(min(1.0, (f - lift) / float(max(fh - lift, 1))))
                ball_t = (IB[s][0], IB[s][1], IB[s][2]) if f <= lift else Bc[f]
                tgt_ball = tuple(Bc[f][i] + (ball_t[i] - Bc[f][i]) * w for i in range(3)) if f > lift else (IB[s][0], IB[s][1], IB[s][2])
                if f > lift:   # hand-over: the pinned offset (idle ball - clip ball at the lift frame) fades into the clip's own swing
                    o_ = tuple(IB[s][i] - Bc[lift][i] for i in range(3)); tgt_ball = tuple(Bc[f][i] + o_[i] * w for i in range(3))
                fp, fq = clip.comp('foot_' + s, f, local); bp, _ = clip.comp('ball_' + s, f, local)
                foot_t = ae.vadd(tgt_ball, ae.vsub(fp, bp))   # keep the clip's own foot rotation and ball offset (pivot on the ball)
                kh = clip.comp('calf_' + s, f, local)[0]
                ae.solve_leg(clip, local, s, f, foot_t, fq, kh)
                err = max(err, ae.vlen(ae.vsub(clip.comp('ball_' + s, f, local)[0], tgt_ball)))
            info[s]['ball_err_after'] = round(err, 2)
        if not DRY:
            for s in ('l', 'r'):
                b = 'ik_foot_' + s
                if b in local and 'ik_foot_root' in local:
                    for f in range(N):
                        fp, fq = clip.comp('foot_' + s, f, local); pp, pq = clip.comp('ik_foot_root', f, local)
                        lt = ae.qrot(ae.qinv(pq), ae.vsub(fp, pp)); lq = ae.qnorm(ae.qmul(ae.qinv(pq), fq)); local[b][f] = (lt, lq, local[b][f][2])
            wb = [b for b in ('thigh_l', 'calf_l', 'foot_l', 'thigh_r', 'calf_r', 'foot_r', 'ik_foot_l', 'ik_foot_r') if b in local]
            ae.write_tracks(seq, local, wb, note='SHME V2.32 start from the idle stance')
            info['saved'] = bool(EAL.save_loaded_asset(seq, False))
    except Exception:
        import traceback; info = {'err': traceback.format_exc()[-700:]}
    out['clips'][path.rsplit('/', 1)[-1]] = info
(P / 'Saved/Codex/SHME_V232_20261027' / ('pinstart232_%s.json' % ('dry' if DRY else 'write'))).write_text(json.dumps(out, indent=1, default=str))
print('PS232 ' + json.dumps({'n': len(out['clips']), 'idle': out.get('idle'), 'err': [k for k, v in out['clips'].items() if 'err' in v]}, default=str))
