"""slide231.py (editor job, read-only): V2.31 audit of the V2.30 re-author log 'support_slide' (40-77 cm on sprint clips). Per clip, in the clip's
own world (root motion included):
  lower_foot  = the V2.30 metric: support = the LOWER foot each frame, drift from the frame it became the lower one (counts swing travel
                whenever both feet are airborne / the lifting foot is still the lower one)
  contact     = contact windows only: ball within 2 cm of the clip's own ball floor AND (window start) ball horizontal speed < 60 cm/s;
                per window first->max horizontal drift; worst window + mean, plus the number of contact windows and the flight fraction
builtins.V231_SLIDE = [asset paths]; prints SLIDE231 {...}."""
import unreal as u, json, math, builtins, pathlib, sys, importlib
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
paths = list(getattr(builtins, 'V231_SLIDE', []))
out = {}
for path in paths:
    seq = u.load_asset(path)
    if not seq: out[path] = 'missing'; continue
    clip = ae.Clip(seq, ['root', 'pelvis', 'foot_l', 'foot_r', 'ball_l', 'ball_r']); L = clip.local; nf = clip.nf
    T = float(seq.get_play_length()); dt = T / max(nf - 1, 1)
    # V2.30 metric
    worst = 0.0; cur = None; anchor = None
    for f in range(nf):
        fl, fr = clip.comp('foot_l', f, L)[0], clip.comp('foot_r', f, L)[0]
        side, p = ('l', fl) if fl[2] < fr[2] else ('r', fr)
        if side != cur: cur = side; anchor = p; continue
        worst = max(worst, math.hypot(p[0] - anchor[0], p[1] - anchor[1]))
    # contact metric
    B = {s: [clip.comp('ball_' + s, f, L)[0] for f in range(nf)] for s in 'lr'}
    z0 = {s: min(b[2] for b in B[s]) for s in 'lr'}
    wins = []; flight = 0
    for f in range(nf):
        if all(B[s][f][2] > z0[s] + 2.0 for s in 'lr'): flight += 1
    for s in 'lr':
        st = None
        for f in range(nf):
            low = B[s][f][2] < z0[s] + 2.0
            v = math.hypot(B[s][f][0] - B[s][f - 1][0], B[s][f][1] - B[s][f - 1][1]) / dt if f else 0.0
            if st is None and low and v < 60.0: st = f
            elif st is not None and not low:
                d = max(math.hypot(B[s][k][0] - B[s][st][0], B[s][k][1] - B[s][st][1]) for k in range(st, f)); wins.append((s, round(st * dt, 2), round((f - st) * dt, 2), round(d, 2))); st = None
        if st is not None:
            d = max(math.hypot(B[s][k][0] - B[s][st][0], B[s][k][1] - B[s][st][1]) for k in range(st, nf)); wins.append((s, round(st * dt, 2), round((nf - st) * dt, 2), round(d, 2)))
    rt = clip.comp('root', nf - 1, L)[0]; r0 = clip.comp('root', 0, L)[0]
    out[path.rsplit('/', 1)[-1]] = {'len': round(T, 3), 'speed': round(math.hypot(rt[0] - r0[0], rt[1] - r0[1]) / max(T, 1e-3), 1), 'lower_foot_metric': round(worst, 1),
        'contact_worst': max((w[3] for w in wins), default=None), 'contact_mean': round(sum(w[3] for w in wins) / len(wins), 2) if wins else None,
        'contact_windows': len(wins), 'flight_frac': round(flight / nf, 2), 'wins': wins[:12]}
print('SLIDE231 ' + json.dumps(out, default=str))
