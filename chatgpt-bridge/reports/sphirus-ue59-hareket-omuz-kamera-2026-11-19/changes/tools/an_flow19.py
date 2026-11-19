# an_flow19.py <label>...: hub counters (GR_Wood, GR_Split, GR_Loose, GR_Fire, GR_Busy) and montage changes over time + PASS checks.
import json, sys
for L in sys.argv[1:]:
    R = json.load(open('Saved/Codex/Grip_20261106/rec/%s.json' % L))['rows']; t0 = R[0]['t']; prev = None; print('==', L, 'rows', len(R), 'sim %.1f s' % (R[-1]['t'] - t0))
    for r in R:
        k = (tuple(r.get('hub') or []), r.get('mont'))
        if k != prev: print('  t %6.1f (%5.0f,%5.0f) hub %s mont %s' % (r['t'] - t0, r['x'], r['y'], r.get('hub'), r.get('mont'))); prev = k
    h = [r.get('hub') for r in R if r.get('hub')]
    if h:
        mw = max(x[0] for x in h); ms = max(x[1] for x in h); mf = max(x[3] for x in h)
        print('  CHECK wood picked %s | split pieces collected max %d (need 2) %s | fire state max %d (1 laid, 2 lit) %s' % (mw >= 1, ms, 'PASS' if ms >= 2 else 'FAIL', mf, 'PASS' if mf >= 2 else ('PARTIAL' if mf == 1 else '-')))
