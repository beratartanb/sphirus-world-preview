# an_hip2.py (2026-11-18 copy of UE59_20261116/an_hip.py: requested vs applied turn, heading of travel) <label> [label2 ...]: turn / hip-swing metrics from hiprec.py recordings (driver vs visible skeleton, per turn event).
import json, math, sys, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Saved', 'UE59Work', 'rec')
def hd(r): return math.degrees(math.atan2(r[7], r[6])) if math.hypot(r[6], r[7]) > 30 else None
def wrap(a): return (a + 180.0) % 360.0 - 180.0
def unwrap(xs):
    o = [xs[0]]
    for x in xs[1:]: o.append(o[-1] + wrap(x - o[-1]))
    return o
def load(lb):
    j = json.load(open(os.path.join(D, lb + '.json'))); R = j['rows']; nb = len(j['bones']); B = {b: i for i, b in enumerate(j['bones'])}
    def bone(r, sk, b): k = 8 + sk * nb * 3 + B[b] * 3; return r[k:k + 3]
    S = {s: 8 + 2 * nb * 3 + i for i, s in enumerate(j['sig'])}
    return j, R, bone, S
def series(R, bone, sk):
    out = []
    for r in R:
        ay = math.radians(r[4]); f = (math.cos(ay), math.sin(ay)); rt = (-math.sin(ay), math.cos(ay))
        p = bone(r, sk, 'pelvis'); tl = bone(r, sk, 'thigh_l'); tr = bone(r, sk, 'thigh_r'); ul = bone(r, sk, 'upperarm_l'); ur = bone(r, sk, 'upperarm_r')
        dx, dy = p[0] - r[1], p[1] - r[2]
        hy = math.degrees(math.atan2(tr[1] - tl[1], tr[0] - tl[0])) - 90.0; cy = math.degrees(math.atan2(ur[1] - ul[1], ur[0] - ul[0])) - 90.0
        roll = math.degrees(math.atan2(tr[2] - tl[2], math.hypot(tr[0] - tl[0], tr[1] - tl[1])))
        out.append(dict(t=r[0], lat=dx * rt[0] + dy * rt[1], fwd=dx * f[0] + dy * f[1], pz=p[2], hip=hy, chest=cy, roll=roll))
    for k in ('hip', 'chest'):
        u = unwrap([o[k] for o in out])
        for o, v in zip(out, u): o[k] = v
    return out
