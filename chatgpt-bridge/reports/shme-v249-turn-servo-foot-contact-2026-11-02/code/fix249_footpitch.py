"""fix249_footpitch.py v2 (editor job; dry = measure job, write = manifest of the project copies): V2.49 GROUND-CONTACT foot repair of the
jog starts derived from CoreMotionAAMS/Candidate af_Loco_Jog_*_Start*_AAMS.
Measured (footpitch249 + clip FK + in-game LTP): in those clips the ankle height is normal (8.7 cm standing) but the foot bone is pitched
83-84 deg, so the ball joint sits 8 cm BELOW the floor (toes through the ground = tiptoe) whenever the foot bears weight; a constant
local offset (v1) was wrong (it tilted swing toes 70 deg up). Rule (physical, per frame, per foot): if the ball is below the floor
contact height Zb, rotate the foot bone about the ANKLE around its lateral axis (toes up) until the ball sits exactly at Zb; otherwise
untouched. Swing, heel strike and real toe-off (a high ankle) keep their authored pitch because the ball is then above Zb.
Zb = ball height of the reference standing start (A_CP2_Jog_Fwd_Start frame 0, foot pitch 24 deg). Only the foot bones change (ball/toes
follow); thigh / calf / ankle positions untouched. Sources, vendor clips and the Candidate originals are not modified.
builtins.V249_FP = {'dry': bool}. Prints FOOTFIX249 {...} (per clip / foot: frames corrected, pitch f0 / mean / max before -> after,
min ball z before -> after)."""
import unreal as u, json, builtins, math, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V249_FP', {})); DRY = bool(cfg.get('dry', True))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
ar = u.AssetRegistryHelpers.get_asset_registry()
allseq = {str(a.asset_name): str(a.package_name) for a in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine', 'AnimSequence'), True)}
clips = sorted(p for n, p in allseq.items() if p.startswith('/Game/GraceRanger/SHME/') and (n.startswith(('SHM_JogQ_af_', 'SHM232_IS_af_')) or (n.startswith('SHM248_Jog_Start_Turn') and n.endswith('_crop'))))
ref = ae.Clip(u.load_asset(allseq['A_CP2_Jog_Fwd_Start']), ['ball_l', 'ball_r'])
ZB = 0.5 * (ref.comp('ball_l', 0)[0][2] + ref.comp('ball_r', 0)[0][2])
def pitch(fo, ba): return math.degrees(math.atan2(-(ba[2] - fo[2]), math.hypot(ba[0] - fo[0], ba[1] - fo[1])))
out = {'dry': DRY, 'zb': round(ZB, 2), 'clips': {}, 'saved': 0}
for p in clips:
    seq = u.load_asset(p); c = ae.Clip(seq, ['foot_l', 'foot_r', 'ball_l', 'ball_r']); nf = c.nf
    local = {k: list(v) for k, v in c.local.items()}; info = {}; changed = []
    for s in ('l', 'r'):
        fo_b = 'foot_' + s; nfix = 0; pb, pa, zb_b, zb_a = [], [], [], []
        for f in range(nf):
            A, Q = c.comp(fo_b, f, local); Bp = c.comp('ball_' + s, f, local)[0]
            pb.append(pitch(A, Bp)); zb_b.append(Bp[2])
            if Bp[2] < ZB - 0.05:
                d = ae.vsub(Bp, A); lat = ae.vnorm(ae.vcross(d, (0.0, 0.0, 1.0)))
                def ball_z(th):
                    return A[2] + ae.qrot(ae.qaxis(lat, th), d)[2]
                # sign: the direction that raises the ball
                sgn = 1.0 if ball_z(5.0) > ball_z(-5.0) else -1.0
                lo, hi = 0.0, 89.0
                if ball_z(sgn * hi) < ZB: th = sgn * hi
                else:
                    for _ in range(40):
                        mid = 0.5 * (lo + hi)
                        if ball_z(sgn * mid) < ZB: lo = mid
                        else: hi = mid
                    th = sgn * hi
                ae.apply_bone_delta(c, local, fo_b, f, ae.qaxis(lat, th)); nfix += 1
            A2 = c.comp(fo_b, f, local)[0]; B2 = c.comp('ball_' + s, f, local)[0]
            pa.append(pitch(A2, B2)); zb_a.append(B2[2])
        if nfix: changed.append(fo_b)
        info[s] = {'fixed': nfix, 'nf': nf, 'f0': [round(pb[0], 1), round(pa[0], 1)], 'mean': [round(sum(pb) / nf, 1), round(sum(pa) / nf, 1)], 'max': [round(max(pb), 1), round(max(pa), 1)],
                   'min_ball_z': [round(min(zb_b), 1), round(min(zb_a), 1)]}
    out['clips'][p.split('/')[-1]] = info
    if not DRY and changed:
        ae.write_tracks(seq, local, changed, note='SHME V2.49 foot ground-contact repair', guard=False)
        assert EAL.save_asset(p, False), p; out['saved'] += 1
out['n'] = len(clips)
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('FOOTFIX249 ' + json.dumps(out))
