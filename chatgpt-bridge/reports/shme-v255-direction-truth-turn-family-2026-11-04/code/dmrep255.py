"""dmrep255.py <prefix> <variant> : V2.55 direction matrix table. For every key swap held >= 1.5 s while moving: the direction the keys mean on screen at the swap (E), the travel heading 1.8 s later, the error, the time until the
travel is within 30 deg of E, the side the body turned, the longest time the acceleration pointed away from the command. FAIL = final error > 20 deg or body turned the long way for a request under 150 deg."""
import sys, math
sys.path.insert(0, 'Tools/SHME_V231_20261026'); import ltp231
P, VAR = sys.argv[1], sys.argv[2]
def ang(a): return (a + 180.0) % 360.0 - 180.0
def stg(r):
    p = str(r['stage']).split('+')[-1].split('_')
    if p[0] == 'mv' and p[1].startswith('kb') and len(p) >= 5: return (None if p[2] == 'rel' else float(p[2])), p[4]
    return None, '0'
tot = {}; bad = []
for gait in ('walk', 'jog', 'sprint'):
    for cam in ('0', '60', 'm120'):
        L = '%s_fz_dm_%s_%s_%s_r1' % (P, gait, cam, VAR)
        try: rows = [r for r in ltp231.load(L) if 'avx' in r]
        except Exception as e: print('MISSING', L); continue
        T = [r['t'] for r in rows]; K = [stg(r) for r in rows]; n = 0; f = 0; th = []
        for i in range(1, len(rows)):
            if K[i][0] is None or K[i - 1][0] is None or K[i][1] == K[i - 1][1]: continue
            j = i
            while j + 1 < len(rows) and K[j + 1][1] == K[i][1]: j += 1
            if T[j] - T[i] < 1.5: continue
            s0 = math.hypot(rows[i]['avx'], rows[i]['avy'])
            if s0 < 80: continue
            E = rows[i]['cy'] + K[i][0]; v0 = math.degrees(math.atan2(rows[i]['avy'], rows[i]['avx'])); chg = ang(E - v0)
            k = min(j, i + int(1.8 * 60)); vh = math.degrees(math.atan2(rows[k]['avy'], rows[k]['avx'])); err = abs(ang(vh - E))
            t30 = next((T[q] - T[i] for q in range(i, j) if math.hypot(rows[q]['avx'], rows[q]['avy']) > 40 and abs(ang(math.degrees(math.atan2(rows[q]['avy'], rows[q]['avx'])) - E)) < 30), None)
            ys = 0.0
            for q in range(i + 1, k): ys += ang(rows[q]['ay'] - rows[q - 1]['ay'])
            long_way = abs(chg) < 150 and abs(ys) > 30 and ys * chg < 0
            n += 1; ok = err <= 20 and not long_way
            if t30 is not None: th.append(t30)
            if not ok: f += 1; bad.append('%s %s t=%.2f %s v0 %.0f chg %+.0f err %.0f yaw %+.0f t30 %s' % (gait, cam, T[i], K[i][1], s0, chg, err, ys, '%.2f' % t30 if t30 is not None else '-'))
        th.sort(); tot[(gait, cam)] = (n, f, th[len(th) // 2] if th else None, th[-1] if th else None)
print('DM255 %s %s (gait cam: events / fail / median t30 / worst t30)' % (P, VAR))
for k, v in tot.items(): print('  %-6s %-5s %2d / %d / %s / %s' % (k[0], k[1], v[0], v[1], '%.2f' % v[2] if v[2] is not None else '-', '%.2f' % v[3] if v[3] is not None else '-'))
print('TOTAL', sum(v[0] for v in tot.values()), 'fail', sum(v[1] for v in tot.values()))
for b in bad[:24]: print('  FAIL', b)
