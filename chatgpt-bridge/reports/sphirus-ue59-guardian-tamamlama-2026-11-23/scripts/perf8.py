# perf8.py <label...> : real (wall) frame time per recorded frame (row 'rdt'), editor PIE data runs; second block = frames with contact state != 0
import json, sys, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Saved', 'Codex', 'Grip_20261106', 'rec')
def rows(l):
    j = json.load(open(os.path.join(D, l + '.json'), encoding='utf8')); return j['rows'] if isinstance(j, dict) else j
def line(l, v):
    v = sorted(x * 1000.0 for x in v if x and x > 0); n = len(v)
    if not n: return '%-22s no rdt' % l
    q = lambda p: v[min(n - 1, int(p * n))]
    return '%-22s n %5d | real frame time ms: p50 %5.1f  p95 %5.1f  p99 %5.1f  max %6.1f | frames > 2 x p50: %d' % (l, n, q(.5), q(.95), q(.99), v[-1], sum(1 for x in v if x > 2 * q(.5)))
for l in sys.argv[1:]:
    try: r = rows(l)
    except Exception as e: print(l, 'ERR', e); continue
    print(line(l, [x.get('rdt') for x in r]))
    c = [x.get('rdt') for x in r if (x.get('ct') or {}).get('st', 0) not in (0, None)] if isinstance(r[0].get('ct'), dict) else []
    if c: print('  reaction only  ' + line(l, c))
