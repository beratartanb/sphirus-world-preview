"""gen244_walk.py (editor job): V2.44 walk-character candidate = the production forward walk loop (vendor A_LB_Walk_Fwd, the clip whose
content owns the 23 deg pelvis-chest counter-rotation measured in game, V2.43) with the PELVIS YAW EXCURSION scaled about its loop mean
(yaw_scale, default 0.65 -> ~15 deg counter-rotation, the human range at 1.3 m/s) while the chest keeps its original world orientation
(spine_01 receives the removed rotation back) and the legs are re-solved to the ORIGINAL foot contacts (same foot positions and orientations
every frame -> cadence, step length, heel/toe timing, arm swing unchanged). Optional arm_scale (upper-arm swing about the lateral axis,
default 1.0 = untouched) and lean_deg (extra forward trunk lean, default 0).
Modes: 'inplace': True edits the loaded vendor asset IN MEMORY ONLY (A/B PRE job; never saved - the vendor clip stays as shipped);
       'out': path writes a project copy (SHM244_Walk_Fwd) for captures / a future database entry.
builtins.G244W = {src, yaw_scale, arm_scale, lean_deg, inplace, out, dry_run}. Prints G244W {...}."""
import unreal as u, json, math, builtins, pathlib, sys, importlib
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'G244W', {})); DRY = bool(cfg.get('dry_run', False))
SRC = cfg.get('src', '/Game/GraceRanger/Animations/LocomotionBehavior/A_LB_Walk_Fwd'); OUT = cfg.get('out'); INPLACE = bool(cfg.get('inplace', False))
S = float(cfg.get('yaw_scale', 0.65)); SC = float(cfg.get('chest_scale', 0.55)); ARM = float(cfg.get('arm_scale', 1.0)); LEAN = float(cfg.get('lean_deg', 0.0))
SD = P / 'Saved/Codex/SHME_V244_20261101'; SD.mkdir(parents=True, exist_ok=True)
seq = u.load_asset(SRC); assert seq, SRC
NAMES = [str(n) for n in AL.get_animation_track_names(seq)]; N = ae.num_frames(seq); T = float(seq.get_play_length()); DT = T / max(N - 1, 1)
L = ae.read_local(seq, NAMES, list(range(N))); local = {b: [L[b][f] for f in range(N)] for b in NAMES}
clip = ae.Clip(seq, ['root', 'pelvis', 'spine_01', 'spine_02', 'spine_03', 'spine_04', 'spine_05', 'neck_01', 'head', 'clavicle_l', 'clavicle_r', 'upperarm_l', 'upperarm_r',
                     'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r', 'thigh_l', 'thigh_r', 'calf_l', 'calf_r', 'foot_l', 'foot_r', 'ball_l', 'ball_r'] + [b for b in ('ik_foot_l', 'ik_foot_r', 'ik_foot_root') if b in NAMES])
UP = (0.0, 0.0, 1.0)
def twist_z(q):
    z, w = q[2], q[3]; n = math.hypot(z, w) or 1.0; return math.degrees(2.0 * math.atan2(z / n, w / n))
def wrap(a): return (a + 180.0) % 360.0 - 180.0
# original foot / knee world transforms (kept), chest yaw (kept), pelvis yaw series
FOOT = {s: [clip.comp('foot_' + s, f, local) for f in range(N)] for s in 'lr'}
KNEE = {s: [clip.comp('calf_' + s, f, local)[0] for f in range(N)] for s in 'lr'}
pq = [clip.comp('pelvis', f, local)[1] for f in range(N)]; cq0 = [clip.comp('spine_05', f, local)[1] for f in range(N)]; HQ0 = [clip.comp('head', f, local)[1] for f in range(N)]
py = [twist_z(q) for q in pq]
mean = math.degrees(math.atan2(sum(math.sin(math.radians(a)) for a in py), sum(math.cos(math.radians(a)) for a in py)))
dl = [wrap(a - mean) for a in py]
before = {'pelvis_yaw_p2p': round(max(dl) - min(dl), 2), 'chest_yaw_p2p': round(max(twist_z(q) for q in cq0) - min(twist_z(q) for q in cq0), 2),
          'counter_p2p': round(max(twist_z(c) - p for c, p in zip(cq0, py)) - min(twist_z(c) - p for c, p in zip(cq0, py)), 2)}
