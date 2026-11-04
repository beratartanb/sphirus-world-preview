"""twist255.py <label> [t0 t1] : V2.55 upper-body twist after a turn. Shoulder line vs hip line in the mesh (mx_upperarm_*, mx_thigh_*), deg, + = shoulders turned to the actor's left; camera error = control yaw vs body yaw. Prints every .25 s and the mean over the window."""
import sys, math
sys.path.insert(0, 'Tools/SHME_V231_20261026'); import ltp231
L = sys.argv[1]; T0 = float(sys.argv[2]) if len(sys.argv) > 2 else 6.8; T1 = float(sys.argv[3]) if len(sys.argv) > 3 else 7.9
def ang(a): return (a + 180.0) % 360.0 - 180.0
R = [r for r in ltp231.load(L) if 'avx' in r and T0 <= r['t'] <= T1]
ks = [k for k in R[0] if k.startswith('mx_')] if R else []
if not ks: print('NO mx keys', list(R[0].keys())[:40] if R else 'no rows'); raise SystemExit
def yl(a, b): return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
tw = []; ce = []
for r in R:
    s = yl(r['mx_upperarm_l'], r['mx_upperarm_r']); h = yl(r['mx_thigh_l'], r['mx_thigh_r']); tw.append(ang(s - h)); ce.append(ang(r['cy'] - r.get('ay', 0.0)))
print('TWIST255 %s window %.1f-%.1f | twist mean %+.1f min %+.1f max %+.1f | control-body yaw mean %+.0f' % (L, T0, T1, sum(tw) / len(tw), min(tw), max(tw), sum(ce) / len(ce)))
