"""arms228.py label [label ...]: arm / head / torso continuity across the authored clip's handover to the loop (and at the entry). Per run:
for each SHM226 clip span: the hand positions relative to the pelvis in the actor frame (forward / lateral), the per-frame hand displacement
(cm, world minus pelvis travel) at the entry frame, inside the clip, and in the exit window [exit-0.1, exit+0.5] (a second "preparation"
= a large hand excursion or a reversal of the swing direction right after the handover), the head position change relative to the pelvis in
the exit window, and the chest (spine_03) yaw vs pelvis yaw swing (torso counter-rotation amplitude) before vs after the handover.
Reports: max hand jump entry / in-clip / exit, swing reversal count in the exit window, head jump, chest-pelvis yaw range before/after."""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
def f(x, d=0.0):
    try: return float(x)
    except Exception: return d
def rel(r, key):
    p = r.get(key); pv = r.get('vb_pelvis')
    if not (isinstance(p, list) and isinstance(pv, list)): return None
    yaw = math.radians(f(r.get('ay'))); c, s = math.cos(yaw), math.sin(yaw)
    dx, dy = p[0] - pv[0], p[1] - pv[1]
    return (dx * c + dy * s, -dx * s + dy * c, p[2] - pv[2])
def yaw_of(r, bone):
    X = r.get('vax_' + bone); Z = r.get('vaz_' + bone)
    if not (isinstance(X, list) and isinstance(Z, list)): return None
    Y = [Z[1] * X[2] - Z[2] * X[1], Z[2] * X[0] - Z[0] * X[2], Z[0] * X[1] - Z[1] * X[0]]
    return math.degrees(math.atan2(Y[1], Y[0]))
def wrap(a): return (a + 180.0) % 360.0 - 180.0
for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
    p = E / (lab + '.json')
    if not p.exists(): print('ARMS228 %s MISSING' % lab); continue
    R = sorted([r for r in json.load(open(p)) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('vb_pelvis'), list)], key=lambda r: f(r['t']))
    n = len(R); T = [f(r['t']) for r in R]
    hk = 'vx_hand_l' if isinstance(R[len(R) // 2].get('vx_hand_l'), list) else None
    if not hk: print('ARMS228 %s no hand telemetry' % lab); continue
    sel = ['JogRev' in str(r.get('av_Phase27_SelectedObject')) or 'Pivot' in str(r.get('av_Phase27_SelectedObject')) for r in R]
    spans = []; k = 0
    while k < n:
        if sel[k]:
            j = k
            while j + 1 < n and sel[j + 1]: j += 1
            spans.append((k, j)); k = j + 1
        else: k += 1
    def hand_jump(k):
        out = 0.0
        for key in ('vx_hand_l', 'vx_hand_r'):
            a, b = rel(R[k], key), rel(R[k - 1], key)
            if a and b: out = max(out, math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]))
        return out
    for (a, c) in spans:
        name = str(R[c].get('av_Phase27_SelectedObject'))[-12:]
        ex0 = next((k for k in range(a, n) if T[k] >= T[c] - 0.1), c); ex1 = next((k for k in range(c, n) if T[k] >= T[c] + 0.5), n - 1)
        j_entry = hand_jump(a) if a > 0 else 0.0
        j_in = max((hand_jump(k) for k in range(a + 1, c + 1)), default=0.0)
        j_exit = max((hand_jump(k) for k in range(max(ex0, 1), ex1 + 1)), default=0.0)
        # swing reversals of the left hand forward coordinate in the exit window
        fw = [rel(R[k], 'vx_hand_l')[0] for k in range(ex0, ex1 + 1) if rel(R[k], 'vx_hand_l')]
        rev = sum(1 for i in range(1, len(fw) - 1) if (fw[i] - fw[i - 1]) * (fw[i + 1] - fw[i]) < 0 and abs(fw[i + 1] - fw[i]) > 0.5)
        hj = 0.0
        for k in range(max(ex0, 1), ex1 + 1):
            h1, h0 = rel(R[k], 'vb_head'), rel(R[k - 1], 'vb_head')
            if h1 and h0: hj = max(hj, math.hypot(h1[0] - h0[0], h1[1] - h0[1], h1[2] - h0[2]))
        def cp_range(k0, k1):
            vals = []
            for k in range(k0, k1 + 1):
                cy, py = yaw_of(R[k], 'spine_03'), yaw_of(R[k], 'pelvis')
                if cy is not None and py is not None: vals.append(wrap(cy - py))
            return (min(vals), max(vals)) if vals else (float('nan'), float('nan'))
        b0 = next((k for k in range(a, n) if T[k] >= T[c] - 0.5), a)
        pre = cp_range(b0, c); post = cp_range(c, ex1)
        print('ARMS228 %-28s %s %.2f..%.2f | hand jump entry %.1f in-clip %.1f exit-win %.1f cm | L-hand swing reversals in exit-win %d | head jump exit-win %.1f cm | chest-pelvis yaw pre %+.0f..%+.0f post %+.0f..%+.0f' % (
            lab[-28:], name, T[a], T[c], j_entry, j_in, j_exit, rev, hj, pre[0], pre[1], post[0], post[1]))
