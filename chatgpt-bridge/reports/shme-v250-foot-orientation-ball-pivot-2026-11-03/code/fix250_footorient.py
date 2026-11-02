"""fix250_footorient.py v2 (dry = measure job, write = manifest of the target clips): V2.50 FOOT repair of the turning-start clips.
Measured (probe250_footaxes / probe250_blendfk / in-game vb+mx): the V2.49 ball-raise repair rotated the foot about cross(ankle->ball, Z),
which is ill-conditioned when the source foot is pitched 84 deg (ankle->ball nearly vertical): the bisection picked the backward swing, the
toes ended up BEHIND the ankle (foot heading ~140 deg off the shin, local 110-116 deg from the idle foot). In game the crossfade from the
idle sample slerps through that rotation (ball -7.6 cm / pitch 74 deg at w 0.5, -9 cm in game) and the crops show a reversed, pointed foot.
v3 (probe250_footaxes): the Candidate copies are a BROKEN retarget (feet heading -68/-101 deg = toes down and backward, pitch 83 deg); the
same clips in /Game/CoreMotion_Retargeted/AAMS/Walk/ (same SK_Mannequin) have correct feet (heading 74/110 deg like the idle, pitch 24 deg,
ball on the floor, 12-14 deg from the idle foot). Rule v3 (per clip, per foot, per frame): (1) foot_l / foot_r component ORIENTATION := that
correct retarget at the same frame
(the crops are frames 0..N-1 of the 30 fps copies; their legs carry a posture bake, so the foot is re-expressed under the crop's own calf), (2) where the ball is below the floor contact
height ZB (A_CP2_Jog_Fwd_Start frame 0 ball height), rotate the foot about ITS OWN lateral axis (foot +Z, horizontal and well defined) in
the direction that lifts the toes forward, until the ball sits at ZB. The heading of the foot is kept; frames with the ball above ZB are the
source untouched. builtins.V250_FO = {'dry': bool, 'clips': {target: source}} (default the 6 SHM248 crops). Prints FOOTORIENT250 {...}."""
import unreal as u, json, builtins, math, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V250_FO', {})); DRY = bool(cfg.get('dry', True))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
ar = u.AssetRegistryHelpers.get_asset_registry(); anyseq = {}
for a in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine', 'AnimSequence'), True):
    n = str(a.asset_name); p = str(a.package_name)
    if n not in anyseq or '/Candidate/' in p or p.startswith('/Game/GraceRanger/SHME/'): anyseq.setdefault(n, p)
