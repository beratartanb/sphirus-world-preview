"""gen242_idle.py (editor job): V2.42 Locomotion Identity - a WEIGHTED, BREATHING standing idle authored as content (no runtime procedural
sway). Production idle (af_Stand_Idle_NaturalBaseline_Phase275, 10 s) measured in game: pelvis p2p 0.1 cm, chest 0.2 cm, pelvis centred
between the feet (-1 cm) - a frozen mannequin; only the head (look AO) moves. A standing human keeps the weight on one leg, breathes
(~15/min, chest rises ~0.5 cm) and drifts a little.
Content (12 s loop, feet fixed in the world, legs re-solved with the hinge-safe two-bone solver, starts and ends on the production idle
pose so the V2.6 walk stops and every start keep their entry/exit stance):
  0.0-0.8 neutral | 0.8-2.2 weight -> RIGHT (pelvis +3.5 cm toward the right foot, -0.7 cm down, 2.5 deg roll (free hip drops), 2 deg yaw;
  spine counter-rolls 1.5 deg so the shoulders stay nearly level) | hold 3.2 s | 5.4-6.8 back | 7.6-9.0 weight -> LEFT | hold | 10.6-12.0 back.
  Breathing 15/min (3 cycles = loop-safe): spine_04/05 pitch 0.5 deg each (chest lift), clavicles +0.4 deg, neck counter 0.4 deg.
  Micro sway: pelvis 0.35 cm at 1/6 Hz lateral + 0.25 cm at 1/4 Hz fore-aft (integer cycles -> seamless loop); head yaw drift +-1 deg at 1/12 Hz.
builtins.G242I = {dry_run, src (idle clip), out (asset path), shift_cm 3.5, drop_cm 0.7, roll_deg 2.5, yaw_deg 2.0, breath_deg 0.5, sway_cm 0.35, seconds 12}.
Output: the clip + Saved/Codex/SHME_V242_20261101/gen242_idle_<dry|write>.json (pelvis offset / head drift / foot error per phase)."""
import unreal as u, json, math, builtins, pathlib, importlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'G242I', {})); DRY = bool(cfg.get('dry_run', True))
SRC = cfg.get('src', '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/Phase275Support/Idle/af_Stand_Idle_NaturalBaseline_Phase275')
OUT = cfg.get('out', '/Game/GraceRanger/SHME/Animations/V242/SHM242_Idle_Weighted')
SD = P / 'Saved/Codex/SHME_V242_20261101'; SD.mkdir(parents=True, exist_ok=True)
K = lambda k, d: float(cfg.get(k, d))
SHIFT = K('shift_cm', 3.5); DROP = K('drop_cm', 0.7); ROLL = K('roll_deg', 2.5); YAW = K('yaw_deg', 2.0); CROLL = K('counter_roll_deg', 1.5)
BREATH = K('breath_deg', 0.5); SWAY = K('sway_cm', 0.35); SWAY2 = K('sway2_cm', 0.25); HEADYAW = K('head_yaw_deg', 1.0); SECS = K('seconds', 11.2)
FPS = 30.0; DT = 1.0 / FPS; N = int(round(SECS * FPS)) + 1
idle = u.load_asset(SRC); assert idle, SRC
NAMES = [str(n) for n in AL.get_animation_track_names(idle)]
B0 = ae.read_local(idle, NAMES, [0]); BASE = {b: B0[b][0] for b in NAMES}
clip = ae.Clip(idle, ['root', 'pelvis', 'spine_03', 'spine_04', 'spine_05', 'neck_01', 'head', 'clavicle_l', 'clavicle_r', 'thigh_l', 'thigh_r', 'calf_l', 'calf_r',
                      'foot_l', 'foot_r', 'ball_l', 'ball_r', 'hand_l', 'hand_r'] + [b for b in ('ik_foot_l', 'ik_foot_r', 'ik_foot_root') if b in NAMES])
