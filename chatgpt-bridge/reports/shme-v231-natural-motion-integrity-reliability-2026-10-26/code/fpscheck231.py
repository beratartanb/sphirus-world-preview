"""fpscheck231.py <label> <fps>: the run's world delta (LTP wdt) must be the fixed 1/fps on >= 98 % of the move frames; prints FPSCHECK ok/INVALID_FPS."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ltp231 import load
lab, fps = sys.argv[1], float(sys.argv[2])
try: R = load(lab)
except Exception as e: print('FPSCHECK %s NO_LTP %s' % (lab, e)); raise SystemExit
w = [r.get('wdt') for r in R if isinstance(r.get('wdt'), float) and r.get('t', 0) > 0.5]
good = sum(1 for x in w if abs(x - 1.0 / fps) < 0.002) / max(len(w), 1)
print('FPSCHECK %s %s fixed=%.3f n=%d' % (lab, 'ok' if good >= 0.98 else 'INVALID_FPS', good, len(w)))
