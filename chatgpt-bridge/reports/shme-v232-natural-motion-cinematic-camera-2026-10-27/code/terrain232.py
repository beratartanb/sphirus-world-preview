"""terrain232.py <label>... : V2.32 step up / down audit (ter_drop_walk / ter_step2 / ter_drop_jog boxes): every capsule step (cumulative z
change > 12 cm within 0.3 s) -> per foot: the swing that crosses the step (lift -> land): peak height above its DESTINATION ground,
hover = seconds the ball is more than 6 cm above that ground while within 25 cm (horizontal) of its landing point, early lift = how high the
trailing foot rose BEFORE its swing started (leg reach), the pelvis lag (visible pelvis height above the capsule base vs its value 1 s
before the step) max and the time it needs to come within 3 cm, the head vertical acceleration p95 around the step (m/s2). TERRAIN232 lines."""
import sys, os, math, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'SHME_V231_20261026'))
from ltp231 import load
for lab in sys.argv[1:]:
    R = [r for r in load(lab) if isinstance(r.get('mh_root'), tuple) and isinstance(r.get('vb_ball_l'), tuple)]
    Z = [r['mh_root'][2] for r in R]; T = [r['t'] for r in R]
    steps = []; i = 1
    while i < len(R):
        j = i
        while j < len(R) and T[j] - T[i] < 0.3: j += 1
        dz = Z[min(j, len(R) - 1)] - Z[i - 1]
        if abs(dz) > 12.0 and (not steps or T[i] - steps[-1][0] > 1.0):
            steps.append((T[i], dz, i)); i = j
        else: i += 1
    for t0, dz, i0 in steps:
        z0 = Z[i0 - 1]; z1 = z0 + dz
        out = {'t': round(t0, 2), 'dz': round(dz, 1)}
        pre = [r for r in R if t0 - 1.2 <= r['t'] <= t0 - 0.2]
        prel = sorted(r['vb_pelvis'][2] - r['mh_root'][2] for r in pre)[len(pre) // 2] if pre else None
        W = [r for r in R if t0 - 0.6 <= r['t'] <= t0 + 1.5]
        feet = {}
        for s in 'lr':
            B = [(r['t'], r['vb_ball_' + s]) for r in W]
            # swing segments by horizontal speed
            segs = []; cur = None
            for k in range(1, len(B)):
                dt = max(B[k][0] - B[k - 1][0], 1e-3); v = math.hypot(B[k][1][0] - B[k - 1][1][0], B[k][1][1] - B[k - 1][1][1]) / dt
                if v > 40.0:
                    if cur is None: cur = [k - 1, k]
                    else: cur[1] = k
                elif cur is not None: segs.append(cur); cur = None
            if cur: segs.append(cur)
            best = None
            for a, b in segs:
                za, zb = B[a][1][2], B[b][1][2]
                if (dz > 0 and zb - za > 0.6 * dz) or (dz < 0 and za - zb > 0.6 * -dz): best = (a, b); break
            if not best: feet[s] = None; continue
            a, b = best; dest = B[b][1][2]; land = B[b][1]
            peak = max(B[k][1][2] for k in range(a, b + 1)) - dest
            hov = sum(B[k][0] - B[k - 1][0] for k in range(a + 1, b + 1) if B[k][1][2] - dest > 6.0 and math.hypot(B[k][1][0] - land[0], B[k][1][1] - land[1]) < 25.0)
            early = B[a][1][2] - min(B[k][1][2] for k in range(max(0, a - 15), a + 1)) if dz > 0 else 0.0
            feet[s] = {'lift_t': round(B[a][0], 2), 'land_t': round(B[b][0], 2), 'peak_over_dest': round(peak, 1), 'hover_s': round(hov, 2), 'early_lift': round(early, 1)}
        out['feet'] = feet
        if prel is not None:
            lag = [(r['t'], prel - (r['vb_pelvis'][2] - r['mh_root'][2])) for r in R if t0 <= r['t'] <= t0 + 2.0]
            mx = max(lag, key=lambda x: abs(x[1])); back = next((t for t, l in lag if t > mx[0] and abs(l) < 3.0), None)
            out['pelvis_lag_max'] = round(mx[1], 1); out['pelvis_settle_s'] = round(back - t0, 2) if back else None
        H = [(r['t'], r['vb_head'][2]) for r in R if t0 - 0.5 <= r['t'] <= t0 + 1.0]
        acc = [abs((H[k + 1][1] - 2 * H[k][1] + H[k - 1][1]) / max((H[k + 1][0] - H[k - 1][0]) / 2.0, 1e-3) ** 2) / 100.0 for k in range(1, len(H) - 1)]
        out['head_acc_p95'] = round(sorted(acc)[int(0.95 * len(acc))], 1) if acc else None
        print('TERRAIN232 %s %s' % (lab, json.dumps(out)))
