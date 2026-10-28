"""worst234.py <tag> <scen:variant> ... : worst planted-ball slide / drag (contact231) and its clip per run label v234<tag>_<scen>_<variant>_r1."""
import sys, os
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H + '/../SHME_V232_20261027', H + '/../SHME_V231_20261026']
from ltp231 import load
from contact231 import classify
tag = sys.argv[1]
for sv in sys.argv[2:]:
    s, v = sv.rsplit(':', 1)
    try: R = load('v234%s_%s_%s_r1' % (tag, s, v))
    except Exception: print('%-16s %-8s missing' % (s, v)); continue
    eps = sorted([e for e in classify(R) if e['cls'] in ('SLIP', 'DRAG')], key=lambda e: -e['drift'])
    print('%-16s %-8s worst %5.1f %s' % (s, v, eps[0]['drift'] if eps else 0.0, (eps[0]['clip'] or '')[:34] if eps else ''))