def slip(R, bone, sk, i0, i1):
    zs = sorted(min(bone(r, sk, 'ball_l')[2], bone(r, sk, 'ball_r')[2]) for r in R); g = zs[len(zs) // 20]; d = 0.0; tt = 0.0
    for i in range(max(i0, 1), i1):
        dt = R[i][0] - R[i - 1][0]
        for b in ('ball_l', 'ball_r'):
            a, c = bone(R[i - 1], sk, b), bone(R[i], sk, b)
            if a[2] < g + 2.0 and c[2] < g + 2.0: d += math.hypot(c[0] - a[0], c[1] - a[1]); tt += dt
    return d / tt if tt > 0 else float('nan')
def p2p(xs): return max(xs) - min(xs)
def run(lb):
    j, R, bone, S = load(lb); T = [r[0] for r in R]; cy = unwrap([r[5] for r in R]); ay = unwrap([r[4] for r in R])
    print('=====', lb, 'frames', len(R), 'note', j.get('note'), 'err', j.get('err'))
    ev = []; i = 1
    while i < len(R):
        dt = T[i] - T[i - 1]; rate = (cy[i] - cy[i - 1]) / dt if dt > 0 else 0
        if abs(rate) > 100:
            k = i
            while k + 1 < len(R) and abs((cy[k + 1] - cy[k]) / max(T[k + 1] - T[k], 1e-4)) > 100: k += 1
            ev.append((i - 1, k, cy[k] - cy[i - 1])); i = k + 20
        else: i += 1
    ser = [series(R, bone, 0), series(R, bone, 1)]
    if not ev: print('NO TURN EVENTS'); return
    b1 = ev[0][0]; b0 = max(0, b1 - 75)
    base = []
    for sk in (0, 1):
        s = ser[sk][b0:b1]; lat = [o['lat'] for o in s]; hr = [wrap(o['hip'] - ay[b0 + n]) for n, o in enumerate(s)]
        base.append(dict(latm=sum(lat) / len(lat), lath=p2p(lat) / 2, hiph=p2p(hr) / 2, hipm=sum(hr) / len(hr), rollh=p2p([o['roll'] for o in s]) / 2, slip=slip(R, bone, sk, b0, b1)))
    sp = [math.hypot(r[6], r[7]) for r in R[b0:b1]]
    print('BASE straight speed %.0f | driver lat +-%.1f cm hipyaw +-%.1f roll +-%.1f slip %.1f | visible lat +-%.1f hipyaw +-%.1f roll +-%.1f slip %.1f cm/s' % (
        sum(sp) / len(sp), base[0]['lath'], base[0]['hiph'], base[0]['rollh'], base[0]['slip'], base[1]['lath'], base[1]['hiph'], base[1]['rollh'], base[1]['slip']))
    print('req = requested control yaw of the flick, app = capsule yaw change 2.8 s later, vel = travel-heading change')
    print('turn  req / app / vel | t_cap90 | sk  | latExc cm (x base) | latSpd cm/s | hipLead deg | hipOver deg | chest-hip deg | roll pk | settle s | pz drop | slip cm/s | spdMin')
    for (i0, i1, dl) in ev:
        iw = min(len(R) - 1, i0 + 85); sg = 1.0 if dl > 0 else -1.0; fin = cy[i1]
        tc = next((T[k] - T[i0] for k in range(i0, iw) if sg * (ay[k] - ay[i0]) >= 0.9 * abs(dl)), float('nan'))
        smin = min(math.hypot(r[6], r[7]) for r in R[i0:iw])
        app = ay[iw] - ay[i0]; h0 = next((hd(R[k]) for k in range(i0, max(0, i0 - 30), -1) if hd(R[k]) is not None), None); h1 = hd(R[iw])
        vel = wrap(h1 - h0) if (h0 is not None and h1 is not None) else float('nan')
        if abs(vel) < 90 and abs(dl) > 150: vel = vel + (360 if dl > 0 else -360) if abs(wrap(vel - dl)) > 120 else vel
        for sk, nm in ((0, 'drv'), (1, 'vis')):
            s = ser[sk]; b = base[sk]
            lat = [s[k]['lat'] - b['latm'] for k in range(i0, iw)]; exc = max(abs(x) for x in lat)
            ls = max(abs((s[k]['lat'] - s[k - 1]['lat']) / max(T[k] - T[k - 1], 1e-4)) for k in range(i0 + 1, iw))
            lead = max(sg * (wrap(s[k]['hip'] - ay[k]) - b['hipm']) for k in range(i0, iw))            # hips ahead of capsule in turn direction
            over = max(sg * (s[k]['hip'] - fin) for k in range(i0, iw)) - b['hiph']                       # hips past final heading beyond gait amplitude
            ch = max(abs(wrap(s[k]['chest'] - s[k]['hip'])) for k in range(i0, iw))
            rp = max(abs(s[k]['roll']) for k in range(i0, iw))
            st = float('nan')
            for k in range(iw - 1, i0, -1):
                if abs(s[k]['lat'] - b['latm']) > 1.4 * b['lath'] + 0.5: st = T[k] - T[i0]; break
            pzb = sum(o['pz'] for o in s[b0:b1]) / (b1 - b0); drop = pzb - min(s[k]['pz'] for k in range(i0, iw))
            print('%+5.0f %+5.0f %+5.0f | %6.2f | %s | %5.1f (%.1fx) | %6.0f | %5.1f | %5.1f | %5.1f | %4.1f | %5.2f | %5.1f | %5.1f | %4.0f' % (
                dl, app, vel, tc, nm, exc, exc / max(b['lath'], 0.1), ls, lead, over, ch, rp, st, drop, slip(R, bone, sk, i0, iw), smin))
    for k_ in ('lean_c', 'h_level', 'h_tilt', 'turn_sev', 'turn_w'):
        v = [r[S[k_]] for r in R if r[S[k_]] is not None]
        if v: print('SIG %s min %.2f max %.2f' % (k_, min(v), max(v)))
for lb in sys.argv[1:]: run(lb)
