"""trans231.py <label>... [--sum] : transition continuity audit (V2.31 item 5). For every Motion Matching clip CHANGE (selected object differs
from the previous frame and stays >= 2 frames), in the 0.35 s after it:
  drag    worst planted-foot SLIP/DRAG (contact231 episodes overlapping the window)
  twist   peak |d(chest yaw - pelvis yaw)/dt| (deg/s; chest yaw from the shoulder line, pelvis yaw from the thigh line) - a body wrung
          to reach the new clip's pose ("ters / uygunsuz poz")
  back    pelvis facing more than 120 deg from the travel direction while moving > 120 cm/s (an inverted body) - frames
  head    peak head acceleration (m/s2, 3-point second difference)
Type by the clip families before -> after: IDLE / WALK / JOG / SPRINT / STOP / START / PIVOT / REV (authored reversal) / TURN (TIP) / OTHER.
--sum prints only the per-type summary (count, worst drag, worst twist, back frames, worst head). Prints TRANS231 lines."""
import sys, math, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ltp231 import load, short
from contact231 import classify
def fam(o):
    s = o.lower()
    if o.startswith(('SHM226_JogRev', 'SHM231S', 'SHM231L', 'SHM214_RevPush', 'SHM216_RevTurn')): return 'REV'
    if 'idle' in s: return 'IDLE'
    if 'stop' in s: return 'STOP'
    if 'start' in s or 'w2s' in s or 'j2s' in s or 'walktosprint' in s or 'backlink' in s: return 'START'
    if 'pivot' in s or 'cut_' in s: return 'PIVOT'
    if 'turn' in s: return 'TURN'
    if 'sprint' in s: return 'SPRINT'
    if 'jog' in s or 'run' in s: return 'JOG'
    if 'walk' in s: return 'WALK'
    return 'OTHER'
def yaw2(a, b): return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
def wr(d): return (d + 180.0) % 360.0 - 180.0
def audit(lab):
    R = [r for r in load(lab) if isinstance(r.get('vb_sh_l'), tuple) and isinstance(r.get('vx_thigh_l'), tuple) and isinstance(r.get('vb_head'), tuple)]
    eps = [e for e in classify(R) if e['cls'] in ('SLIP', 'DRAG')]
    tw = [wr(yaw2(r['vb_sh_r'], r['vb_sh_l']) - yaw2(r['vx_thigh_r'], r['vx_thigh_l'])) for r in R]
    out = []
    for i in range(1, len(R) - 2):
        a, b = short(R[i - 1].get('av_Phase27_SelectedObject')), short(R[i].get('av_Phase27_SelectedObject'))
        if a == b or short(R[i + 1].get('av_Phase27_SelectedObject')) != b or not a or not b: continue
        t0 = R[i]['t']; w = [k for k in range(i, len(R)) if R[k]['t'] <= t0 + 0.35]
        twr = max((abs(wr(tw[k] - tw[k - 1])) / max(R[k]['t'] - R[k - 1]['t'], 1e-3) for k in w if k > 0), default=0.0)
        back = 0
        for k in w:
            p, q = R[k - 1]['mh_root'], R[k]['mh_root']; dt = max(R[k]['t'] - R[k - 1]['t'], 1e-3); vx, vy = (q[0] - p[0]) / dt, (q[1] - p[1]) / dt
            if math.hypot(vx, vy) > 120.0:
                pf = yaw2(R[k]['vx_thigh_r'], R[k]['vx_thigh_l']) + 90.0   # thigh line r->l, +90 = forward
                bk = any(x in b for x in ('Bwd', 'Rear', 'Back', 'B_F', 'F_B', 'Pivot', 'Turn'))   # backpedal / pivot clips face away from the travel by design
                if abs(wr(pf - math.degrees(math.atan2(vy, vx)))) > 120.0 and fam(b) not in ('REV',) and not bk: back += 1
        hz = [R[k]['vb_head'] for k in range(max(1, i - 1), min(len(R), w[-1] + 2))]; tt = [R[k]['t'] for k in range(max(1, i - 1), min(len(R), w[-1] + 2))]
        ha = 0.0
        for k in range(1, len(hz) - 1):
            d = (tt[k + 1] - tt[k - 1]) / 2 or 1e-3
            ha = max(ha, math.sqrt(sum(((hz[k + 1][j] - 2 * hz[k][j] + hz[k - 1][j]) / (d * d)) ** 2 for j in range(3))) / 100.0)
        dr = max((e['drift'] for e in eps if t0 - 0.05 <= e['tw'] <= t0 + 0.35), default=0.0)
        out.append({'t': round(t0, 2), 'type': fam(a) + '>' + fam(b), 'from': a[:30], 'to': b[:30], 'drag': round(dr, 1), 'twist': round(twr), 'back': back, 'head': round(ha)})
    return out
if __name__ == '__main__':
    SUM = '--sum' in sys.argv; agg = {}
    for lab in [x for x in sys.argv[1:] if not x.startswith('--')]:
        try: tr = audit(lab)
        except Exception as e: print('TRANS231 %s ERR %s' % (lab, e)); continue
        for x in tr:
            g = agg.setdefault(x['type'], {'n': 0, 'drag': 0.0, 'twist': 0, 'back': 0, 'head': 0, 'worst': ''})
            g['n'] += 1; g['back'] += x['back']; g['twist'] = max(g['twist'], x['twist']); g['head'] = max(g['head'], x['head'])
            if x['drag'] > g['drag']: g['drag'] = x['drag']; g['worst'] = '%s@%.2f %s>%s' % (lab[-26:], x['t'], x['from'][:22], x['to'][:22])
            if not SUM and (x['drag'] >= 8 or x['twist'] >= 400 or x['back'] or x['head'] >= 40): print('TRANS231 %-30s %s' % (lab[-30:], x))
    for k, g in sorted(agg.items(), key=lambda kv: -kv[1]['drag']):
        print('TRANS231SUM %-14s n %3d | worst drag %5.1f | twist %4d deg/s | back frames %2d | head %3d m/s2 | %s' % (k, g['n'], g['drag'], g['twist'], g['back'], g['head'], g['worst']))
