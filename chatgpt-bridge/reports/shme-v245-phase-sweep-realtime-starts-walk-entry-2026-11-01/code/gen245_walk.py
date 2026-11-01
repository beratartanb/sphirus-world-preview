"""gen245_walk.py (editor job): V2.45 walk-character candidate = gen244_walk with the SAME METRIC THE GAME MEASURES: the in-game pelvis
yaw is the yaw of the hip line (thigh_r -> thigh_l joint positions) and the chest yaw the yaw of the clavicle line (gait242 / LTP vx_*);
V2.44 scaled the pelvis quaternion's Z-twist, which moved the hip line only 1 deg of 12 (in game 14.0 -> 13.8) while the chest fell
23 -> 19. Here every frame's HIP-LINE yaw excursion about its loop mean is scaled by hip_scale (rotation about world UP at the pelvis,
spine_01 compensated so the chest keeps its orientation), then the CLAVICLE-LINE yaw excursion is scaled by chest_scale (spine_01, neck
compensated so the head keeps its world yaw), legs re-solved to the ORIGINAL foot contacts (positions + orientations), ik_feet updated.
Modes: 'inplace' (in-memory vendor edit, A/B PRE only - never saved), 'out' (project copy, e.g. SHM245_Walk_Fwd), dry_run.
builtins.G245W = {src, hip_scale 0.65, chest_scale 0.55, inplace, out, dry_run}. Prints G245W {...}."""
import unreal as u, json, math, builtins, pathlib, sys, importlib
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'G245W', {})); DRY = bool(cfg.get('dry_run', False))
SRC = cfg.get('src', '/Game/GraceRanger/Animations/LocomotionBehavior/A_LB_Walk_Fwd'); OUT = cfg.get('out'); INPLACE = bool(cfg.get('inplace', False))
HS = float(cfg.get('hip_scale', 0.65)); CS = float(cfg.get('chest_scale', 0.55))
SD = P / 'Saved/Codex/SHME_V245_20261101'; SD.mkdir(parents=True, exist_ok=True)
seq = u.load_asset(SRC); assert seq, SRC
NAMES = [str(n) for n in AL.get_animation_track_names(seq)]; N = ae.num_frames(seq); T = float(seq.get_play_length())
L = ae.read_local(seq, NAMES, list(range(N))); local = {b: [L[b][f] for f in range(N)] for b in NAMES}
clip = ae.Clip(seq, ['root', 'pelvis', 'spine_01', 'spine_02', 'spine_03', 'spine_04', 'spine_05', 'neck_01', 'head', 'clavicle_l', 'clavicle_r', 'upperarm_l', 'upperarm_r',
                     'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r', 'thigh_l', 'thigh_r', 'calf_l', 'calf_r', 'foot_l', 'foot_r', 'ball_l', 'ball_r'] + [b for b in ('ik_foot_l', 'ik_foot_r', 'ik_foot_root') if b in NAMES])
UP = (0.0, 0.0, 1.0)
def yaw(a, b): return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
def wrap(a): return (a + 180.0) % 360.0 - 180.0
def cmean(a): return math.degrees(math.atan2(sum(math.sin(math.radians(x)) for x in a), sum(math.cos(math.radians(x)) for x in a)))
def hip_line(f): return yaw(clip.comp('thigh_r', f, local)[0], clip.comp('thigh_l', f, local)[0])
def clav_line(f): return yaw(clip.comp('clavicle_r', f, local)[0], clip.comp('clavicle_l', f, local)[0])
def head_yaw(f):
    q = clip.comp('head', f, local)[1]; v = ae.qrot(q, (1.0, 0.0, 0.0)); return math.degrees(math.atan2(v[1], v[0]))
FOOT = {s: [clip.comp('foot_' + s, f, local) for f in range(N)] for s in 'lr'}; KNEE = {s: [clip.comp('calf_' + s, f, local)[0] for f in range(N)] for s in 'lr'}
hip0 = [hip_line(f) for f in range(N)]; cla0 = [clav_line(f) for f in range(N)]; head0 = [head_yaw(f) for f in range(N)]
p2p = lambda a: round(max(a) - min(a), 2)
before = {'hip_line_p2p': p2p([wrap(h - hip0[0]) for h in hip0]), 'clav_line_p2p': p2p([wrap(c - cla0[0]) for c in cla0]), 'counter_p2p': p2p([wrap(c - h) for c, h in zip(cla0, hip0)])}
mh = cmean(hip0); dh = [wrap(h - mh) for h in hip0]
for f in range(N):
    d = -(1.0 - HS) * dh[f]
    ae.apply_bone_delta(clip, local, 'pelvis', f, ae.qaxis(UP, d)); ae.apply_bone_delta(clip, local, 'spine_01', f, ae.qaxis(UP, -d))
