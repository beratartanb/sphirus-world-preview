"""stance253.py <label> [--v] : V2.53 decomposition of the STANCE (support) foot motion of every walk start-transfer step in a run.
Window = clip entry .. swing toe-off + 0.25 s. Every frame the stance foot is classified on the visible skeleton (vb_):
  FLAT  heel (foot joint) and ball both within 2.5 cm of their standing floor   -> any heel/ball travel is a SLIDE
  BALL  ball grounded, heel raised                                            -> rotation about the ball = PIVOT, ball travel = SLIDE
  HEEL  heel grounded, ball raised                                            -> rotation about the heel = PIVOT, heel travel = SLIDE
  AIR   both raised                                                          -> travel = STEP (a real re-placement)
Prints per event: frames per class, slide [cm] (sum of grounded-point travel), pivot yaw [deg], step travel [cm], net foot travel
(heel-ball midpoint, start -> end), pelvis drop and leg compression (pelvis - ankle distance change) at toe-off, chest-pelvis lag."""
import sys, math
L = sys.argv[1]; VERB = '--v' in sys.argv
def vec(s):
    p = dict(kv.split('=') for kv in s.split()); return float(p['X']), float(p['Y']), float(p['Z'])
rows = []
for line in open('Saved/Codex/SHME_V1_20260925/LTP/%s.ltp' % L, encoding='utf8', errors='ignore'):
    d = {}
    for kv in line.rstrip('\n').split('|')[2:]:
        if '=' in kv: k, v = kv.split('=', 1); d.setdefault(k, v)
    try:
        t = float(d['t']); rows.append((t, d, {k: vec(d['vb_' + k]) for k in ('foot_l', 'foot_r', 'ball_l', 'ball_r', 'pelvis', 'chest', 'head')}))
    except Exception: pass
