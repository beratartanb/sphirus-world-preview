"""rec233.py <label> [...] : V2.33 auto-recentre audit from the FINAL camera (LTP camrot yaw), the control yaw (cy), the travel yaw
(velocity) and the movement path. Per run, after the last key change into a held direction: error |camera yaw - travel yaw| over time,
settle time (error < 20 deg and staying), final error, the camera's peak angular speed / jerk (real time), path straightness while the
same key is held (travel yaw drift after the turn: a circling input frame shows as a large drift), and the control-yaw change.
Prints REC233 lines."""
import sys, os, math, json
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'SHME_V231_20261026'))
from ltp231 import load
def w(a): return (a + 180.0) % 360.0 - 180.0
def yaw_of(s):
    try: return float(str(s).split('Y=')[1].split()[0])
    except Exception: return None
for lab in sys.argv[1:]:
    R = load(lab); rows = []
    # travel direction over a 0.1 s window (FPS independent; per-frame pelvis steps are sway noise at 120 FPS)
    for i, r in enumerate(R):
        cam = yaw_of(r.get('camrot')); vel = None
        j = i
        while j > 0 and r['t'] - R[j]['t'] < 0.1: j -= 1
        if r.get('vb_pelvis') and R[j].get('vb_pelvis') and r['t'] - R[j]['t'] > 0.05:
            dx = r['vb_pelvis'][0] - R[j]['vb_pelvis'][0]; dy = r['vb_pelvis'][1] - R[j]['vb_pelvis'][1]
            if math.hypot(dx, dy) / (r['t'] - R[j]['t']) > 40: vel = math.degrees(math.atan2(dy, dx))
        rows.append((r['t'], cam, float(r.get('cy') or 0.0), vel, r.get('Speed2D', 0.0)))
    mv = [x for x in rows if x[3] is not None and x[1] is not None]
    if len(mv) < 10: print('REC233 %s too few moving rows' % lab); continue
    # the held phase = the last 60 % of the moving rows
    hold = mv[int(len(mv) * 0.4):]
    err = [abs(w(c - v)) for t, c, cy, v, sp in hold]
    settle = None
    for i in range(len(hold)):
        if all(e < 20.0 for e in err[i:]): settle = round(hold[i][0] - hold[0][0], 2); break
    tr = [v for t, c, cy, v, sp in hold]; drift = max(abs(w(a - tr[0])) for a in tr)
    rate = [abs(w(hold[i][1] - hold[i - 1][1])) / max(hold[i][0] - hold[i - 1][0], 1e-3) for i in range(1, len(hold))]
    acc = [abs(rate[i] - rate[i - 1]) / max(hold[i + 1][0] - hold[i][0], 1e-3) for i in range(1, len(rate))]
    print('REC233 %-28s err start %5.1f end %5.1f settle %s s | cam rate max %5.1f deg/s p95 acc %6.0f | travel drift while held %5.1f deg | ctl change %6.1f' % (
        lab, err[0], err[-1], settle, max(rate), sorted(acc)[int(0.95 * len(acc))] if acc else 0, drift, w(hold[-1][2] - hold[0][2])))
