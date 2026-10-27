"""stopfix232.py (editor job) - V2.32 D: closing-step clearance of the OWNED stop clips (walk / jog stops: the closing step slid along the
floor 27-33 cm in game, c30_calm SHM_M_Neutral_Walk_Stop_FR_Lfoot: the clip lifts the closing foot only 2-3 cm, the runtime pelvis settle
puts it under the floor band -> a dragged foot instead of a step).
Per clip, per foot, in CLIP space (component space incl. the root track = planted feet are still): swing segments = contiguous frames where
the ball moves horizontally > SPEED cm/s for >= MIN_TRAVEL cm in total; clearance = max ball height over the segment - the foot's planted
level (its 3rd lowest ball z). A segment with clearance < MIN_CLEAR gets a smooth bell lift on the FOOT target (sin^2 over the segment,
peak TARGET_CLEAR - clearance), the leg solved with v137_animedit.solve_leg (bone lengths, knee hinge kept; leg_guard on write), the
ik_foot_* bones re-derived from the new foot (gen226 rule). Upper body / root / timing / curves / notifies untouched.
builtins.SF232 = {'dry': True, 'clips': [...] (optional; default = scan of the owned stop clips), 'min_clear': 3.0, 'target_clear': 5.0,
'speed': 12.0, 'min_travel': 6.0, 'mode': 'bell' | 'minclear', 'min_ball': 2.5, 'd_off': 3.0, 'low_band': 2.0}. Dry = report only.
mode 'minclear' (V2.32 after the c30_calm isolation: the runtime layers do not own the drag; the clip's closing step starts with the ball
dipping 2.8 cm under its planted level and skimming 3 frames along the floor): the ball is kept MIN_BALL above its planted level from
D_OFF cm after the lift-off to D_OFF cm before the landing; 'low_travel' (cm covered within LOW_BAND of the planted level) before / after. Prints SF232 {...}."""
import unreal as u, json, math, builtins, pathlib, importlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary; AR = u.AssetRegistryHelpers.get_asset_registry()
cfg = getattr(builtins, 'SF232', {}); DRY = bool(cfg.get('dry', True))
MIN_CLEAR = float(cfg.get('min_clear', 3.0)); TARGET = float(cfg.get('target_clear', 5.0)); SPEED = float(cfg.get('speed', 12.0)); MIN_TRAVEL = float(cfg.get('min_travel', 6.0))
FPS = 30.0
MODE = cfg.get('mode', 'bell'); LOW_BAND = float(cfg.get('low_band', 2.0)); MIN_BALL = float(cfg.get('min_ball', 2.5)); D_OFF = float(cfg.get('d_off', 3.0))
clips = cfg.get('clips')
if not clips:
    clips = []
    for d in ('/Game/GraceRanger/SHME/Animations', '/Game/GraceRanger/Animations'):
        for a in AR.get_assets_by_path(d, recursive=True):
            n = str(a.asset_name)
            if str(a.asset_class_path.asset_name) == 'AnimSequence' and 'Stop' in n and (n.startswith('SHM_') or n.startswith('A_GR') or n.startswith('A_CT')):
                clips.append(str(a.package_name))
