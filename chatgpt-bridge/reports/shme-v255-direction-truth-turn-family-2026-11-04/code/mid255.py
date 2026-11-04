"""mid255.py <prefixA:variantA> <prefixB:variantB> [scenario ...] : every key change of a scripted run, read apart: a new command during a turn, a short tap, fast left-right. Per change: speed at the change, reaction, heading and body within 30 deg of the new command, lowest speed, highest speed in the next 1.2 s (free speed shows as more than the speed before), peak g (5-frame window)."""
import sys, math
sys.path.insert(0, 'Tools/SHME_V231_20261026'); import ltp231
def ang(a): return (a + 180.0) % 360.0 - 180.0
def stg(r):
    p = str(r['stage']).split('+')[-1].split('_')
    if p[0] != 'mv' or len(p) < 3: return None
    for x in p[1:]:
        try: return float(x)
        except ValueError:
            if x == 'rel': return None
    return None
def f(x): return '-' if x is None else '%.2f' % x
def rows(L):
    R = [r for r in ltp231.load(L) if 'avx' in r]; T = [r['t'] for r in R]; K = [stg(r) for r in R]; V = [(r['avx'], r['avy']) for r in R]; S = [math.hypot(*v) for v in V]; n = len(R); out = []; w = 5
    for i in range(1, n):
        if K[i] is None or K[i - 1] is None or K[i] == K[i - 1] or T[i] < 3.0: continue
        j = i
        while j + 1 < n and K[j + 1] == K[i]: j += 1
        E = R[i]['cy'] + K[i]; e = (math.cos(math.radians(E)), math.sin(math.radians(E))); v0 = S[max(0, i - 3)]; react = face = dirn = None; run = 0; peak = 0.0; e2 = min(n - 1, i + 72)
        for k in range(i, min(j, e2) + 1):
            if w <= k < n - w:
                d = max(T[k + w] - T[k - w], 1e-3); a = ((V[k + w][0] - V[k - w][0]) / d, (V[k + w][1] - V[k - w][1]) / d); peak = max(peak, math.hypot(*a))
                ok = a[0] * e[0] + a[1] * e[1] > 120.0; run = run + 1 if ok else 0
                if react is None and run >= 3: react = T[k - 2] - T[i]
            if face is None and abs(ang(R[k].get('ay', 0.0) - E)) < 30.0: face = T[k] - T[i]
            if dirn is None and S[k] > 40.0 and abs(ang(math.degrees(math.atan2(V[k][1], V[k][0])) - E)) < 30.0: dirn = T[k] - T[i]
        out.append((T[i], K[i], v0, react, face, dirn, min(S[i:e2 + 1]), max(S[i:e2 + 1]), peak / 981.0))
    return out
PA, VA = sys.argv[1].split(':'); PB, VB = sys.argv[2].split(':')
print('| senaryo | yapı | t | yeni tuş | v0 | ilk tepki | yüz | yön | en düşük v | 1.2 s tepe v | tepe g |'); print('|---|---|---|---|---|---|---|---|---|---|---|')
for s in sys.argv[3:] or ['s54_tap', 's54_mid', 's54_lr']:
    for p, v, nm in ((PA, VA, 'üretim'), (PB, VB, 'aday')):
        for x in rows('%s_%s_%s_r1' % (p, s, v)):
            print('| %s | %s | %.2f | %+.0f | %.0f | %s | %s | %s | %.0f | %.0f | %.2f |' % (s, nm, x[0], x[1], x[2], f(x[3]), f(x[4]), f(x[5]), x[6], x[7], x[8]))
