# an_fl8.py <label>...: fall timeline from hk_fl8 rows (state/phase changes, ground contact time, roll tries, blocked waits, get-up position jump).
import json, sys, math
for n in sys.argv[1:]:
    R = json.load(open('C:/Users/berat/Documents/Unreal Projects/sphirus_UE59/Saved/Codex/Grip_20261106/rec/%s.json' % n))['rows']; prev = None; out = []; pj = 0.0; pr = None
    for r in R:
        f = r['hook'].get('fl8')
        if not f: continue
        key = (f[0], f[2], f[4], f[6], f[8], f[10])
        if key != prev: out.append('t%.2f st%.0f T%.2f ph%.0f gnd%.0f tries%.0f free%.0f blk%.0f prone%.0f ko%.0f rcN%.0f %s z%.0f' % (r['t'], f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10], r['z']))
        if pr is not None: pj = max(pj, math.dist((r['x'], r['y'], r['z']), pr))
        pr = (r['x'], r['y'], r['z']); prev = key
    print('==', n, 'max per-frame capsule jump %.1f cm' % pj, 'err', [r['hook'].get('flerr') for r in R if r['hook'].get('flerr')][:1])
    for x in out[:40]: print('  ', x)