local = {b: [BASE[b] for _ in range(N)] for b in NAMES}
# frames of reference from the base pose: RIGHT = left foot -> right foot, FWD = up x RIGHT (horizontal), feet / knee targets
fl, ql = clip.comp('foot_l', 0, local); fr, qr = clip.comp('foot_r', 0, local)
RIGHT = ae.vnorm((fr[0] - fl[0], fr[1] - fl[1], 0.0)); FWD = ae.vnorm(ae.vcross((0.0, 0.0, 1.0), RIGHT)); UP = (0.0, 0.0, 1.0)
FOOT = {'l': (fl, ql), 'r': (fr, qr)}; KNEE0 = {s: clip.comp('calf_' + s, 0, local)[0] for s in 'lr'}
PEL0 = clip.comp('pelvis', 0, local)[0]; HEAD0 = clip.comp('head', 0, local)[0]
_, QROOT = clip.comp('root', 0, local)
def mj(x): x = min(1.0, max(0.0, x)); return x * x * x * (10 - 15 * x + 6 * x * x)
def ramp(t, t0, t1): return mj((t - t0) / max(t1 - t0, 1e-3))
def weights(t):
    wr = ramp(t, 0.8, 2.2) * (1.0 - ramp(t, 5.4, 6.8)); wl = ramp(t, 7.6, 9.0) * (1.0 - ramp(t, 10.6, 12.0)); return wr, wl
def breath(t): return 0.5 * (1.0 - math.cos(2.0 * math.pi * 0.25 * t))
rows = []
for f in range(N):
    t = f * DT; wr, wl = weights(t); w = wr - wl; b = breath(t)
    sway = ae.vadd(ae.vsc(RIGHT, SWAY * math.sin(2.0 * math.pi * t / 6.0)), ae.vsc(FWD, SWAY2 * math.sin(2.0 * math.pi * t / 4.0 + 1.1)))
    dp = ae.vadd(ae.vadd(ae.vsc(RIGHT, SHIFT * w), ae.vsc(UP, -DROP * abs(w))), sway)
    lt, lq, ls = local['pelvis'][f]; local['pelvis'][f] = (ae.vadd(lt, ae.qrot(ae.qinv(QROOT), dp)), lq, ls)
    # pelvis: free hip drops (roll about FWD toward the free side), slight yaw toward the free side; spine counter-rolls
    ae.apply_bone_delta(clip, local, 'pelvis', f, ae.qaxis(FWD, -ROLL * w))
    ae.apply_bone_delta(clip, local, 'pelvis', f, ae.qaxis(UP, YAW * w))
    ae.apply_bone_delta(clip, local, 'spine_03', f, ae.qaxis(FWD, CROLL * w))
    ae.apply_bone_delta(clip, local, 'spine_05', f, ae.qaxis(FWD, 0.5 * CROLL * w))
    ae.apply_bone_delta(clip, local, 'spine_03', f, ae.qaxis(UP, -0.6 * YAW * w))
    # breathing: chest lifts (pitch back about RIGHT), shoulders rise, head stays level
    for bn, k in (('spine_04', 1.0), ('spine_05', 1.0)):
        if bn in NAMES: ae.apply_bone_delta(clip, local, bn, f, ae.qaxis(RIGHT, -BREATH * k * b))
    for s, sg in (('l', 1.0), ('r', -1.0)):
        if 'clavicle_' + s in NAMES: ae.apply_bone_delta(clip, local, 'clavicle_' + s, f, ae.qaxis(FWD, sg * 0.4 * BREATH / 0.5 * b))
    if 'neck_01' in NAMES: ae.apply_bone_delta(clip, local, 'neck_01', f, ae.qaxis(RIGHT, 0.8 * BREATH * b))
    if 'head' in NAMES: ae.apply_bone_delta(clip, local, 'head', f, ae.qaxis(UP, HEADYAW * math.sin(2.0 * math.pi * t / 12.0)))
    # legs: feet fixed in the world, knee hints = base knees pushed a little outward (lateral), continuity through the solver
    for s in 'lr':
        kh = ae.vadd(KNEE0[s], ae.vsc(RIGHT, (1.0 if s == 'r' else -1.0) * 1.0))
        ae.solve_leg(clip, local, s, f, FOOT[s][0], FOOT[s][1], kh)
    if 'ik_foot_root' in NAMES:
        for s in 'lr':
            bn = 'ik_foot_' + s
            if bn in NAMES:
                fp, fq = clip.comp('foot_' + s, f, local); pp, pq = clip.comp('ik_foot_root', f, local)
                local[bn][f] = (ae.qrot(ae.qinv(pq), ae.vsub(fp, pp)), ae.qnorm(ae.qmul(ae.qinv(pq), fq)), local[bn][f][2])
    pel = clip.comp('pelvis', f, local)[0]; hd = clip.comp('head', f, local)[0]
    fe = max(ae.vlen(ae.vsub(clip.comp('foot_' + s, f, local)[0], FOOT[s][0])) for s in 'lr')
    rows.append({'t': round(t, 3), 'w': round(w, 3), 'b': round(b, 3), 'pel_right_cm': round(ae.vdot(ae.vsub(pel, PEL0), RIGHT), 2), 'pel_z': round(pel[2] - PEL0[2], 2),
                 'head_right_cm': round(ae.vdot(ae.vsub(hd, HEAD0), RIGHT), 2), 'head_z': round(hd[2] - HEAD0[2], 2), 'foot_err': round(fe, 3)})
