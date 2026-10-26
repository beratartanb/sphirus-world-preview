"""cols231.py <label> t0 t1 col1 col2 ... : print chosen LTP columns (object paths shortened) in a time window."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ltp231 import load, short
lab, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); cols = sys.argv[4:]
def fmt(v):
    if isinstance(v, tuple): return '(%.0f,%.0f,%.0f)' % v
    if isinstance(v, float): return '%.2f' % v
    s = str(v); return short(s) if '/' in s or "'" in s else s
print('t ' + ' '.join(cols))
for r in load(lab):
    if t0 <= r['t'] <= t1: print('%.3f ' % r['t'] + ' '.join(fmt(r.get(c))[:34] for c in cols))
