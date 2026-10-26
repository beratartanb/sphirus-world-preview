"""exits231.py <label>... : what MM selects right after an authored reversal clip (SHM226/SHM231) stops being selected: next clip, its
database, time from the exit, and the planted-ball slide over the following 0.5 s."""
import sys, math, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ltp231 import load, short
for lab in sys.argv[1:]:
    try: R = load(lab)
    except Exception as e: print(lab, 'ERR', e); continue
    R = [r for r in R if isinstance(r.get('vb_ball_l'), tuple)]
    floor = {s: sorted(r['vb_ball_' + s][2] for r in R)[len(R) // 10] + 2.0 for s in 'lr'}
    for i in range(1, len(R)):
        a, b = short(R[i - 1].get('av_Phase27_SelectedObject')), short(R[i].get('av_Phase27_SelectedObject'))
        if a.startswith(('SHM226_', 'SHM231')) and not b.startswith(('SHM226_', 'SHM231')):
            seq = []
            for k in range(i, min(len(R), i + 12)):
                o = short(R[k].get('av_Phase27_SelectedObject'))
                if not seq or seq[-1] != o: seq.append(o)
            sl = {'l': 0.0, 'r': 0.0}
            for k in range(i, min(len(R), i + int(0.5 / max(R[i]['t'] - R[i - 1]['t'], 1e-3)))):
                for s in 'lr':
                    p, q = R[k - 1]['vb_ball_' + s], R[k]['vb_ball_' + s]
                    if p[2] < floor[s] and q[2] < floor[s]: sl[s] += math.hypot(q[0] - p[0], q[1] - p[1])
            print('%-34s t=%.3f %s@%.2f -> %s db=%s hold=%s | slide %.1f/%.1f' % (lab[-34:], R[i]['t'], a, R[i - 1].get('av_Phase27_SelectedTime') or 0, ' > '.join(seq)[:110], short(R[i].get('av_CurrentSelectedDatabase')), str(R[i].get('av_SHM227_Hold'))[:1], sl['l'], sl['r']))