if 'spine_01' not in NAMES: raise RuntimeError('no spine_01')
cy0 = [twist_z(q) for q in cq0]; mean_c = math.degrees(math.atan2(sum(math.sin(math.radians(a)) for a in cy0), sum(math.cos(math.radians(a)) for a in cy0)))
dc = [wrap(a - mean_c) for a in cy0]        # chest world-yaw excursion (the clip's chest swings MORE than its pelvis: 16 vs 12 deg p2p)
LAT = None
for f in range(N):
    d = -(1.0 - S) * dl[f]                                   # remove part of the pelvis yaw excursion
    ae.apply_bone_delta(clip, local, 'pelvis', f, ae.qaxis(UP, d))
    ae.apply_bone_delta(clip, local, 'spine_01', f, ae.qaxis(UP, -d))   # the chest keeps its world orientation
    dcf = -(1.0 - SC) * dc[f]                                 # then the chest's own world-yaw excursion is scaled (chest_scale)
    if abs(dcf) > 1e-6:
        ae.apply_bone_delta(clip, local, 'spine_01', f, ae.qaxis(UP, dcf))
        if 'neck_01' in NAMES: ae.apply_bone_delta(clip, local, 'neck_01', f, ae.qaxis(UP, -dcf))   # the head keeps its world yaw
    if abs(LEAN) > 1e-3:
        cp_, cqn = clip.comp('spine_03', f, local); fwd = ae.qrot(cqn, (0.0, 1.0, 0.0)); lat = ae.vnorm(ae.vcross(UP, (fwd[0], fwd[1], 0.0)))
        ae.apply_bone_delta(clip, local, 'spine_01', f, ae.qaxis(lat, -LEAN))
    if abs(ARM - 1.0) > 1e-3:
        for s in 'lr':
            b = 'upperarm_' + s
            if b not in NAMES: continue
            cp_, cqn = clip.comp('spine_05', f, local); fwd = ae.qrot(cqn, (0.0, 1.0, 0.0)); lat = ae.vnorm(ae.vcross(UP, (fwd[0], fwd[1], 0.0)))
            # swing angle about the lateral axis relative to the loop-mean orientation is scaled by ARM (approximation on the twist about lat)
            _, aq = clip.comp(b, f, local); mq = ae.qnorm(ae.qmul(ae.qinv(cqn), aq))
            ang = math.degrees(2.0 * math.atan2(mq[0] * lat[0] + mq[1] * lat[1] + mq[2] * lat[2], mq[3]))
            ae.apply_bone_delta(clip, local, b, f, ae.qaxis(lat, (ARM - 1.0) * ang))
    for s in 'lr':
        ae.solve_leg(clip, local, s, f, FOOT[s][f][0], FOOT[s][f][1], KNEE[s][f])
    if 'ik_foot_root' in NAMES:
        for s in 'lr':
            b = 'ik_foot_' + s
            if b in NAMES:
                fp, fq = clip.comp('foot_' + s, f, local); pp, pqq = clip.comp('ik_foot_root', f, local)
                local[b][f] = (ae.qrot(ae.qinv(pqq), ae.vsub(fp, pp)), ae.qnorm(ae.qmul(ae.qinv(pqq), fq)), local[b][f][2])
pq2 = [clip.comp('pelvis', f, local)[1] for f in range(N)]; cq2 = [clip.comp('spine_05', f, local)[1] for f in range(N)]
py2 = [twist_z(q) for q in pq2]; m2 = math.degrees(math.atan2(sum(math.sin(math.radians(a)) for a in py2), sum(math.cos(math.radians(a)) for a in py2)))
dl2 = [wrap(a - m2) for a in py2]
ferr = max(ae.vlen(ae.vsub(clip.comp('foot_' + s, f, local)[0], FOOT[s][f][0])) for s in 'lr' for f in range(N))
after = {'pelvis_yaw_p2p': round(max(dl2) - min(dl2), 2), 'chest_yaw_p2p': round(max(twist_z(q) for q in cq2) - min(twist_z(q) for q in cq2), 2),
         'counter_p2p': round(max(twist_z(c) - p for c, p in zip(cq2, py2)) - min(twist_z(c) - p for c, p in zip(cq2, py2)), 2), 'foot_err_max': round(ferr, 3),
         'chest_yaw_change_max': round(max(abs(wrap(twist_z(a) - twist_z(b))) for a, b in zip(cq2, cq0)), 2), 'head_yaw_change_max': round(max(abs(wrap(twist_z(clip.comp('head', f, local)[1]) - twist_z(HQ0[f]))) for f in range(N)), 2)}
try:
    lm = ae.leg_metrics(seq, local, None, None); leg = {s: {'axis_jump_deg': round(lm[s]['axis_jump_deg'], 1), 'hinge_min': round(lm[s]['hinge_min'], 2), 'backward': lm[s]['backward_frames']} for s in 'lr'}
except Exception as ex: leg = {'err': str(ex)[:100]}
out = {'src': SRC, 'frames': N, 'len_s': round(T, 3), 'cfg': {k: cfg[k] for k in cfg}, 'before': before, 'after': after, 'leg': leg, 'mode': 'inplace' if INPLACE else ('out' if OUT else 'dry')}
def apply_to(target):
    ae.leg_guard(seq, local, label='SHM244_Walk')
    c = ae.controller(target)
    try: c.open_bracket(u.Text('SHME V2.44 walk candidate'), True)
    except Exception: c.open_bracket('SHME V2.44 walk candidate', True)
    try:
        for b in NAMES:
            ks = local[b]
            if not c.set_bone_track_keys(b, [u.Vector(*k[0]) for k in ks], [u.Quat(*k[1]) for k in ks], [u.Vector(*k[2]) for k in ks], True): raise RuntimeError('keys ' + b)
    finally: c.close_bracket(True)
if not DRY:
    if INPLACE: apply_to(seq); out['applied_in_memory'] = True; out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()][:6]
    elif OUT:
        tgt = u.load_asset(OUT) if EAL.does_asset_exist(OUT) else EAL.duplicate_asset(SRC, OUT); assert tgt
        for tr in [str(x) for x in AL.get_animation_notify_track_names(tgt)]:
            AL.remove_animation_notify_events_by_track(tgt, tr)
            try: AL.remove_animation_notify_track(tgt, tr)
            except Exception: pass
        apply_to(tgt); out['saved'] = EAL.save_loaded_asset(tgt, False); out['out'] = OUT
(SD / ('gen244_walk_%s.json' % out['mode'])).write_text(json.dumps(out, indent=1))
print('G244W ' + json.dumps(out))
