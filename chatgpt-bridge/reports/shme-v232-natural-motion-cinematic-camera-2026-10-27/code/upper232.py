"""upper232.py <label>... : V2.32 systematic upper-body / posture audit on the VISIBLE body (LTP vx_/vb_ world bones), per movement stage.
Body frame = the travel heading (+-0.15 s) when moving, the visible hip line when standing (f forward, r right); trunk = lean added to the run's standing posture. Per stage (steady part = speed within 15 % of the stage median, >= 0.5 s) and per acceleration /
deceleration window (|dv/dt| > 150 cm/s2):
  arm   hand fore-aft excursion relative to its shoulder (peak-to-peak cm, mean of both arms) and midline crossing (hand lateral past the
        body centre line, cm; > 0 = crosses)
  ctr   shoulder line vs hip line yaw (counter-rotation, peak-to-peak deg)
  hlat  head lateral sway relative to the pelvis (p2p cm); hbob head vertical p2p (cm)
  trunk pitch of pelvis -> chest from vertical in the forward plane (deg, + forward): mean / min / max
  dip   pelvis height drop below the run's standing pelvis level (cm, max)
Reference bands (a measured, non-athletic adult; only a screen for outliers, never acceptance): walk arm 15-45 hlat <= 4 trunk -2..9;
jog arm 25-60 hlat <= 5 trunk 0..12; sprint arm 40-85 hlat <= 6 trunk 4..18; ctr <= 25 everywhere; dip <= 12. 'two characters' = the
trunk mean of acceleration windows minus that of deceleration windows (> 14 deg flagged). Prints UPPER232 {...} per label."""
import sys, os, math, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'SHME_V231_20261026'))
from ltp231 import load
BAND = {'walk': {'arm': (15, 45), 'hlat': 4, 'trunk': (-2, 9)}, 'jog': {'arm': (25, 60), 'hlat': 5, 'trunk': (0, 12)}, 'sprint': {'arm': (40, 85), 'hlat': 6, 'trunk': (4, 18)}}
def gait(v): return 'walk' if v < 190 else ('jog' if v < 380 else 'sprint')
def frame(r):
    # the VISIBLE body frame from the hip line (thigh_l -> thigh_r = right): the actor yaw lags the body by up to 45 deg in sprint curves
    if r.get('hd'):   # moving: the travel heading over +-0.15 s (the hip line rotates +-20 deg with the gait)
        f = r['hd']; return f, (-f[1], f[0])
    h = sub(r['vx_thigh_r'], r['vx_thigh_l']); n = math.hypot(h[0], h[1]) or 1.0; rt = (h[0] / n, h[1] / n)
    return (rt[1], -rt[0]), rt
def dot2(a, b): return a[0] * b[0] + a[1] * b[1]
def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
TP0 = [0.0]
def metrics(W, stand_pz):
    A = []; C = []; HL = []; HZ = []; TP = []; PZ = []; X = []
    for r in W:
        f, rt = frame(r)
        for s in 'lr':
            A.append((s, dot2(sub(r['vx_hand_' + s], r['vb_sh_' + s]), f)))
            X.append((s, dot2(sub(r['vx_hand_' + s], r['vb_pelvis']), rt) * (1 if s == 'l' else -1)))
        sl = sub(r['vb_sh_r'], r['vb_sh_l']); hl = sub(r['vx_thigh_r'], r['vx_thigh_l'])
        C.append(math.degrees(math.atan2(sl[1], sl[0]) - math.atan2(hl[1], hl[0])))
        HL.append(dot2(sub(r['vb_head'], r['vb_pelvis']), rt)); HZ.append(r['vb_head'][2])
        d = sub(r['vb_chest'], r['vb_pelvis']); TP.append(math.degrees(math.atan2(dot2(d, f), max(d[2], 1.0))) - TP0[0]); PZ.append(r['vb_pelvis'][2])
    C = [((c + 180) % 360) - 180 for c in C]
    arm = sum(max(a for s_, a in A if s_ == s) - min(a for s_, a in A if s_ == s) for s in 'lr') / 2.0
    cross = max(-x for s_, x in X)   # the left hand's lateral toward the right of the centre line (negative = crossed) mirrored for the right
    return {'arm': round(arm, 1), 'cross': round(cross, 1), 'ctr': round(max(C) - min(C), 1), 'hlat': round(max(HL) - min(HL), 1), 'hbob': round(max(HZ) - min(HZ), 1),
            'trunk': [round(sum(TP) / len(TP), 1), round(min(TP), 1), round(max(TP), 1)], 'dip': round(stand_pz - min(PZ), 1) if stand_pz else None}
