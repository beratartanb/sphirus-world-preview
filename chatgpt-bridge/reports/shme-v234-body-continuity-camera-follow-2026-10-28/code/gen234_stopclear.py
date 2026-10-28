"""gen234_stopclear.py (V2.34 chain 1, sphirus-natural-motion) - copy of tip_clearance215 for the STOP closing steps: the project stop
clips close the stance by sliding a foot 40-60 cm with the ball <= 3 cm off the floor (clipstop234: SHM_A_CP2_Jog_Fwd_Stop left 0.93-1.33 s,
right 1.53-1.83 s, same in the CorePerformance source) = the 22 cm closing drag in every chain. Original V2.15 notes follow.
SHME V2.15 goal 3 (turn in place, content): the project-owned turn clips (PSD_SHM_TurnInPlace) move their stepping foot 18-111 cm with
the ball only 3-8 cm off the floor (probe_tipclips.py: Turn_180_R right foot 111 cm, ball max 5.7 cm) - a ground-skimming shuffle that the
runtime reads as a dragged planted foot (contactslip 'mid' 13-23 cm in t_tiprev / t_tiprev2). A step lifts the foot; a pivot rotates it
about the ball or the heel without travelling. This bake separates the two per foot and per travel segment:
  - travel segment: the ball moves faster than V_MOVE (25 cm/s) horizontally (component space, root-relative motion removed is NOT done:
    the clips are root-motion turns, the floor is the component frame), merged with gaps < 0.07 s;
  - pivot (natural, untouched): the segment's ankle OR ball horizontal travel stays below P_TRAVEL (8 cm) while the other end moves
    (rotation about the heel / the ball);
  - step: both ends travel. The foot (ankle + ball, rigid) is lifted along a smooth bump  h(s) = H * sin(pi s)^1.5, s = normalized
    segment time, H = clamp(K_LIFT * travel, H_MIN, H_MAX) minus the clip's own mid-segment lift (never lowered); legs re-solved to the
    lifted foot with the original knee as hint (v137 solve_leg + leg_guard on write).
Owned clips only. builtins.V215_TC = {'clips': [...], 'dry_run': True, 'K': 0.10, 'HMIN': 3.0, 'HMAX': 8.0}. Prints TC215 [...]."""
import unreal as u, json, math, builtins, pathlib, importlib, sys, shutil
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
cfg = getattr(builtins, 'V234_SC', {}); DRY = bool(cfg.get('dry_run', True))
K = float(cfg.get('K', 0.10)); HMIN = float(cfg.get('HMIN', 3.0)); HMAX = float(cfg.get('HMAX', 8.0)); V_MOVE = 25.0; P_TRAVEL = 8.0
BK = None   # V2.34: backups come from the write manifest (manifest234), never written by the generator
def hdist(a, b): return math.hypot(b[0] - a[0], b[1] - a[1])
def bake(path):
    if not path.startswith('/Game/GraceRanger/'): return {'path': path, 'refused': 'not project-owned'}
    seq = u.load_asset(path); clip = ae.Clip(seq, ['foot_l', 'foot_r', 'ball_l', 'ball_r', 'calf_l', 'calf_r'])
    base = {b: list(v) for b, v in clip.local.items()}; local = {b: list(v) for b, v in clip.local.items()}
    nk = clip.nf; ln = float(u.AnimationLibrary.get_sequence_length(seq)); fr = (nk - 1) / max(ln, 1e-3)
    rec = {'path': path, 'segments': {}}; touched = set()
    for s in ('l', 'r'):
        A = [clip.comp('foot_' + s, f, base) for f in range(nk)]; Bl = [clip.comp('ball_' + s, f, base)[0] for f in range(nk)]
        Kn = [clip.comp('calf_' + s, f, base)[0] for f in range(nk)]
        mv = [False] + [hdist(Bl[f - 1], Bl[f]) * fr > V_MOVE or hdist(A[f - 1][0], A[f][0]) * fr > V_MOVE for f in range(1, nk)]
        segs = []; f = 0
        while f < nk:
            if mv[f]:
                g = f
                while g + 1 < nk and (mv[g + 1] or any(mv[g + 1:min(nk, g + 1 + int(0.07 * fr) + 1)])): g += 1
                segs.append((max(f - 1, 0), min(g + 1, nk - 1))); f = g + 1
            else: f += 1
        out = []
        CLOSE = bool(cfg.get('closing_only', True)); TMAX = float(cfg.get('travel_max', 80.0))
        for si, (a, b) in enumerate(segs):
            ta = sum(hdist(A[i - 1][0], A[i][0]) for i in range(a + 1, b + 1)); tb = sum(hdist(Bl[i - 1], Bl[i]) for i in range(a + 1, b + 1))
            lift0 = max(min(A[i][0][2] - A[a][0][2], Bl[i][2] - Bl[a][2]) for i in range(a, b + 1))   # the clip's own clearance
            if bool(cfg.get('ball_mid', False)):   # V2.34 b: the TOE clearance over the middle 60 % of the segment (an ankle-only lift that drags the toe is not a step)
                m0 = a + int(0.2 * (b - a)); m1 = max(m0 + 1, a + int(0.8 * (b - a)))
                lift0 = min(Bl[i][2] - min(Bl[a][2], Bl[b][2]) for i in range(m0, m1 + 1))
            kind = 'pivot' if min(ta, tb) < P_TRAVEL else 'step'
            # V2.34: only the CLOSING step (the foot's last travel segment, <= TMAX cm) - normal strides / the run-in are never changed
            if CLOSE and kind == 'step' and (si != len(segs) - 1 or max(ta, tb) > TMAX): kind = 'stride'
            H = 0.0
            if kind == 'step':
                H = max(0.0, min(max(K * max(ta, tb), HMIN), HMAX) - max(lift0, 0.0))
            out.append({'t': [round(a / fr, 3), round(b / fr, 3)], 'kind': kind, 'travel_ankle': round(ta, 1), 'travel_ball': round(tb, 1), 'own_lift': round(lift0, 1), 'added': round(H, 1)})
            if H > 0.2 and b - a >= 2:
                for i in range(a, b + 1):
                    x = (i - a) / float(b - a); dz = H * math.sin(math.pi * x) ** 1.5
                    t_, q_ = A[i]; ae.solve_leg(clip, local, s, i, (t_[0], t_[1], t_[2] + dz), q_, (Kn[i][0], Kn[i][1], Kn[i][2] + dz * 0.5))
                touched.update(('thigh_' + s, 'calf_' + s, 'foot_' + s))
        rec['segments'][s] = out
    # check: the feet outside the lifted segments are unchanged, inside they follow target
    err = 0.0
    for f in range(nk):
        for s in ('l', 'r'):
            a0 = clip.comp('foot_' + s, f, base)[0]; a1 = clip.comp('foot_' + s, f, local)[0]
            err = max(err, hdist(a0, a1))
    rec['foot_xy_err_cm'] = round(err, 3); rec['touched'] = sorted(touched)
    if not DRY and touched and err < 0.5:
        ae.write_tracks(seq, local, sorted(touched), note='SHME V2.34 stop closing-step clearance')
        rec['saved'] = bool(u.EditorAssetLibrary.save_loaded_asset(seq, False))
    elif not DRY: rec['not_written'] = 'xy err %.2f or nothing touched' % err
    return rec
res = []
clips = []
for c in cfg.get('clips', []):
    if c.startswith('folder:'):
        clips += sorted(str(a.package_name) + '.' + str(a.asset_name) for a in u.AssetRegistryHelpers.get_asset_registry().get_assets_by_path(c[7:], False) if str(a.asset_class_path.asset_name) == 'AnimSequence')
    else: clips.append(c)
for p in clips:
    try: res.append(bake(p))
    except Exception:
        import traceback; res.append({'path': p, 'err': traceback.format_exc()[-700:]})
(P / 'Saved/Codex/SHME_V234_20261028' / ('sc234_%s.json' % ('dry' if DRY else 'apply'))).write_text(json.dumps(res, indent=1))
print('SC234 ' + json.dumps(res)[:8000])
