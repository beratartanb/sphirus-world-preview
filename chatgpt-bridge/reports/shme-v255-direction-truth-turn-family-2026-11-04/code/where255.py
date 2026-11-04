"""where255.py <label> ... : where a hard turn happened: capsule position and height at the key change and at the lowest speed, and the height range of the following 1.5 s, so a terrain scenario can be checked for really turning on the feature."""
import sys, math
sys.path.insert(0, 'Tools/SHME_V231_20261026'); import ltp231
for L in sys.argv[1:]:
    R = [r for r in ltp231.load(L) if 'avx' in r]; prev = None; i = None
    for k, r in enumerate(R):
        s = str(r['stage']).split('+')[-1]
        if prev is not None and s != prev and r['t'] > 3.0 and s.startswith('mv_') and '_rel' not in s: i = k; break
        prev = s
    if i is None: print(L, 'no change'); continue
    W = R[i:i + 100]; km = min(range(len(W)), key=lambda k: math.hypot(W[k]['avx'], W[k]['avy']))
    z = [w['ax'][2] for w in W]; a = R[i]['ax']; b = W[km]['ax']
    print('%-36s key t %.2f at (%.0f, %.0f, %.0f) lowest v t %.2f at (%.0f, %.0f, %.0f) z range %.0f..%.0f' % (L.replace('v255q60_', ''), R[i]['t'], a[0], a[1], a[2], W[km]['t'], b[0], b[1], b[2], min(z), max(z)))
