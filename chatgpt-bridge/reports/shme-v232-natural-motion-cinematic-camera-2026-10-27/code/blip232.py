"""blip232.py <label-glob>... : one-frame selection blips (V2.32 A). A -> B -> C where B is selected for exactly ONE logged frame and B is a
different clip than A and C (a re-search on one frame that the next frame overrides: two blends in two frames). Per blip: time, A@ct, B@ct,
C@ct, the speed, and the max visible-ball speed jump at that frame (cm/s). Summary BLIP232 per label and the families involved."""
import sys, os, glob, math, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'SHME_V231_20261026'))
from ltp231 import load, short
L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Saved', 'Codex', 'SHME_V1_20260925', 'LTP')
def fam(o):
    o = short(o)
    for k in ('SHM226_JogRev_B_F', 'SHM226_JogRev_F_B', 'SHM231L', 'SHM231S', 'SHM217_BackLink', 'SHM216_RevTurn', 'SHM214_RevPush', 'SHM217_J2S', 'SHM218_W2S'):
        if o.startswith(k): return k
    return o[:22]
labs = []
for a in sys.argv[1:]:
    labs += [os.path.basename(p)[:-4] for p in glob.glob(os.path.join(L, a + '.ltp'))] or [a]
tot = collections.Counter(); per = {}
for lab in sorted(set(labs)):
    try: R = load(lab)
    except Exception as e: print('ERR', lab, e); continue
    R = [r for r in R if isinstance(r.get('vb_ball_l'), tuple)]
    sel = [short(r.get('av_Phase27_SelectedObject')) for r in R]
    n = 0
    for i in range(1, len(R) - 1):
        a, b, c = sel[i - 1], sel[i], sel[i + 1]
        if b != a and b != c and a and c:
            dt = max(R[i]['t'] - R[i - 1]['t'], 1e-3)
            jump = max(math.hypot(R[i]['vb_ball_' + s][0] - R[i - 1]['vb_ball_' + s][0], R[i]['vb_ball_' + s][1] - R[i - 1]['vb_ball_' + s][1]) / dt for s in 'lr')
            key = '%s > %s > %s' % (fam(a), fam(b), fam(c)); tot[key] += 1; n += 1
            if '--v' in sys.argv or len(labs) <= 3:
                print('  %-30s %6.3f %s@%.2f > %s@%.2f > %s@%.2f  v %.0f  ballv %.0f' % (lab[-30:], R[i]['t'], a[:24], float(R[i - 1].get('av_Phase27_SelectedTime') or 0), b[:24], float(R[i].get('av_Phase27_SelectedTime') or 0), c[:24], float(R[i + 1].get('av_Phase27_SelectedTime') or 0), math.hypot(*[float(R[i].get(k) or 0) for k in ('avx', 'avy')]) if R[i].get('avx') is not None else 0.0, jump))
    per[lab] = n
print('BLIP232 labels %d with_blips %d total %d' % (len(per), sum(1 for v in per.values() if v), sum(per.values())))
for k, v in tot.most_common(25): print('  %4d  %s' % (v, k))
