"""envtime234.py <label>... : is the cinematic orbit tied to the action? CamEnv (computed in every run, applied only with CamEnvEnabled)
marks the brake / reversal / turn / redirect episode + hold. Reports the orbit while the action happens (CamEnv > 0.5) vs after it (CamEnv
< 0.2, moving > 100): mean |orbit| deg, peak, and 'late' = seconds with |orbit| > 4 deg after the action (swing-out after the turn)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'SHME_V231_20261026'))
from ltp231 import load
def f(x, d=0.0):
    try: return float(x)
    except Exception: return d
for lab in sys.argv[1:]:
    R = load(lab); A = []; P = []; late = 0.0
    for i in range(1, len(R)):
        r = R[i]; e = f(r.get('cv_CamEnv')); o = abs(f(r.get('cv_CamOrbitYaw'))); dt = f(r['t']) - f(R[i - 1]['t'])
        if e > 0.5: A.append(o)
        elif e < 0.2 and f(r['Speed2D']) > 100: P.append(o); late += dt if o > 4.0 else 0.0
    m = lambda x: sum(x) / len(x) if x else 0.0
    print('ENV234 %-36s during: mean %4.1f peak %4.1f (n %d) | after: mean %4.1f peak %4.1f late>4deg %.2f s' % (lab, m(A), max(A or [0]), len(A), m(P), max(P or [0]), late))
