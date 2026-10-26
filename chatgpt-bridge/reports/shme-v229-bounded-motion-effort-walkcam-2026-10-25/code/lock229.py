"""lock229.py label [label ...]: control-lock audit (V2.29). For every input event whose heading turns > 90 deg from the current velocity
(world lix/liy vs avx/avy), while the key stays held: t_rev = time until the velocity component along the input becomes positive
(the body stops travelling against the request), against_cm = distance travelled against the request after it, v_against_max = the
largest speed against the request AFTER 0.3 s (a brake decelerates; a lock keeps or gains speed). LOCK = t_rev > 1.2 s or the input is
released before the body ever follows (NOT_FOLLOWED). Prints one line per event and LOCK229 {...}."""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
def f(x, d=0.0):
    try: return float(x)
    except Exception: return d
for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
    p = E / (lab + '.json')
    if not p.exists(): print('LOCK229 %s MISSING' % lab); continue
    R0 = sorted([r for r in json.load(open(p)) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('ax'), list)], key=lambda r: f(r['t']))
    R = []; seen = set()
    for r in R0:
        if f(r['t']) not in seen: seen.add(f(r['t'])); R.append(r)
    n = len(R); T = [f(r['t']) for r in R]
    V = [(f(r.get('avx')), f(r.get('avy'))) for r in R]; I = [(f(r.get('lix')), f(r.get('liy'))) for r in R]
    ev = []
    for k in range(1, n):
        a, b = I[k], I[k - 1]
        if math.hypot(*a) < 0.2: continue
        if math.hypot(*b) > 0.2 and (a[0] * b[0] + a[1] * b[1]) / (math.hypot(*a) * math.hypot(*b)) > 0.0: continue
        s = math.hypot(*V[k - 1])
        if s < 60: continue
        if (V[k - 1][0] * a[0] + V[k - 1][1] * a[1]) / (s * math.hypot(*a)) > -0.1: continue      # not against the travel (> ~95 deg)
        ev.append(k)
    out = []; worst = 0.0; locks = 0
    for k in ev:
        a = I[k]; ua = (a[0] / math.hypot(*a), a[1] / math.hypot(*a)); trev = None; ag = 0.0; vmax = 0.0; rel = None
        for j in range(k, n):
            if math.hypot(*I[j]) < 0.2 or (I[j][0] * ua[0] + I[j][1] * ua[1]) < 0.7 * math.hypot(*I[j]): rel = T[j] - T[k]; break
            along = V[j][0] * ua[0] + V[j][1] * ua[1]
            if along > 0: trev = T[j] - T[k]; break
            dt = T[j] - T[j - 1]; ag += -along * dt
            if T[j] - T[k] > 0.3: vmax = max(vmax, -along)
        lock = (trev is not None and trev > 1.2) or (trev is None and (rel is None or rel > 1.2))
        if lock: locks += 1
        worst = max(worst, trev if trev is not None else (rel or 9.9))
        o = {'t': round(T[k], 2), 'v0': round(math.hypot(*V[k - 1])), 't_rev': round(trev, 2) if trev is not None else None, 'released_after': round(rel, 2) if rel is not None else None, 'against_cm': round(ag, 1), 'v_against_max_after_0.3s': round(vmax), 'lock': lock}
        out.append(o); print('  ' + json.dumps(o))
    print('LOCK229 %s %s' % (lab, json.dumps({'events': len(out), 'locks': locks, 'worst_t_rev': round(worst, 2)})))
