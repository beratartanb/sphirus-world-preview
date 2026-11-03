"""contact231.py <label>... [--t0 x --t1 y] [--v] : V2.31 contact classifier on the VISIBLE feet (LTP vb_ball_* / vb_foot_*), every low-foot episode
(ball within 2 cm of that foot's floor level = 10th percentile + 2 cm) is classified:
  SKIM    the ball never gets still (min horizontal speed > 25 cm/s): a low swing / a landing approach - not a contact
  PIVOT   still, then the foot turns (foot yaw from ankle->ball changes > 15 deg) while the ball drifts < 5 cm: a normal ball pivot
  SLIP    still (< 25 cm/s), then the BALL drifts >= 5 cm horizontally while still low: a planted-foot slide (the defect)
  OK      still and the ball drift < 5 cm
  DRAG    the ball is ON the floor (within 0.8 cm of its 5th-percentile level) while moving > 25 cm/s for >= 5 cm in total: a
          planted foot dragged before it ever got still (s29_swl12 P6: 2-4 m/s at floor level) - a defect like SLIP
'drift' = max horizontal ball distance from where it first got still, until the episode ends (lift or end). Support relocation (a real
small step) lifts the ball above the band and is a new episode, so it never counts as slip. Also prints the clip selected at the worst
slip. Prints CONTACT231 lines: worst SLIP, counts per class, and (--v) every SLIP / PIVOT episode."""
import sys, math, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ltp231 import load, short
def yaw(a, b): return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
def wrap(d): return (d + 180.0) % 360.0 - 180.0
def classify(R, t0=-1e9, t1=1e9):
    R = [r for r in R if isinstance(r.get('vb_ball_l'), tuple) and isinstance(r.get('vb_foot_l'), tuple)]
    eps = []
    for s in 'lr':
        zs = sorted(r['vb_ball_' + s][2] for r in R); zf = zs[len(zs) // 20]; z0 = zs[len(zs) // 10] + 2.0; ep = None
        for i in range(1, len(R)):
            a, b = R[i - 1], R[i]; dt = max(b['t'] - a['t'], 1e-3)
            pb = b['vb_ball_' + s]; pa = a['vb_ball_' + s]; low = pb[2] < z0
            v = math.hypot(pb[0] - pa[0], pb[1] - pa[1]) / dt
            if low and ep is None: ep = {'s': s, 'i0': i, 'still': None, 'drift': 0.0, 'yaw0': None, 'dyaw': 0.0, 'vmin': v, 'v0': v, 'drag': 0.0}
            if ep is not None and low and pb[2] < zf + 0.8 and pa[2] < zf + 0.8 and v > 25.0:
                ep['drag'] += v * dt
                if ep['drag'] > ep.get('dragw', 0.0): ep['dragw'] = ep['drag']; ep.setdefault('iw', i)
            if ep is not None and low:
                ep['vmin'] = min(ep['vmin'], v); ep['i1'] = i
                if ep['still'] is None and v < 25.0: ep['still'] = (pb[0], pb[1]); ep['yaw0'] = yaw(b['vb_foot_' + s], pb); ep['it'] = i
                if ep['still'] is not None:
                    d = math.hypot(pb[0] - ep['still'][0], pb[1] - ep['still'][1])
                    if d > ep['drift']: ep['drift'] = d; ep['iw'] = i
                    ep['dyaw'] = max(ep['dyaw'], abs(wrap(yaw(b['vb_foot_' + s], pb) - ep['yaw0'])))
            if ep is not None and (not low or i == len(R) - 1):
                ep['t'] = R[ep['i0']]['t']; ep['dur'] = R[ep.get('i1', ep['i0'])]['t'] - ep['t']
                if t0 <= ep['t'] <= t1: eps.append(ep)
                ep = None
    for e in eps:
        if e['drag'] >= 5.0 and e['drag'] > e['drift']: e['cls'] = 'DRAG'; e['drift'] = e['drag']
        elif e['still'] is None: e['cls'] = 'SKIM'
        elif e['drift'] >= 5.0: e['cls'] = 'SLIP'
        elif e['dyaw'] > 15.0: e['cls'] = 'PIVOT'
        else: e['cls'] = 'OK'
        k = e.get('iw', e['i0']); e['clip'] = short(R[k].get('av_Phase27_SelectedObject')); e['ct'] = R[k].get('av_Phase27_SelectedTime')
        e['tw'] = R[k]['t']
    return eps
if __name__ == '__main__':
    a = sys.argv[1:]; V = '--v' in a
    t0 = float(a[a.index('--t0') + 1]) if '--t0' in a else -1e9; t1 = float(a[a.index('--t1') + 1]) if '--t1' in a else 1e9
    labs = [x for i, x in enumerate(a) if not x.startswith('--') and not (i > 0 and a[i - 1] in ('--t0', '--t1'))]
    for lab in labs:
        try: eps = classify(load(lab), t0, t1)
        except Exception as ex: print('CONTACT231 %-36s ERR %s' % (lab[-36:], ex)); continue
        n = {}
        for e in eps: n[e['cls']] = n.get(e['cls'], 0) + 1
        sl = [e for e in eps if e['cls'] in ('SLIP', 'DRAG')]; w = max(sl, key=lambda e: e['drift']) if sl else None
        print('CONTACT231 %-36s worst SLIP/DRAG %5.1f cm %s | n %s' % (lab[-36:], w['drift'] if w else 0.0, ('at %.2f %s %s@%.2f' % (w['tw'], w['s'], w['clip'][:30], w['ct'] or 0)) if w else '', n))
        if V:
            for e in sorted(eps, key=lambda e: e['t']):
                if e['cls'] in ('SLIP', 'PIVOT', 'DRAG'): print('   %.2f %s %-5s drift %5.1f dyaw %5.1f v0 %4.0f dur %.2f %s@%.2f' % (e['t'], e['s'], e['cls'], e['drift'], e['dyaw'], e['v0'], e['dur'], e['clip'][:34], e['ct'] or 0))
