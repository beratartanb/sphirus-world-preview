# an_palm6.py <label> [nx ny]: palm alignment of the supporting hand. From the recorded hand quaternion (component space of the visible body)
# and the actor yaw: world direction of the palm axis (right hand +Y local, left hand -Y local) and of the finger axis (right -X, left +X).
# Reports, while the contact reach is active (> 0.5): angle between the palm direction and the direction INTO the surface (0 = flat on
# it), finger elevation (90 = fingers straight up), and the same for the frame just before the reach (the unaligned arm) for comparison.
import json, sys, math
lab = sys.argv[1]; into = (float(sys.argv[2]), float(sys.argv[3]), 0.0) if len(sys.argv) > 3 else (1.0, 0.0, 0.0)
R = [r for r in json.load(open('Saved/Codex/Grip_20261106/rec/' + lab + '.json'))['rows'] if isinstance(r.get('hook'), dict) and r['hook'].get('pq')]
def rot(q, v):
    x, y, z, w = q; t = [2 * (y * v[2] - z * v[1]), 2 * (z * v[0] - x * v[2]), 2 * (x * v[1] - y * v[0])]
    return [v[0] + w * t[0] + (y * t[2] - z * t[1]), v[1] + w * t[1] + (z * t[0] - x * t[2]), v[2] + w * t[2] + (x * t[1] - y * t[0])]
def world(r, v):
    a = math.radians(r['yaw'] - 90.0); c = math.cos(a); s = math.sin(a); return [v[0] * c - v[1] * s, v[0] * s + v[1] * c, v[2]]
def ang(a, b): return math.degrees(math.acos(max(-1, min(1, sum(a[i] * b[i] for i in range(3))))))
A = {'r': [], 'l': []}; B = {'r': [], 'l': []}
for r in R:
    ct = r['hook'].get('ct'); ra = ct[12] if ct else 0.0; ctm = r['hook'].get('ctm') or [0, 0]
    for s, pa, fa in (('r', [0, 1, 0], [-1, 0, 0]), ('l', [0, -1, 0], [1, 0, 0])):
        q = r['hook']['pq']['hand_' + s]; p = world(r, rot(q, pa)); f = world(r, rot(q, fa)); d = (ang(p, into), math.degrees(math.asin(max(-1, min(1, f[2])))))
        (A if ra > 0.5 else B)[s].append((r['t'], d, r['v_hand_' + s]))
for s in 'rl':
    if not A[s]: continue
    hx = [abs(sum((x[2][i]) * into[i] for i in range(3))) for x in A[s]]
    m = lambda L, k: sum(x[1][k] for x in L) / len(L)
    print('%s hand %s: reach active %d frames | palm vs into-surface angle mean %.0f deg (min %.0f, max %.0f) | finger elevation mean %.0f deg || without reach: palm angle mean %.0f deg, finger elevation %.0f deg' % (
        lab, s, len(A[s]), m(A[s], 0), min(x[1][0] for x in A[s]), max(x[1][0] for x in A[s]), m(A[s], 1), m(B[s], 0), m(B[s], 1)))