for lab in sys.argv[1:]:
    R = [r for r in load(lab) if all(isinstance(r.get(k), tuple) for k in ('vx_hand_l', 'vx_hand_r', 'vb_sh_l', 'vb_sh_r', 'vb_head', 'vb_pelvis', 'vb_chest', 'vx_thigh_l', 'vx_thigh_r', 'mh_root'))]
    for i in range(len(R)):
        a, b = R[max(i - 1, 0)], R[min(i + 1, len(R) - 1)]; dt = max(b['t'] - a['t'], 1e-3)
        R[i]['sp'] = math.hypot(b['mh_root'][0] - a['mh_root'][0], b['mh_root'][1] - a['mh_root'][1]) / dt
    for i in range(len(R)):
        a, b = R[max(i - 3, 0)], R[min(i + 3, len(R) - 1)]; R[i]['acc'] = (b['sp'] - a['sp']) / max(b['t'] - a['t'], 1e-3)
        a, b = R[max(i - 4, 0)], R[min(i + 4, len(R) - 1)]; dx, dy = b['mh_root'][0] - a['mh_root'][0], b['mh_root'][1] - a['mh_root'][1]; n_ = math.hypot(dx, dy)
        R[i]['hd'] = (dx / n_, dy / n_) if (n_ > 1.0 and R[i]['sp'] > 30.0) else None
    st = [r['vb_pelvis'][2] for r in R if r['sp'] < 5.0]; stand_pz = sorted(st)[len(st) // 2] if st else None
    # standing trunk baseline (the skeleton's own pelvis -> chest offset): trunk values are the lean added to the standing posture
    TP0[0] = 0.0; S0 = [r for r in R if r['sp'] < 5.0]
    if S0:
        tps = []
        for r in S0:
            f, rt = frame(r); d = sub(r['vb_chest'], r['vb_pelvis']); tps.append(math.degrees(math.atan2(dot2(d, f), max(d[2], 1.0))))
        TP0[0] = sorted(tps)[len(tps) // 2]
    stages = []
    for r in R:
        s = '+'.join(x for x in str(r.get('stage', '')).split('+') if x.startswith('mv_')) or 'idle'
        if not stages or stages[-1][0] != s: stages.append([s, []])
        stages[-1][1].append(r)
    res = {'steady': [], 'acc': None, 'dec': None, 'flags': []}
    for s, W in stages:
        if len(W) < 15: continue
        med = sorted(r['sp'] for r in W)[len(W) // 2]
        if med < 40: continue
        S = [r for r in W if abs(r['sp'] - med) < 0.15 * med and abs(r['acc']) < 150]
        if len(S) < 15: continue
        m = metrics(S, stand_pz); m['stage'] = s[-26:]; m['gait'] = gait(med); m['v'] = round(med); res['steady'].append(m)
        bd = BAND[m['gait']]
        if not bd['arm'][0] <= m['arm'] <= bd['arm'][1]: res['flags'].append('%s arm %.0f (%s %s)' % (m['stage'], m['arm'], m['gait'], bd['arm']))
        if m['hlat'] > bd['hlat']: res['flags'].append('%s hlat %.1f > %s' % (m['stage'], m['hlat'], bd['hlat']))
        if not bd['trunk'][0] <= m['trunk'][0] <= bd['trunk'][1]: res['flags'].append('%s trunk %.1f (%s)' % (m['stage'], m['trunk'][0], bd['trunk']))
        if m['ctr'] > 25: res['flags'].append('%s ctr %.0f' % (m['stage'], m['ctr']))
    AC = [r for r in R if r['acc'] > 150 and r['sp'] > 40]; DC = [r for r in R if r['acc'] < -150 and r['sp'] > 40]
    if len(AC) > 5: res['acc'] = metrics(AC, stand_pz)
    if len(DC) > 5: res['dec'] = metrics(DC, stand_pz)
    if res['acc'] and res['dec']:
        d = res['acc']['trunk'][0] - res['dec']['trunk'][0]; res['acc_minus_dec_trunk'] = round(d, 1)
        if abs(d) > 14: res['flags'].append('two characters: trunk acc - dec %.1f deg' % d)
    for k in ('acc', 'dec'):
        if res[k] and res[k]['dip'] is not None and res[k]['dip'] > 12: res['flags'].append('%s dip %.1f cm' % (k, res[k]['dip']))
    print('UPPER232 %s %s' % (lab, json.dumps(res)))