# V2.42b: NOT closed as a loop. A BranchIn-built database entry does not loop: MM entered the 12 s clip at its LAST frame (identical to
# frame 0 = the stop's end pose) and held it - a frozen idle. The clip now ends at 11.2 s, 37 % of the way back from the left weight
# shift (1.3 cm off neutral): frame 0 is the unique best match for the stop's end pose, and the re-entry at the clip end is a 1.3 cm
# pelvis blend over the MM blend time instead of a hold.
if cfg.get('close_loop'):
    for bn in NAMES: local[bn][N - 1] = local[bn][0]
try:
    lm = ae.leg_metrics(idle, local, None, None); leg = {s: {'axis_jump_deg': round(lm[s]['axis_jump_deg'], 1), 'hinge_min': round(lm[s]['hinge_min'], 2), 'backward': lm[s]['backward_frames']} for s in 'lr'}
except Exception as ex: leg = {'err': str(ex)[:100]}
out = {'src': SRC, 'out': OUT, 'frames': N, 'seconds': SECS, 'cfg': {k: cfg[k] for k in cfg if k != 'dry_run'}, 'leg': leg,
       'pelvis_right_max': max(r['pel_right_cm'] for r in rows), 'pelvis_right_min': min(r['pel_right_cm'] for r in rows), 'pelvis_z_min': min(r['pel_z'] for r in rows),
       'head_right_p2p': round(max(r['head_right_cm'] for r in rows) - min(r['head_right_cm'] for r in rows), 2), 'head_z_p2p': round(max(r['head_z'] for r in rows) - min(r['head_z'] for r in rows), 2),
       'foot_err_max': max(r['foot_err'] for r in rows), 'samples': rows[::15]}
def write():
    ae.leg_guard(idle, local, label='SHM242_Idle_Weighted')
    seq = u.load_asset(OUT) if EAL.does_asset_exist(OUT) else EAL.duplicate_asset(SRC, OUT)
    for tr in [str(x) for x in AL.get_animation_notify_track_names(seq)]:
        AL.remove_animation_notify_events_by_track(seq, tr)
        try: AL.remove_animation_notify_track(seq, tr)
        except Exception: pass
    c = ae.controller(seq)
    try: c.open_bracket(u.Text('SHME V2.42 weighted idle'), True)
    except Exception: c.open_bracket('SHME V2.42 weighted idle', True)
    try:
        c.set_number_of_frames(u.FrameNumber(N - 1), True)
        for bn in NAMES:
            ks = local[bn]
            if not c.set_bone_track_keys(bn, [u.Vector(*k[0]) for k in ks], [u.Quat(*k[1]) for k in ks], [u.Vector(*k[2]) for k in ks], True): raise RuntimeError('keys ' + bn)
    finally: c.close_bracket(True)
    ts = [f * DT for f in range(N)]
    for cn in [str(x) for x in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]: AL.remove_curve(seq, cn, False)
    for cn in ('FootSpeed_L', 'FootSpeed_R', 'MoveData_Speed', 'footspeed_l', 'footspeed_r'):
        AL.add_curve(seq, cn, u.RawCurveTrackTypes.RCT_FLOAT, False); AL.add_float_curve_keys(seq, cn, ts, [0.0] * N)
    return EAL.save_loaded_asset(seq, False)
if not DRY: out['saved'] = write()
(SD / ('gen242_idle_%s.json' % ('dry' if DRY else 'write'))).write_text(json.dumps(out, indent=1))
print('G242I ' + json.dumps({k: out[k] for k in out if k != 'samples'}))
