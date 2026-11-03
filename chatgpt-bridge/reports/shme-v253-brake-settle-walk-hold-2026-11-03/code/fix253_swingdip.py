"""fix253_swingdip.py (dry = measure job; write = manifest of the listed loops): V2.53 owner of the jog-loop "toe scuff" (jstart 50-59 cm at
60 / 120 FPS, A_CT_Jog_FwdLeft): measured frame by frame (v252f60 / f120 jstart 9.2 s): the right ball touches the floor at 7-11 m/s in
the MIDDLE of its swing (-1.9 cm vs the standing floor), lifts again to +3.8 cm and lands 0.15 s later - identical at 60 and 120 FPS, also in
the mannequin pose. Clip data (probe253_clips.py): A_CT_Jog_FwdLeft itself passes the swinging right ball only ~2 cm above its contact
level at 0.833 s at 8 m/s (a mid-swing dip), then rises to 7 cm before the landing at 1.0 s.
Fix (content): for every A_CT_Jog_* loop in /Game/GraceRanger/Animations/Continuity, per foot and per swing phase (ball above contact + 1 cm
between toe-off and landing), a local minimum of the ball height with a rise of > RISE cm after it (a dip, not the landing approach) and a
clearance < CLEAR cm above the contact level is lifted by a smooth bump (quintic, window = the swing part from the previous maximum to the
next maximum) so the dip clears CLEAR cm; the foot keeps its rotation, the leg is re-solved (V2.10 hinge solver, knee hint = source knee),
loop seam and stance untouched. builtins.V253_DIP = {'dry': bool, 'clear': 3.5, 'rise': 1.5, 'only': [...]}. Prints DIP253 {...}."""
import unreal as u, json, builtins, math, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V253_DIP', {})); DRY = bool(cfg.get('dry', True)); CLEAR = float(cfg.get('clear', 3.5)); RISE = float(cfg.get('rise', 1.5)); ONLY = cfg.get('only')
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
F = '/Game/GraceRanger/Animations/Continuity'
ar = u.AssetRegistryHelpers.get_asset_registry()
names = sorted(str(a.asset_name) for a in ar.get_assets_by_path(F, False) if str(a.asset_class_path.asset_name) == 'AnimSequence' and str(a.asset_name).startswith('A_CT_Jog'))
def mj(x): x = min(1.0, max(0.0, x)); return x * x * x * (10 - 15 * x + 6 * x * x)
out = {'dry': DRY, 'clear': CLEAR, 'clips': {}}
for n in names:
    if ONLY and n not in ONLY: continue
    p = F + '/' + n; seq = u.load_asset(p)
    TN = [str(x) for x in AL.get_animation_track_names(seq)]; IK = [b for b in ('ik_foot_root', 'ik_foot_l', 'ik_foot_r') if b in TN]
    c = ae.Clip(seq, ['root', 'pelvis', 'thigh_l', 'calf_l', 'foot_l', 'ball_l', 'thigh_r', 'calf_r', 'foot_r', 'ball_r'] + IK); nf = c.nf; dt = float(seq.get_play_length()) / max(1, nf - 1)
    local = {b: list(v) for b, v in c.local.items()}; rec = {'frames': nf, 'dips': []}; touched = False
    for s in 'lr':
        bz = [c.comp('ball_' + s, f)[0][2] for f in range(nf)]; contact = min(bz)
        feet = [c.comp('foot_' + s, f) for f in range(nf)]; knees = [c.comp('calf_' + s, f)[0] for f in range(nf)]
        lift = [0.0] * nf
        for f in range(1, nf - 1):
            if not (bz[f] <= bz[f - 1] and bz[f] <= bz[f + 1]) or bz[f] > contact + CLEAR or bz[f] < contact + 1.0: continue
            # previous / next local maximum (the swing part around the dip)
            a = f
            while a > 0 and bz[a - 1] >= bz[a]: a -= 1
            b = f
            while b < nf - 1 and bz[b + 1] >= bz[b]: b += 1
            if bz[b] - bz[f] < RISE or bz[a] - bz[f] < RISE or a == f or b == f: continue
            need = contact + CLEAR - bz[f]
            for g in range(a, b + 1):
                x = (g - a) / max(1, f - a) if g <= f else 1.0 - (g - f) / max(1, b - f)
                lift[g] = max(lift[g], need * mj(x))
            rec['dips'].append([s, round(f * dt, 3), round(bz[f] - contact, 2), round(bz[b] - contact, 2), round(a * dt, 3), round(b * dt, 3), round(need, 2)])
        for g in range(nf):
            if lift[g] > 1e-3:
                ft, fq = feet[g]; ae.solve_leg(c, local, s, g, (ft[0], ft[1], ft[2] + lift[g]), fq, ae.vadd(knees[g], (0.0, 0.0, lift[g])))
                touched = True
        rec['ball_after_' + s] = None
    if touched and 'ik_foot_root' in IK:
        for s in 'lr':
            b = 'ik_foot_' + s
            if b not in IK: continue
            for f in range(nf):
                fp, fq = c.comp('foot_' + s, f, local); pp, pq = c.comp('ik_foot_root', f, local)
                local[b][f] = (ae.qrot(ae.qinv(pq), ae.vsub(fp, pp)), ae.qnorm(ae.qmul(ae.qinv(pq), fq)), local[b][f][2])
    rec['ik_bones'] = IK
    if touched:
        ferr = max(abs(c.comp('foot_' + s, f, local)[0][2] - c.comp('foot_' + s, f)[0][2]) for s in 'lr' for f in range(nf)); rec['max_lift_cm'] = round(ferr, 2)
        if not DRY:
            ae.write_tracks(seq, local, ['thigh_l', 'calf_l', 'foot_l', 'thigh_r', 'calf_r', 'foot_r'] + [b for b in IK if b != 'ik_foot_root'], note='SHME V2.53 swing dip clearance', guard=True)
            assert EAL.save_loaded_asset(seq, False), p; rec['saved'] = True
    out['clips'][n] = rec
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('DIP253 ' + json.dumps(out, default=str))