BONES = ['ball_l', 'ball_r', 'foot_l', 'foot_r', 'calf_l', 'calf_r', 'thigh_l', 'thigh_r', 'pelvis', 'root']
out = {'dry': DRY, 'cfg': {k: v for k, v in cfg.items() if k != 'clips'}, 'clips': {}}
for path in clips:
    info = {}
    try:
        seq = u.load_asset(path)
        try: clip = ae.Clip(seq, BONES + ['ik_foot_l', 'ik_foot_r', 'ik_foot_root'])
        except Exception: clip = ae.Clip(seq, BONES)
        N = clip.nf; local = {b: list(v) for b, v in clip.local.items()}
        segs_all = {}; changed = False
        for s in ('l', 'r'):
            B = [clip.comp('ball_' + s, f)[0] for f in range(N)]
            zs = sorted(b[2] for b in B); z0 = zs[min(2, len(zs) - 1)]
            mv = [False] + [math.hypot(B[f][0] - B[f - 1][0], B[f][1] - B[f - 1][1]) * FPS > SPEED for f in range(1, N)]
            segs = []; f = 1
            while f < N:
                if mv[f]:
                    g = f
                    while g + 1 < N and mv[g + 1]: g += 1
                    f0, f1 = max(f - 1, 0), min(g, N - 1)
                    trav = sum(math.hypot(B[k][0] - B[k - 1][0], B[k][1] - B[k - 1][1]) for k in range(f0 + 1, f1 + 1))
                    if trav >= MIN_TRAVEL:
                        clr = max(B[k][2] for k in range(f0, f1 + 1)) - z0
                        segs.append({'t0': round(f0 / FPS, 2), 't1': round(f1 / FPS, 2), 'travel': round(trav, 1), 'clear': round(clr, 1), 'f0': f0, 'f1': f1})
                    f = g + 1
                else: f += 1
            for sg in segs:
                f0, f1 = sg['f0'], sg['f1']
                # low travel: horizontal distance covered while the ball is within LOW_BAND of its planted level (a dragged toe / shuffle)
                def lowtrav(BB):
                    return sum(math.hypot(BB[k][0] - BB[k - 1][0], BB[k][1] - BB[k - 1][1]) for k in range(f0 + 1, f1 + 1) if BB[k][2] - z0 < LOW_BAND)
                sg['low_travel'] = round(lowtrav(B), 1)
                if MODE == 'minclear':
                    # required lift per frame: the ball at least MIN_BALL above its planted level once it left the plant by D_OFF cm and until
                    # D_OFF cm before the landing; smoothed (3-frame mean) so the lift ramps in and out
                    d0 = [math.hypot(B[k][0] - B[f0][0], B[k][1] - B[f0][1]) for k in range(N)]
                    d1 = [math.hypot(B[k][0] - B[f1][0], B[k][1] - B[f1][1]) for k in range(N)]
                    req = {k: max(0.0, MIN_BALL - (B[k][2] - z0)) if (d0[k] > D_OFF and d1[k] > D_OFF) else 0.0 for k in range(f0, f1 + 1)}
                    sm_ = {k: (req.get(k - 1, 0.0) + req[k] + req.get(k + 1, 0.0)) / 3.0 for k in req}
                    sm_ = {k: max(sm_[k], req[k] * 0.85) for k in sm_}
                    if max(sm_.values() or [0.0]) < 0.3: continue
                    sg['lift'] = round(max(sm_.values()), 1)
                    for k in range(f0 + 1, f1):
                        if sm_[k] <= 0.0: continue
                        ft, fq = clip.comp('foot_' + s, k, local); kh = clip.comp('calf_' + s, k, local)[0]
                        ae.solve_leg(clip, local, s, k, (ft[0], ft[1], ft[2] + sm_[k]), fq, kh)
                    B2 = [clip.comp('ball_' + s, f, local)[0] for f in range(N)]; sg['low_travel_after'] = round(lowtrav(B2), 1)
                    changed = True; continue
                if sg['clear'] >= MIN_CLEAR or sg['f1'] - sg['f0'] < 3: continue
                lift = TARGET - sg['clear']; sg['lift'] = round(lift, 1)
                for k in range(f0 + 1, f1):
                    w = math.sin(math.pi * (k - f0) / float(f1 - f0)) ** 2
                    ft, fq = clip.comp('foot_' + s, k, local)
                    kh = clip.comp('calf_' + s, k, local)[0]
                    ae.solve_leg(clip, local, s, k, (ft[0], ft[1], ft[2] + lift * w), fq, kh)
                changed = True
            segs_all[s] = [{k: v for k, v in sg.items() if k not in ('f0', 'f1')} for sg in segs]
        if changed:
            for s in ('l', 'r'):
                b = 'ik_foot_' + s
                if b in local and 'ik_foot_root' in local:
                    for f in range(N):
                        fp, fq = clip.comp('foot_' + s, f, local); pp, pq = clip.comp('ik_foot_root', f, local)
                        lt = ae.qrot(ae.qinv(pq), ae.vsub(fp, pp)); lq = ae.qnorm(ae.qmul(ae.qinv(pq), fq)); local[b][f] = (lt, lq, local[b][f][2])
        info = {'frames': N, 'segs': segs_all, 'changed': changed}
        if changed and not DRY:
            wb = [b for b in ('thigh_l', 'calf_l', 'foot_l', 'thigh_r', 'calf_r', 'foot_r', 'ik_foot_l', 'ik_foot_r') if b in local]
            ae.write_tracks(seq, local, wb, note='SHME V2.32 closing-step clearance')
            info['saved'] = bool(EAL.save_loaded_asset(seq, False))
    except Exception:
        import traceback; info = {'err': traceback.format_exc()[-700:]}
    out['clips'][path.rsplit('/', 1)[-1]] = info
(P / 'Saved/Codex/SHME_V232_20261027' / ('stopfix232_%s.json' % ('dry' if DRY else 'write'))).write_text(json.dumps(out, indent=1, default=str))
print('SF232 ' + json.dumps({'n': len(out['clips']), 'changed': [k for k, v in out['clips'].items() if v.get('changed')], 'err': [k for k, v in out['clips'].items() if 'err' in v]}, default=str))
