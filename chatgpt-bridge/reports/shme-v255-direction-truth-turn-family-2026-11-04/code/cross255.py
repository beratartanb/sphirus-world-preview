"""cross255.py <stick name> ... : V2.55 crossover check on the generated clip (stick JSON). A foot crosses when, at its touchdown, the LEFT ball lies right of the pelvis or the RIGHT ball left of it, measured across the current
travel direction. Prints every contact: foot, time, lateral offset (+ = its own side, - = crossed), along offset. Crossed by more than 5 cm is flagged."""
import json, math, sys
for nm in sys.argv[1:]:
    j = json.load(open('Saved/Codex/SHME_V255_20261104/stick/%s.json' % nm)); B = {b: i for i, b in enumerate(j['bones'])}; F = j['frames']; dt = j['dt']; R = j['root']; n = len(F); P = j['planted']; bad = 0; rows = []
    for s in 'lr':
        for f in range(1, n):
            if P[s][f] and not P[s][f - 1]:
                a, b = max(0, f - 3), min(n - 1, f + 3); dx, dy = R[b][0] - R[a][0], R[b][1] - R[a][1]; l = math.hypot(dx, dy) or 1.0; fx, fy = dx / l, dy / l
                pe = F[f][B['pelvis']]; ba = F[f][B['ball_' + s]]; rx, ry = ba[0] - pe[0], ba[1] - pe[1]
                al = rx * fx + ry * fy; rt = rx * (fy) + ry * (-fx)     # comp space: forward +Y, right -X -> right of (fx, fy) = (-fy, fx) rotated; sign fixed below
                right = -(rx * fy - ry * fx) if False else (rx * -fy + ry * fx) * -1.0 * -1.0
                # right vector of forward (fx, fy) with right = -X when forward = +Y: (-fy, fx)
                lat = rx * (-fy) + ry * fx
                own = lat if s == 'r' else -lat
                rows.append((f * dt, s.upper(), own, al)); bad += own < -5.0
    print('%s crossed %d' % (nm, bad))
    for t, s, own, al in sorted(rows): print('   %.2f %s own-side %+5.1f along %+5.1f %s' % (t, s, own, al, 'CROSSED' if own < -5.0 else ''))
