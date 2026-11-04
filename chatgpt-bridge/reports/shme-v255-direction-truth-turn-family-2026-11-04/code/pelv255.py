"""pelv255.py <name> [t0 t1] : V2.55 real body speed of a source clip (pelvis in world = root motion + pelvis offset), not the authored root track.
Per 0.1 s: root speed, pelvis speed, pelvis velocity heading vs the first heading, facing (hip line normal), pelvis height, trunk lean, foot on ground."""
import json, math, sys
j = json.load(open('Saved/Codex/SHME_V255_20261104/src/%s.json' % sys.argv[1])); B = {b: i for i, b in enumerate(j['bones'])}; F = j['frames']; n = len(F); dt = j['dt']
t0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0; t1 = float(sys.argv[3]) if len(sys.argv) > 3 else 9.0
w = max(1, int(round(0.05 / dt)))
zf = min(min(F[f][B['ball_l']][2], F[f][B['ball_r']][2]) for f in range(n))
def P(f, b): return F[f][B[b]]
h0 = None
step = max(1, int(round(0.1 / dt)))
print('name %s dt %.4f' % (j['name'], dt))
for f in range(0, n, step):
    a, b = max(0, f - w), min(n - 1, f + w); T = (b - a) * dt
    pv = ((P(b, 'pelvis')[0] - P(a, 'pelvis')[0]) / T, (P(b, 'pelvis')[1] - P(a, 'pelvis')[1]) / T); rv = ((P(b, 'root')[0] - P(a, 'root')[0]) / T, (P(b, 'root')[1] - P(a, 'root')[1]) / T)
    sp = math.hypot(*pv); hd = math.degrees(math.atan2(pv[0], pv[1]))
    if h0 is None and sp > 40: h0 = hd
    tl, tr = P(f, 'thigh_l'), P(f, 'thigh_r'); dx, dy = tr[0] - tl[0], tr[1] - tl[1]; face = math.degrees(math.atan2(-dy, dx)) if False else math.degrees(math.atan2(dy, -dx)) * -1
    sl, sr = P(f, 'upperarm_l'), P(f, 'upperarm_r'); sx, sy = sr[0] - sl[0], sr[1] - sl[1]; sface = math.degrees(math.atan2(sy, -sx)) * -1
    p, c = P(f, 'pelvis'), P(f, 'spine_05'); fa = math.radians(face); fx, fy = math.sin(fa), math.cos(fa)
    lean = math.degrees(math.atan2((c[0] - p[0]) * fx + (c[1] - p[1]) * fy, c[2] - p[2]))
    t = f * dt
    if t0 <= t <= t1:
        print('%.2f root %4.0f pelvis %4.0f head %+5.0f hip %+5.0f sh %+5.0f pz %3.0f lean %+4.0f %s%s ball z L %2.0f R %2.0f' % (t, math.hypot(*rv), sp, ((hd - (h0 or 0) + 180) % 360) - 180, face, sface, p[2], lean, 'L' if P(f, 'ball_l')[2] - zf < 5 else '.', 'R' if P(f, 'ball_r')[2] - zf < 5 else '.', P(f, 'ball_l')[2] - zf, P(f, 'ball_r')[2] - zf))
