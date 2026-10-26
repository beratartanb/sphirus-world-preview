"""step231.py <label>... : capsule step events (CMC step-up / step-down: root z changes > 8 cm within 0.2 s) and the feet around them.
UP:   per foot after the rise: peak ball height above the new level, HOVER = time from the rise until the ball is within 2 cm of the new level
      and still (< 25 cm/s); the leading foot is the one that plants first on the new level.
DOWN: the leading foot before the drop: HANG = time its ball spends between low+3 cm and high-3 cm (neither on the upper nor the lower floor)
      before the capsule drops; plant delay after the drop.
HEAD: peak head vertical acceleration (m/s2) and head z range in the +-0.4 s window; pelvis z range. Prints STEP231 lines."""
import sys, math, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ltp231 import load, short
def run(lab):
    R = [r for r in load(lab) if isinstance(r.get('mh_root'), tuple) and isinstance(r.get('vb_ball_l'), tuple)]
    ev = []; i = 1
    while i < len(R):
        j = i
        while j < len(R) and R[j]['t'] - R[i - 1]['t'] <= 0.2: j += 1
        dz = R[min(j, len(R) - 1)]['mh_root'][2] - R[i - 1]['mh_root'][2]
        if abs(dz) > 8.0:
            k = i
            while k < len(R) - 1 and abs(R[k]['mh_root'][2] - R[i - 1]['mh_root'][2]) < abs(dz) * 0.9: k += 1
            sg = 1.0 if dz > 0 else -1.0   # merge a CMC step spread over several frames (28 cm in 0.13 s) into one event
            while k < len(R) - 1 and sg * (R[k + 1]['mh_root'][2] - R[k]['mh_root'][2]) > 0.5: k += 1
            dz = R[k]['mh_root'][2] - R[i - 1]['mh_root'][2]
            ev.append((i - 1, k, dz)); i = k + 6; continue
        i += 1
    for a, b, dz in ev:
        z0 = R[a]['mh_root'][2] + 1.85; z1 = R[b]['mh_root'][2] + 1.85; t0 = R[a]['t']; t1 = R[b]['t']
        lo, hi = min(z0, z1), max(z0, z1)
        win = [r for r in R if t0 - 0.6 <= r['t'] <= t1 + 0.8]
        hz = [(r['t'], r['vb_head'][2]) for r in win]
        acc = [abs((hz[k + 1][1] - 2 * hz[k][1] + hz[k - 1][1]) / ((hz[k + 1][0] - hz[k - 1][0]) / 2) ** 2) / 100 for k in range(1, len(hz) - 1)]
        pel = [r['vb_pelvis'][2] for r in win]
        out = {'t': round(t0, 2), 'dz': round(dz, 1), 'head_acc_max': round(max(acc) if acc else 0, 1), 'head_z_range': round(max(h for _, h in hz) - min(h for _, h in hz), 1), 'pelvis_z_range': round(max(pel) - min(pel), 1)}
        for s in 'lr':
            if dz > 0:
                after = [r for r in R if t1 <= r['t'] <= t1 + 1.0]; peak = max((r['vb_ball_' + s][2] - (z1 - 2.0)) for r in after) if after else 0
                hov = None
                for k in range(1, len(after)):
                    p, q = after[k - 1]['vb_ball_' + s], after[k]['vb_ball_' + s]; v = math.hypot(q[0] - p[0], q[1] - p[1]) / max(after[k]['t'] - after[k - 1]['t'], 1e-3)
                    if abs(q[2] - (z1 - 2.0)) < 2.0 and v < 25.0: hov = round(after[k]['t'] - t1, 2); break
                out[s] = {'peak_above': round(peak, 1), 'plant_after_rise': hov}
            else:
                before = [r for r in R if t0 - 1.0 <= r['t'] <= t0]
                hang = sum(after_dt for after_dt in [before[k]['t'] - before[k - 1]['t'] for k in range(1, len(before)) if lo + 3.0 < before[k]['vb_ball_' + s][2] - 0.0 + 2.0 < hi - 3.0])
                after = [r for r in R if t0 <= r['t'] <= t0 + 1.0]; pl = None
                for k in range(1, len(after)):
                    p, q = after[k - 1]['vb_ball_' + s], after[k]['vb_ball_' + s]; v = math.hypot(q[0] - p[0], q[1] - p[1]) / max(after[k]['t'] - after[k - 1]['t'], 1e-3)
                    if abs(q[2] - (lo - 2.0)) < 2.0 and v < 25.0: pl = round(after[k]['t'] - t0, 2); break
                out[s] = {'hang_before_drop': round(hang, 2), 'plant_after_drop': pl}
        print('STEP231 %-30s %s %s' % (lab[-30:], 'UP  ' if dz > 0 else 'DOWN', out))
for lab in sys.argv[1:]:
    try: run(lab)
    except Exception as e: print('STEP231 %s ERR %s' % (lab, e))