CAND = {str(a.asset_name): str(a.package_name) for a in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine', 'AnimSequence'), True) if '/CoreMotionAAMS/Candidate/' in str(a.package_name)}
V = '/Game/GraceRanger/SHME/Animations/V248/'
RTG = '/Game/CoreMotion_Retargeted/AAMS/Walk/'   # the CORRECT retarget of the same Core Motion clips on SK_Mannequin (feet forward, ball on the floor)
targets = cfg.get('clips') or {V + 'SHM248_Jog_Start_Turn%s%s_crop' % (s, d): RTG + 'af_Loco_Jog_Start_Turn%s%s_%sfoot' % (s, d, s) for s in 'LR' for d in ('090', '135', '180')}
ref = ae.Clip(u.load_asset(anyseq['A_CP2_Jog_Fwd_Start']), ['ball_l', 'ball_r'])
ZB = 0.5 * (ref.comp('ball_l', 0)[0][2] + ref.comp('ball_r', 0)[0][2])
idle = u.load_asset(anyseq['af_Stand_Idle_NaturalBaseline_Phase275'])
FI = int(round(79.40 * (ae.num_frames(idle) - 1) / idle.get_play_length()))
IL = {b: ae.read_local(idle, [b], [FI])[b][0][1] for b in ('foot_l', 'foot_r')}
def pitch(a, b): return math.degrees(math.atan2(a[2] - b[2], max(1e-6, math.hypot(b[0] - a[0], b[1] - a[1]))))
def head(a, b): return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
def qang(a, b): return round(math.degrees(2 * math.acos(min(1.0, abs(sum(x * y for x, y in zip(a, b)))))), 1)
out = {'dry': DRY, 'zb': round(ZB, 2), 'clips': {}, 'saved': 0}
for tp, sp in targets.items():
    seq = u.load_asset(tp); src = u.load_asset(sp); c = ae.Clip(seq, ['foot_l', 'foot_r', 'ball_l', 'ball_r']); nf = c.nf
    scl = ae.Clip(src, ['foot_l', 'foot_r', 'ball_l', 'ball_r'])
    local = {k: list(v) for k, v in c.local.items()}; info = {}
    calf_err = max(qang(local['calf_' + s][f][1], scl.local['calf_' + s][f][1]) for s in 'lr' for f in range(min(nf, scl.nf)))
    pel_err = max(ae.vlen(ae.vsub(c.comp('pelvis', f, local)[0], scl.comp('pelvis', f)[0])) for f in range(min(nf, scl.nf))) if 'pelvis' in scl.local and 'pelvis' in local else -1
    root_err = max(ae.vlen(ae.vsub(c.comp('root', f, local)[0], scl.comp('root', f)[0])) for f in range(min(nf, scl.nf)))
    for s in 'lr':
        fb = 'foot_' + s; nfix = 0; hd = 0.0; zmin = 1e9; pb, pa = [], []
        for f in range(nf):
            Qsrc = scl.comp(fb, min(f, scl.nf - 1))[1]; Qp = c.comp(c.parent[fb], f, local)[1]     # (1) the untouched source foot ORIENTATION
            local[fb][f] = (local[fb][f][0], ae.qnorm(ae.qmul(ae.qinv(Qp), Qsrc)), local[fb][f][2])
            A, Q = c.comp(fb, f, local); B0 = c.comp('ball_' + s, f, local)[0]; pb.append(pitch(A, B0))
            if B0[2] < ZB - 0.05:
                lat = ae.vnorm(ae.qrot(Q, (0.0, 0.0, 1.0))); d = ae.vsub(B0, A); h0 = head(A, B0)
                def ball(th): return ae.vadd(A, ae.qrot(ae.qaxis(lat, th), d))
                def ok(th):
                    b = ball(th); return b[2] - B0[2] > 0 and abs(((head(A, b) - h0) + 180) % 360 - 180) < 60
                sgn = 1.0 if ok(10.0) else -1.0
                lo, hi = 0.0, 89.0
                if ball(sgn * hi)[2] < ZB: th = sgn * hi
                else:
                    for _ in range(40):
                        mid = 0.5 * (lo + hi)
                        if ball(sgn * mid)[2] < ZB: lo = mid
                        else: hi = mid
                    th = sgn * hi
                ae.apply_bone_delta(c, local, fb, f, ae.qaxis(lat, th)); nfix += 1
            A2 = c.comp(fb, f, local)[0]; B2 = c.comp('ball_' + s, f, local)[0]
            pa.append(pitch(A2, B2)); zmin = min(zmin, B2[2]); hd = max(hd, abs(((head(A2, B2) - head(A, B0)) + 180) % 360 - 180))
        info[s] = {'fixed': nfix, 'nf': nf, 'pitch_src': [round(min(pb), 1), round(max(pb), 1), round(pb[0], 1)], 'pitch_after': [round(min(pa), 1), round(max(pa), 1), round(pa[0], 1)],
                   'ball_z_min': round(zmin, 1), 'heading_change_max': round(hd, 1), 'f0_local_to_idle': qang(local[fb][0][1], IL[fb])}
    info['calf_err'] = calf_err; info['root_err_cm'] = round(root_err, 2); info['pelvis_err_cm'] = round(pel_err, 2); out['clips'][tp.split('/')[-1]] = info
    if not DRY:
        ae.write_tracks(seq, local, ['foot_l', 'foot_r'], note='SHME V2.50 foot repair (source foot + lateral-axis lift)', guard=False)
        assert EAL.save_asset(tp, False), tp; out['saved'] += 1
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('FOOTORIENT250 ' + json.dumps(out))
