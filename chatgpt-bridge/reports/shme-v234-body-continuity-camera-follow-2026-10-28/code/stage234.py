"""stage234.py <label>... : where does an upper-body source change get lost? Same run, same time window (steady sprint: speed within 10 %
of the run's max, >= 1 s), two observation points recorded every tick: mx_ = the MotionMatching mesh after the whole MM ABP (MM blend +
additive lean / posture + feet IK layer modify-bones + IK / look-at layers), vx_ = the VISIBLE body after retarget / its post process.
Metrics per point, in the travel frame: arm = hand fore-aft excursion relative to the upper arm (p2p cm, mean L/R), elbow = lower arm
fore-aft p2p, nlat = neck lateral sway relative to the pelvis (p2p cm), trunk = pelvis->neck forward lean (deg, mean), ctr = clavicle line
vs thigh line yaw p2p (deg). Prints STAGE234 per label."""
import sys, os, math, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'SHME_V231_20261026'))
from ltp231 import load
def P(s):
    try: return tuple(float(x.split('=')[1]) for x in s.split(' ')[:3]) if 'X=' in s else tuple(float(x) for x in s.replace(',', ' ').split()[:3])
    except Exception: return None
def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def d2(a, b): return a[0] * b[0] + a[1] * b[1]
for lab in sys.argv[1:]:
    R = load(lab); rows = []
    for r in R:
        try: d = {k: v for k, v in r.items()}; d['sp'] = float(r.get('Speed2D', 0)); rows.append(d)
        except Exception: pass
    vmax = max(r['sp'] for r in rows)
    def hd(i):
        a = rows[max(i - 9, 0)]['vb_pelvis']; b = rows[min(i + 9, len(rows) - 1)]['vb_pelvis']; return math.atan2(b[1] - a[1], b[0] - a[0])
    W = []
    for i, r in enumerate(rows):   # steady sprint on a STRAIGHT stretch (heading change over +-0.6 s < 4 deg): turns add lean / sway
        if r['sp'] < 0.9 * vmax or i < 18 or i > len(rows) - 19: continue
        if abs(math.degrees(((hd(i + 9) - hd(i - 9) + math.pi) % (2 * math.pi)) - math.pi)) < 4.0: r['_f'] = hd(i); W.append(r)
    out = {'n': len(W), 'vmax': round(vmax)}
    for pt in ('mx_', 'vx_'):
        A = {'l': [], 'r': []}; E = {'l': [], 'r': []}; NL = []; TR = []; CT = []; AG = {'l': [], 'r': []}
        for i, r in enumerate(W):
            f = (math.cos(r['_f']), math.sin(r['_f']), 0.0); rt = (-f[1], f[0], 0.0)
            pel = r.get(pt + 'pelvis') or r['vb_pelvis']
            for s in 'lr':
                ua = sub(r[pt + 'lowerarm_' + s], r[pt + 'upperarm_' + s]); AG[s].append(math.degrees(math.atan2(d2(ua, f), -ua[2])))
                A[s].append(d2(sub(r[pt + 'hand_' + s], r[pt + 'upperarm_' + s]), f)); E[s].append(d2(sub(r[pt + 'lowerarm_' + s], r[pt + 'upperarm_' + s]), f))
            NL.append(d2(sub(r[pt + 'neck_01'], pel), rt))
            dv = sub(r[pt + 'neck_01'], pel); TR.append(math.degrees(math.atan2(d2(dv, f), max(dv[2], 1.0))))
            cl = sub(r[pt + 'upperarm_r'], r[pt + 'upperarm_l']); th = sub(r[pt + 'thigh_r'], r[pt + 'thigh_l'])
            CT.append(((math.degrees(math.atan2(cl[1], cl[0]) - math.atan2(th[1], th[0])) + 180) % 360) - 180)
        p2p = lambda x: max(x) - min(x)
        out[pt[:2]] = {'arm': round((p2p(A['l']) + p2p(A['r'])) / 2, 1), 'elbow': round((p2p(E['l']) + p2p(E['r'])) / 2, 1), 'nlat': round(p2p(NL), 1),
                       'trunk': round(sum(TR) / len(TR), 1), 'ctr': round(p2p(CT), 1), 'uarm_deg': round((p2p(AG['l']) + p2p(AG['r'])) / 2, 1), 'uarm_len': round(sum(math.dist(r[pt + 'lowerarm_l'], r[pt + 'upperarm_l']) for r in W) / len(W), 1)}
    print('STAGE234 %s %s' % (lab, json.dumps(out)))