# second pass on the hip line (the pelvis delta is exact for a Z rotation; measure and correct any residual)
hip1 = [hip_line(f) for f in range(N)]; m1 = cmean(hip1); tgt = [mh + HS * x for x in dh]
for f in range(N):
    r = wrap(tgt[f] - hip1[f])
    if abs(r) > 0.05: ae.apply_bone_delta(clip, local, 'pelvis', f, ae.qaxis(UP, r)); ae.apply_bone_delta(clip, local, 'spine_01', f, ae.qaxis(UP, -r))
# chest: clavicle-line excursion scaled at spine_01, head world yaw kept
cla1 = [clav_line(f) for f in range(N)]; mc = cmean(cla1); dc = [wrap(c - mc) for c in cla1]
for f in range(N):
    d = -(1.0 - CS) * dc[f]
    if abs(d) > 1e-6:
        ae.apply_bone_delta(clip, local, 'spine_01', f, ae.qaxis(UP, d))
        if 'neck_01' in NAMES: ae.apply_bone_delta(clip, local, 'neck_01', f, ae.qaxis(UP, -d))
cla2 = [clav_line(f) for f in range(N)]; tgt_c = [mc + CS * x for x in dc]
for f in range(N):
    r = wrap(tgt_c[f] - cla2[f])
    if abs(r) > 0.05:
        ae.apply_bone_delta(clip, local, 'spine_01', f, ae.qaxis(UP, r))
        if 'neck_01' in NAMES: ae.apply_bone_delta(clip, local, 'neck_01', f, ae.qaxis(UP, -r))
for f in range(N):
    for s in 'lr': ae.solve_leg(clip, local, s, f, FOOT[s][f][0], FOOT[s][f][1], KNEE[s][f])
    if 'ik_foot_root' in NAMES:
        for s in 'lr':
            b = 'ik_foot_' + s
            if b in NAMES:
                fp, fq = clip.comp('foot_' + s, f, local); pp, pq = clip.comp('ik_foot_root', f, local)
                local[b][f] = (ae.qrot(ae.qinv(pq), ae.vsub(fp, pp)), ae.qnorm(ae.qmul(ae.qinv(pq), fq)), local[b][f][2])
hipA = [hip_line(f) for f in range(N)]; claA = [clav_line(f) for f in range(N)]; headA = [head_yaw(f) for f in range(N)]
ferr = max(ae.vlen(ae.vsub(clip.comp('foot_' + s, f, local)[0], FOOT[s][f][0])) for s in 'lr' for f in range(N))
after = {'hip_line_p2p': p2p([wrap(h - hipA[0]) for h in hipA]), 'clav_line_p2p': p2p([wrap(c - claA[0]) for c in claA]), 'counter_p2p': p2p([wrap(c - h) for c, h in zip(claA, hipA)]),
         'foot_err_max': round(ferr, 3), 'head_yaw_change_max': round(max(abs(wrap(a - b)) for a, b in zip(headA, head0)), 2)}
try:
    lm = ae.leg_metrics(seq, local, None, None); leg = {s: {'axis_jump_deg': round(lm[s]['axis_jump_deg'], 1), 'hinge_min': round(lm[s]['hinge_min'], 2), 'backward': lm[s]['backward_frames']} for s in 'lr'}
except Exception as ex: leg = {'err': str(ex)[:100]}
out = {'src': SRC, 'frames': N, 'len_s': round(T, 3), 'cfg': {k: cfg[k] for k in cfg}, 'before': before, 'after': after, 'leg': leg, 'mode': 'inplace' if INPLACE else ('out' if OUT else 'dry')}
def apply_to(target):
    ae.leg_guard(seq, local, label='SHM245_Walk')
    c = ae.controller(target)
    try: c.open_bracket(u.Text('SHME V2.45 walk candidate'), True)
    except Exception: c.open_bracket('SHME V2.45 walk candidate', True)
    try:
        for b in NAMES:
            ks = local[b]
            if not c.set_bone_track_keys(b, [u.Vector(*k[0]) for k in ks], [u.Quat(*k[1]) for k in ks], [u.Vector(*k[2]) for k in ks], True): raise RuntimeError('keys ' + b)
    finally: c.close_bracket(True)
if not DRY:
    if INPLACE: apply_to(seq); out['applied_in_memory'] = True
    elif OUT:
        tgt = u.load_asset(OUT) if EAL.does_asset_exist(OUT) else EAL.duplicate_asset(SRC, OUT); assert tgt
        for tr in [str(x) for x in AL.get_animation_notify_track_names(tgt)]:
            AL.remove_animation_notify_events_by_track(tgt, tr)
            try: AL.remove_animation_notify_track(tgt, tr)
            except Exception: pass
        apply_to(tgt); out['saved'] = EAL.save_loaded_asset(tgt, False); out['out'] = OUT
(SD / ('gen245_walk_%s.json' % out['mode'])).write_text(json.dumps(out, indent=1))
print('G245W ' + json.dumps(out))
