"""knee255.py <stick name> ... : V2.55 leg quality on a generated clip (stick JSON, local data): per frame the knee swivel = angle of the knee off the hip-ankle line, measured around that line against the foot's forward direction
(0 = knee over the toes, + = outward); knee flexion; swivel rate. Flags a sudden knee direction change (> 12 deg per frame with the knee really bent) and a knee far off the toes while loaded."""
import json, math, sys
def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def nrm(a):
    l = math.sqrt(dot(a, a)) or 1.0; return (a[0] / l, a[1] / l, a[2] / l)
for nm in sys.argv[1:]:
    j = json.load(open('Saved/Codex/SHME_V255_20261104/stick/%s.json' % nm)); B = {b: i for i, b in enumerate(j['bones'])}; F = j['frames']; dt = j['dt']; n = len(F); P = j['planted']
    print('==', nm, 'frames', n)
    for s in 'lr':
        sw = []; fx = []
        for f in range(n):
            H, K, A, Bl = (F[f][B[x + s]] for x in ('thigh_', 'calf_', 'foot_', 'ball_'))
            ax = nrm(sub(A, H)); kv = sub(K, H); kp = nrm(sub(kv, tuple(ax[i] * dot(kv, ax) for i in range(3))))
            fd = sub(Bl, A); fp = nrm(sub(fd, tuple(ax[i] * dot(fd, ax) for i in range(3))))
            a = math.degrees(math.atan2(dot(cross(fp, kp), ax), dot(fp, kp))); a = a if s == 'r' else -a
            sw.append(a); u = nrm(sub(H, K)); v = nrm(sub(A, K)); fx.append(180.0 - math.degrees(math.acos(max(-1, min(1, dot(u, v))))))
        rates = []
        for f in range(1, n):
            d = (sw[f] - sw[f - 1] + 180.0) % 360.0 - 180.0
            if fx[f] > 25.0: rates.append((abs(d), f))
        rates.sort(reverse=True)
        load = [(abs(sw[f]), f) for f in range(n) if P[s][f] and fx[f] > 25.0]; load.sort(reverse=True)
        print('  %s swivel rate worst %s | loaded knee off toes worst %s | flex max %.0f' % (s, ' '.join('%.0f@%.2f' % (r, f * dt) for r, f in rates[:3]), ' '.join('%.0f@%.2f' % (r, f * dt) for r, f in load[:3]), max(fx)))
        print('    swivel every .1 s:', ' '.join('%+.0f' % sw[f] for f in range(0, n, 3)))
