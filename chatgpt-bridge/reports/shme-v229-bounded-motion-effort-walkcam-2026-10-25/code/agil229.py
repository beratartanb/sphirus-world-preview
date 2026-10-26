"""agil229.py label [label ...]: direction-change capability per input event (V2.29 effort / agility audit).
An event = the raw input heading (lix/liy, world) changes by > 45 deg (or input appears / disappears is ignored). For each event:
speed at the request, the old-direction carry (distance travelled along the OLD velocity direction after the request until the velocity
turns > 90 deg away or the next event), minimum speed, time until the velocity heading is within 20 deg of the input heading AND speed
>= 60 % of the pre-event speed (or 150 cm/s) = 'commit', peak horizontal acceleration (m/s2, 3-frame smoothed), heel strikes between the
request and commit (= support steps used), and whether the next event arrived before commit (chained). Prints one line per event and
EVENTS229 {...}."""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
def f(x, d=0.0):
    try: return float(x)
    except Exception: return d
def b(x): return str(x) in ('True', 'true', '1', '1.0')
W = lambda a: (a + 180.0) % 360.0 - 180.0
for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
    p = E / (lab + '.json')
    if not p.exists(): print('AGIL229 %s MISSING' % lab); continue
    R0 = sorted([r for r in json.load(open(p)) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('ax'), list)], key=lambda r: f(r['t']))
    R = []; seen = set()
    for r in R0:
        if f(r['t']) not in seen: seen.add(f(r['t'])); R.append(r)
    T = [f(r['t']) for r in R]; n = len(R)
    V = [(f(r.get('avx')), f(r.get('avy'))) for r in R]; S = [math.hypot(*v) for v in V]
    IH = []
    for r in R:
        lx, ly = f(r.get('lix')), f(r.get('liy')); IH.append(math.degrees(math.atan2(ly, lx)) if math.hypot(lx, ly) > 0.2 else None)
    ev = []
    for k in range(1, n):
        if IH[k] is not None and IH[k - 1] is not None and abs(W(IH[k] - IH[k - 1])) > 45: ev.append(k)
        elif IH[k] is not None and IH[k - 1] is None and S[k] > 100: ev.append(k)
    out = []
    for i, k in enumerate(ev):
        kn = ev[i + 1] if i + 1 < len(ev) else n
        s0 = S[k - 1]; vh0 = math.degrees(math.atan2(V[k - 1][1], V[k - 1][0])) if s0 > 5 else None
        carry = 0.0; smin = s0; kc = None; acc = 0.0; steps = 0; k60 = None; v60 = None
        want = W(IH[k] - vh0) if (vh0 is not None and IH[k] is not None) else None
        for j in range(k, n):
            dt = T[j] - T[j - 1] if j > 0 else 0.033
            if vh0 is not None and S[j] > 5:
                vh = math.degrees(math.atan2(V[j][1], V[j][0]))
                if abs(W(vh - vh0)) < 90 and kc is None: carry += S[j] * dt * math.cos(math.radians(W(vh - vh0)))
            smin = min(smin, S[j])
            if k60 is None and want is not None and S[j] > 5 and abs(want) > 20:
                turned = W(math.degrees(math.atan2(V[j][1], V[j][0])) - vh0)
                if turned * want > 0 and abs(turned) >= 0.6 * abs(want): k60 = j; v60 = S[j]
                elif S[j] < 15 and abs(want) > 150: k60 = j; v60 = S[j]
            if j >= 2 and dt > 0:
                a3 = math.hypot(V[j][0] - V[j - 2][0], V[j][1] - V[j - 2][1]) / max(1e-3, T[j] - T[j - 2]) / 100.0; acc = max(acc, a3)
            if b(R[j].get('cv_HeelStrikeL')) or b(R[j].get('cv_HeelStrikeR')): steps += 1
            ih = IH[j] if IH[j] is not None else IH[k]
            if S[j] > 5 and abs(W(math.degrees(math.atan2(V[j][1], V[j][0])) - ih)) < 20 and S[j] >= min(150.0, 0.6 * max(s0, 1.0)):
                kc = j; break
            if j >= kn + 45: break
        dang = W(IH[k] - (IH[k - 1] if IH[k - 1] is not None else IH[k]))
        out.append({'t': round(T[k], 2), 'turn': round(dang), 'v0': round(s0), 'carry_cm': round(carry, 1), 'vmin': round(smin), 'commit_s': round(T[kc] - T[k], 2) if kc else None, 'steps': steps, 'acc_max': round(acc, 1), 'chained': kc is None or kc > kn, 't60': round(T[k60] - T[k], 2) if k60 else None, 'v60': round(v60) if v60 is not None else None})
    for o in out: print('  %s' % json.dumps(o))
    print('EVENTS229 %s %d events' % (lab, len(out)))
