"""clipstat255.py [name-substring ...] : V2.55 what a source clip really does, from src/<name>.json. Per clip: length, root speed profile (start, min,
end), root yaw change, time of brake start / min speed / 50 % / 90 % of the travel turn, foot contacts (foot, t0-t1, world place, slip while planted, heel/toe
pitch at touchdown, along-travel offset from the pelvis at touchdown), pelvis height range, trunk lean range, swing apex."""
import json, math, os, sys
D = 'Saved/Codex/SHME_V255_20261104/src/'
sel = sys.argv[1:]
def hyp(a, b): return math.hypot(a[0] - b[0], a[1] - b[1])
for fn in sorted(os.listdir(D)):
    if not fn.endswith('.json') or (sel and not any(s in fn for s in sel)): continue
    j = json.load(open(D + fn)); B = {b: i for i, b in enumerate(j['bones'])}; F = j['frames']; n = len(F); dt = j['dt']; R = j['root']
    w = max(1, int(round(0.05 / dt)))
    sp = []; hd = []
    for f in range(n):
        a, b = max(0, f - w), min(n - 1, f + w); d = (R[b][0] - R[a][0], R[b][1] - R[a][1]); s = math.hypot(*d) / max(1e-4, (b - a) * dt); sp.append(s); hd.append(math.degrees(math.atan2(d[0], d[1])) if s > 15 else None)
    ry = [math.degrees(math.atan2(v[0], v[1])) for v in j['rootfwd']]
    def uw(x):
        o = [x[0]]
        for y in x[1:]: o.append(o[-1] + ((y - o[-1] + 180) % 360 - 180))
        return o
    ryw = uw(ry); fmin = min(range(n), key=lambda f: sp[f]); s0 = sp[min(n - 1, 2)]; zf = min(min(F[f][B['ball_l']][2], F[f][B['ball_r']][2]) for f in range(n))
    brake = next((f for f in range(n) if sp[f] < 0.9 * s0), None)
    pz = [F[f][B['pelvis']][2] for f in range(n)]
    print('== %s len %.2f dt %.3f n %d | speed %.0f -> min %.0f @%.2f -> end %.0f | brake from %s | root yaw %+.0f (50%% @%s, 90%% @%s) | pelvis z %.0f..%.0f (loop start %.0f)' % (
        j['name'], j['len'], dt, n, s0, sp[fmin], fmin * dt, sp[-3], '%.2f' % (brake * dt) if brake is not None else '-', ryw[-1] - ryw[0],
        next(('%.2f' % (f * dt) for f in range(n) if abs(ryw[f] - ryw[0]) > 0.5 * abs(ryw[-1] - ryw[0])), '-'), next(('%.2f' % (f * dt) for f in range(n) if abs(ryw[f] - ryw[0]) > 0.9 * abs(ryw[-1] - ryw[0])), '-'), min(pz), max(pz), pz[0]))
    out = []
    for s in 'lr':
        ball = [F[f][B['ball_' + s]] for f in range(n)]; foot = [F[f][B['foot_' + s]] for f in range(n)]
        c0 = None
        for f in range(n + 1):
            on = f < n and ball[f][2] - zf < 5.0 and (f == 0 or hyp(ball[f], ball[f - 1]) / dt < 60.0)
            if on and c0 is None: c0 = f
            if not on and c0 is not None:
                if (f - c0) * dt >= 0.06:
                    pel = F[c0][B['pelvis']]; h = hd[c0]; slip = max(hyp(ball[k], ball[c0]) for k in range(c0, f))
                    pitch = math.degrees(math.atan2(foot[c0][2] - ball[c0][2], hyp(foot[c0], ball[c0])))
                    if h is not None:
                        hx, hy = math.sin(math.radians(h)), math.cos(math.radians(h)); al = (ball[c0][0] - pel[0]) * hx + (ball[c0][1] - pel[1]) * hy; la = (ball[c0][0] - pel[0]) * hy - (ball[c0][1] - pel[1]) * hx
                    else: al = la = 0.0
                    out.append((c0 * dt, s.upper(), (f - c0) * dt, slip, pitch, al, la, sp[c0], F[c0][B['pelvis']][2]))
                c0 = None
    for o in sorted(out): print('   %.2f %s %.2fs slip %4.1f heelUp %+4.0f along %+5.0f lat %+5.0f | v %4.0f pelvis %.0f' % o)
    k = [round(sp[f]) for f in range(0, n, max(1, int(round(0.1 / dt))))]; print('   v/0.1s', k)
