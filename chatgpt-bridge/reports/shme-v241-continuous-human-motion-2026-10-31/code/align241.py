"""align241.py <label>... : pelvis / chest / head yaw minus the velocity heading (deg) at +0.6 / +1.2 / +1.8 s after the second request
(balance238.analyse, as TABLES_V240 section 3) + the mean |head - heading| over +0.3..+2.0 s. Prints ALIGN241 lines."""
import sys, os
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H + '/../SHME_V231_20261026', H + '/../SHME_V238_20261030', H + '/../SHME_V239_20261030', H + '/../SHME_V240_20261030', H]
from tables240 import second_req
from balance238 import analyse
for lab in sys.argv[1:]:
    t2 = second_req(lab)
    if t2 is None: print('ALIGN241 %s no second request' % lab); continue
    A = analyse(lab, t2, 2.2, 0.1); rows = A['rows']
    d = lambda r, k: None if r.get(k) is None or r.get('hd') is None else ((r[k] - r['hd']) + 180) % 360 - 180
    def at(tt):
        r = min(rows, key=lambda q: abs(q['t'] - tt)); f = lambda k: '-' if d(r, k) is None else '%d' % round(d(r, k))
        return '%s/%s/%s' % (f('pel'), f('chest'), f('head'))
    hs = [abs(d(r, 'head')) for r in rows if 0.3 <= r['t'] <= 2.0 and d(r, 'head') is not None]
    cs = [abs(d(r, 'chest')) for r in rows if 0.3 <= r['t'] <= 2.0 and d(r, 'chest') is not None]
    print('ALIGN241 %-30s t2 %.2f  pel/chest/head @+0.6 %s @+1.2 %s @+1.8 %s | mean|head| %.1f mean|chest| %.1f' % (lab, t2, at(0.6), at(1.2), at(1.8), sum(hs) / max(len(hs), 1), sum(cs) / max(len(cs), 1)))
