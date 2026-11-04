"""score255.py <prefixA:variantA> <prefixB:variantB> [scenario ...] : V2.55 hard-turn scorecard. The brief asks that the four things are read apart, so they are measured apart, on the same frames, from the moment the key changes:
  react  first time the acceleration points toward the command by > 120 cm/s2 for 3 frames
  face   the body yaw within 30 deg of the command
  dir    the travel heading within 30 deg of the command at > 40 cm/s
  push   the speed back at 80 % of the speed before the change (measured after the lowest speed)
plus the lowest speed, the peak horizontal acceleration (g, 5-frame window) and the time travelled with the body more than 120 deg off the travel (backward).
Command = control yaw + key angle at the change. Prints one markdown row per scenario and side."""
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
def score(L):
    R = [r for r in ltp231.load(L) if 'avx' in r]; T = [r['t'] for r in R]; K = [stg(r) for r in R]
    i = next((k for k in range(1, len(R)) if K[k] is not None and K[k - 1] is not None and K[k] != K[k - 1] and T[k] > 3.0), None)
    if i is None: return None
    H = 1.0 / 60.0; n = len(R); V = [(r['avx'], r['avy']) for r in R]; S = [math.hypot(*v) for v in V]
    E = R[i]['cy'] + K[i]; e = (math.cos(math.radians(E)), math.sin(math.radians(E))); v0 = S[max(0, i - 3)]; j = i
    while j + 1 < n and K[j + 1] == K[i]: j += 1
    w = 5; A = [None] * n
    for k in range(w, n - w):
        d = max(T[k + w] - T[k - w], 1e-3); A[k] = ((V[k + w][0] - V[k - w][0]) / d, (V[k + w][1] - V[k - w][1]) / d)
    react = face = dirn = push = None; run = 0; peak = 0.0; back = 0.0; kmin = min(range(i, j + 1), key=lambda k: S[k])
    for k in range(i, j + 1):
        if A[k]:
            peak = max(peak, math.hypot(*A[k]))
            ok = A[k][0] * e[0] + A[k][1] * e[1] > 120.0; run = run + 1 if ok else 0
            if react is None and run >= 3: react = T[k - 2] - T[i]
        if face is None and abs(ang(R[k].get('ay', 0.0) - E)) < 30.0: face = T[k] - T[i]
        hd = math.degrees(math.atan2(V[k][1], V[k][0]))
        if dirn is None and S[k] > 40.0 and abs(ang(hd - E)) < 30.0: dirn = T[k] - T[i]
        if k >= kmin and push is None and S[k] >= 0.8 * v0: push = T[k] - T[i]
        if S[k] > 40.0 and abs(ang(R[k].get('ay', 0.0) - hd)) > 120.0 and k + 1 < n: back += T[k + 1] - T[k]
    return dict(v0=v0, chg=ang(E - math.degrees(math.atan2(V[i][1], V[i][0]))), react=react, face=face, dirn=dirn, push=push, vmin=S[kmin], g=peak / 981.0, back=back)
def f(x): return '-' if x is None else '%.2f' % x
PA, VA = sys.argv[1].split(':'); PB, VB = sys.argv[2].split(':')
SC = sys.argv[3:] or ['s54_revR', 's54_revL', 's54_r135', 's54_r90', 's54_l90', 'j54_rev', 'j54_r135', 'j54_r90', 'j38_c90l', 'w54_rev']
print('| senaryo | yapı | v0 | ilk tepki s | yüz s | yön s | yeniden hız s | en düşük v | tepe g | geri s |'); print('|---|---|---|---|---|---|---|---|---|---|')
for s in SC:
    for p, v, nm in ((PA, VA, 'üretim'), (PB, VB, 'aday')):
        try: x = score('%s_%s_%s_r1' % (p, s, v))
        except Exception as ex: x = None
        if not x: print('| %s | %s | yok |' % (s, nm)); continue
        print('| %s | %s | %.0f | %s | %s | %s | %s | %.0f | %.2f | %.2f |' % (s, nm, x['v0'], f(x['react']), f(x['face']), f(x['dirn']), f(x['push']), x['vmin'], x['g'], x['back']))
