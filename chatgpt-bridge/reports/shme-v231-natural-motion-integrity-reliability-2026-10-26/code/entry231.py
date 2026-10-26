"""entry231.py <label>... : every entry into an authored reversal clip (SHM2xx_JogRev*) -> entry time, speed along facing, the pose source
(previous selected clip + its time), entry clip + ct, worst planted-ball slide in the first 0.6 s (ball z < floor+2 cm, cm travelled while
'planted'), capsule speed jump when the clip-bound speed switches on (|v(on) - v(prev)|), and the input sample time."""
import sys, math, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ltp231 import load, short
def vf(prev, r):
    dt = (r['t'] - prev['t']) or 1e-3; yaw = math.radians(r.get('ay', 0.0))
    pr, pc = prev['mh_root'], r['mh_root']; return ((pc[0] - pr[0]) * math.cos(yaw) + (pc[1] - pr[1]) * math.sin(yaw)) / dt
def entries(lab, fam=('SHM226_JogRev', 'SHM230L', 'SHM231')):
    R = load(lab); R = [r for r in R if 'mh_root' in r and isinstance(r.get('mh_root'), tuple)]; out = []
    floor = {s: min(r['vb_ball_' + s][2] for r in R) for s in 'lr'}
    for i in range(2, len(R)):
        so, po = short(R[i].get('av_Phase27_SelectedObject')), short(R[i - 1].get('av_Phase27_SelectedObject'))
        if so.startswith(fam) and not po.startswith(fam):
            j = i; src = po; srct = R[i - 1].get('av_Phase27_SelectedTime')
            v0 = vf(R[i - 2], R[i - 1]); slide = {'l': 0.0, 'r': 0.0}; jump = 0.0; on = None
            for k in range(i, min(len(R), i + int(0.6 / max(R[i]['t'] - R[i - 1]['t'], 1e-3)) + 1)):
                for s in 'lr':
                    a, b = R[k - 1]['vb_ball_' + s], R[k]['vb_ball_' + s]
                    if a[2] < floor[s] + 2.0 and b[2] < floor[s] + 2.0: slide[s] += math.hypot(b[0] - a[0], b[1] - a[1])
                if on is None and str(R[k].get('cv_ClipSpeedOn')) == 'True':
                    on = R[k]['t']; jump = vf(R[k - 1], R[k]) - vf(R[k - 2], R[k - 1])
            out.append({'t': R[i]['t'], 'v0': round(v0), 'src': src, 'src_t': srct, 'clip': so, 'ct': R[i].get('av_Phase27_SelectedTime'),
                        'slideL': round(slide['l'], 1), 'slideR': round(slide['r'], 1), 'bind_t': on, 'bind_jump': round(jump)})
    return out
if __name__ == '__main__':
    for lab in sys.argv[1:]:
        try:
            for e in entries(lab): print(lab, e)
        except Exception as ex: print(lab, 'ERR', ex)