def fl(key):
    z = [r[2][key][2] for r in rows if r[0] < rows[0][0] + 1.0]; return sorted(z)[len(z) // 2]
FLOOR = {k: fl(k) for k in ('foot_l', 'foot_r', 'ball_l', 'ball_r')}
def yaw(a, b): return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
def h(a, b): return math.hypot(a[0] - b[0], a[1] - b[1])
out = []
i = 0
while i < len(rows):
    t, d, P = rows[i]; o = d.get('av_Phase27_SelectedObject', '')
    if 'StartTransfer' in o and (i == 0 or 'StartTransfer' not in rows[i - 1][1].get('av_Phase27_SelectedObject', '')):
        sw = 'l' if o.split('_APA')[0].endswith('Lfoot') else 'r'; st = 'r' if sw == 'l' else 'l'
        b0 = P['ball_' + sw][2]; toe = None; j = i
        while j < len(rows) and rows[j][0] < t + 0.8:
            if rows[j][2]['ball_' + sw][2] > b0 + 1.5: toe = j; break
            j += 1
        if toe is None: i += 1; continue
        end = toe
        while end < len(rows) - 1 and rows[end][0] < rows[toe][0] + 0.25: end += 1
        cnt = {'FLAT': 0, 'BALL': 0, 'HEEL': 0, 'AIR': 0}; slide = {'FLAT': 0.0, 'BALL': 0.0, 'HEEL': 0.0}; piv = 0.0; step = 0.0; trace = []
        pre_slide = 0.0; ball_pre = 0.0; heel_pre = 0.0; yaw_pre = 0.0
        for k in range(i, end + 1):
            Q = rows[k][2]; hf, bf = Q['foot_' + st], Q['ball_' + st]
            hg = hf[2] < FLOOR['foot_' + st] + 2.5; bg = bf[2] < FLOOR['ball_' + st] + 2.5
            c = 'FLAT' if hg and bg else 'BALL' if bg else 'HEEL' if hg else 'AIR'; cnt[c] += 1
            if k > i:
                R = rows[k - 1][2]; ph, pb = R['foot_' + st], R['ball_' + st]
                dy = (yaw(hf, bf) - yaw(ph, pb) + 180) % 360 - 180
                if c == 'FLAT': s_ = max(h(hf, ph), h(bf, pb)); slide['FLAT'] += s_
                elif c == 'BALL': s_ = h(bf, pb); slide['BALL'] += s_; piv += dy
                elif c == 'HEEL': s_ = h(hf, ph); slide['HEEL'] += s_; piv += dy
                else: s_ = h(((hf[0] + bf[0]) / 2, (hf[1] + bf[1]) / 2), ((ph[0] + pb[0]) / 2, (ph[1] + pb[1]) / 2)); step += s_
                if k <= toe and c != 'AIR': pre_slide += s_; ball_pre += h(bf, pb); heel_pre += h(hf, ph); yaw_pre += dy
            trace.append('%s%.1f' % (c[0], (hf[2] - FLOOR['foot_' + st])))
        A, Z = rows[i][2], rows[end][2]
        mid = lambda Q: ((Q['foot_' + st][0] + Q['ball_' + st][0]) / 2, (Q['foot_' + st][1] + Q['ball_' + st][1]) / 2)
        T = rows[toe][2]
        comp0 = math.dist(A['pelvis'], A['foot_' + st]); compT = math.dist(T['pelvis'], T['foot_' + st])
        lag = (T['chest'][0] - T['pelvis'][0], T['chest'][1] - T['pelvis'][1])
        # pelvis along the frame-0 stance->swing axis (cm toward the stance foot = negative) and its peak acceleration (artificial = spiky)
        sc0 = mid(A); sw0 = ((A['foot_' + sw][0] + A['ball_' + sw][0]) / 2, (A['foot_' + sw][1] + A['ball_' + sw][1]) / 2)
        ax_ = (sw0[0] - sc0[0], sw0[1] - sc0[1]); n_ = math.hypot(*ax_) or 1; ax_ = (ax_[0] / n_, ax_[1] / n_)
        lat = [(rows[k][2]['pelvis'][0] - A['pelvis'][0]) * ax_[0] + (rows[k][2]['pelvis'][1] - A['pelvis'][1]) * ax_[1] for k in range(i, end + 1)]
        dts = [rows[k][0] - rows[k - 1][0] for k in range(i + 1, end + 1)]
        acc = [abs(lat[k + 1] - 2 * lat[k] + lat[k - 1]) / (max(dts[k - 1], 1e-3) ** 2) / 100.0 for k in range(1, len(lat) - 1)] or [0]
        acc_t = (acc.index(max(acc)) + 1) * (rows[end][0] - t) / max(1, end - i)
        chl = [((rows[k][2]['chest'][0] - rows[k][2]['pelvis'][0]) * ax_[0] + (rows[k][2]['chest'][1] - rows[k][2]['pelvis'][1]) * ax_[1]) for k in range(i, end + 1)]
        r = dict(t=t, clip=o.split('/')[-1][-34:], sw=sw, toe=rows[toe][0] - t, cnt=cnt, slide=slide, pre=pre_slide, piv=piv, step=step,
                 net=h(mid(A), mid(Z)), drop=A['pelvis'][2] - T['pelvis'][2], comp=comp0 - compT)
        print('STANCE253 %s t=%.2f %-34s toe +%.2f | FLAT %2d BALL %2d HEEL %2d AIR %2d | pre-toe ball %.1f heel %.1f yaw %+.0f | slide pre-toe %.1f / flat %.1f ball %.1f heel %.1f | pivot %+.0f deg | step %.1f | net %.1f | pelvis drop %.1f leg comp %.1f | pelvis lat %+.1f..%+.1f (toe %+.1f) acc max %.1f m/s2 @+%.2f | chest-pelvis lat %+.1f..%+.1f' % (
            L, t, r['clip'], r['toe'], cnt['FLAT'], cnt['BALL'], cnt['HEEL'], cnt['AIR'], ball_pre, heel_pre, yaw_pre, pre_slide, slide['FLAT'], slide['BALL'], slide['HEEL'], piv, step, r['net'], r['drop'], r['comp'], min(lat), max(lat), lat[toe - i], max(acc), acc_t, min(chl), max(chl)))
        if VERB: print('   ', ' '.join(trace))
    i += 1
