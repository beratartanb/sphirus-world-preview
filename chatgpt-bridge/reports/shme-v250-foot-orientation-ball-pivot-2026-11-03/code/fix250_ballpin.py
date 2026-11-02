"""fix250_ballpin.py (dry = measure job, write = manifest of the crops): V2.50 FIRST-STEP BALL PIVOT of the turning-start crops.
Measured (probe250_footpath, in game contact250): in the TurnL135 crop (and its Core Motion source) the stepping foot SKIDS 4-6 cm along the
floor during its first 0.2 s (ball at floor height, heel rising, foot turning) before it lifts; in game 6-10 cm. A real pivot step keeps
the ball of the foot fixed while the heel swings round it, then the foot lifts cleanly.
Rule (per crop, per foot): first contact phase = frames from 0 while the ball stays within 2 cm of its frame-0 height. In that phase the
ball is pinned to its frame-0 position (component space with the animated root = the in-game world path under the V2.49 servo); the foot
keeps its own rotation, so the heel swings round the ball; the leg is re-solved with the V2.10 hinge solver (knee hint = the clip's knee).
The correction fades out over the 6 frames after lift-off. Only thigh/calf/foot of that leg change; write_tracks runs the leg guard.
builtins.V250_BP = {'dry': bool, 'feet': {crop: 'lr'|'l'|'r'}} (only the feet whose knee-axis jump stays within 3 deg of the source). Prints BALLPIN250 {...}."""
import unreal as u, json, builtins, math, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V250_BP', {})); DRY = bool(cfg.get('dry', True))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
V = '/Game/GraceRanger/SHME/Animations/V248/'
clips = cfg.get('clips') or [V + 'SHM248_Jog_Start_Turn%s%s_crop' % (s, d) for s in 'LR' for d in ('090', '135', '180')]
FADE = (0.857, 0.714, 0.571, 0.429, 0.286, 0.143)
def hd(a, b): return math.hypot(a[0] - b[0], a[1] - b[1])
out = {'dry': DRY, 'clips': {}, 'saved': 0}
for p in clips:
    seq = u.load_asset(p); c = ae.Clip(seq, ['foot_l', 'foot_r', 'ball_l', 'ball_r']); nf = c.nf
    local = {k: list(v) for k, v in c.local.items()}; info = {}; changed = []
    try: ref_guard = ae.leg_metrics(seq, {k: list(v) for k, v in c.local.items()})
    except Exception as e: ref_guard = {'err': str(e)[:100]}
    allow = (cfg.get('feet') or {}).get(p.split('/')[-1], 'lr')
    for s in 'lr':
        fb, bb, cb = 'foot_' + s, 'ball_' + s, 'calf_' + s
        if s not in allow: info[s] = {'skipped': 'knee-axis guard (pin raised the frame-to-frame hinge-axis jump > 3 deg over the source)'}; continue
        B0 = c.comp(bb, 0, local)[0]; fe = 0
        while fe + 1 < nf and c.comp(bb, fe + 1, local)[0][2] < B0[2] + 2.0: fe += 1
        before = max(hd(c.comp(bb, f, local)[0], B0) for f in range(fe + 1))
        if before < 1.0 or fe < 2: info[s] = {'phase': [0, fe], 'drift_before': round(before, 2), 'pinned': False}; continue
        last = (0.0, 0.0, 0.0); shift = 0.0
        for f in range(min(nf, fe + 1 + len(FADE))):
            A, Q = c.comp(fb, f, local); Bc = c.comp(bb, f, local)[0]; K = c.comp(cb, f, local)[0]
            if f <= fe: dlt = (B0[0] - Bc[0], B0[1] - Bc[1], B0[2] - Bc[2]); last = dlt
            else: w = FADE[f - fe - 1]; dlt = ae.vsc(last, w)
            shift = max(shift, ae.vlen(dlt))
            ae.solve_leg(c, local, s, f, ae.vadd(A, dlt), Q, K)
        after = max(hd(c.comp(bb, f, local)[0], B0) for f in range(fe + 1))
        lift = [round(c.comp(bb, f, local)[0][2] - B0[2], 1) for f in range(fe + 1, min(nf, fe + 5))]
        info[s] = {'phase': [0, fe], 'drift_before': round(before, 2), 'drift_after': round(after, 2), 'ankle_shift_max': round(shift, 2), 'lift_after': lift, 'pinned': True}
        changed += ['thigh_' + s, cb, fb]
    out['clips'][p.split('/')[-1]] = info
    try: g = ae.leg_metrics(seq, local); out['clips'][p.split('/')[-1]]['guard'] = {sd: {'jump': round(g[sd]['axis_jump_deg'], 1), 'jump_src': round(ref_guard[sd]['axis_jump_deg'], 1), 'hinge': g[sd]['hinge_min'], 'back': g[sd]['backward_frames'], 'twist': g[sd]['twisted_frames']} for sd in g if sd in ref_guard}
    except Exception as e: out['clips'][p.split('/')[-1]]['guard_err'] = str(e)[:200]
    if not DRY and changed:
        ae.write_tracks(seq, local, changed, note='SHME V2.50 first-step ball pivot', guard=True)
        assert EAL.save_asset(p, False), p; out['saved'] += 1
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('BALLPIN250 ' + json.dumps(out, default=str))
