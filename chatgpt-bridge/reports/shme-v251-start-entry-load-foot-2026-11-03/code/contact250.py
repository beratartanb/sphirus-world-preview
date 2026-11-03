"""contact250.py <label> [t0 t1] [--pre mx|vb] [--v] : V2.50 per-foot CONTACT QUALITY on the VISIBLE skeleton (vb_ = final MetaHuman bones;
--pre mx = the mannequin pose that drives the retarget). Separates five things that one slide number mixes:
  PEN   ground penetration: deepest ball below its standing floor level (floor = median ball z over the first 1.0 s of standing) [cm]
  PITCH foot bend: ankle->ball angle below horizontal, max over the window while the ball is within 4 cm of the floor [deg]
        (standing 25-35, normal push-off <= ~60; above that with a grounded ball = toes driven into the floor)
  PLANT planted-point translation per contact phase: the point on the heel..toe line that moves least while the foot bears weight
        (pivot249 rule) [cm]  - a heel or ball pivot is NOT a slide
  BALL  ball travel while the ball is grounded and the phase lasts >= 3 frames [cm] (a pivot shows as BALL > PLANT with YAW > 15)
  YAW   foot yaw turned inside the contact phase [deg] and its peak rate [deg/s]
Prints one CONTACT250 line per foot + per window worst; --v prints every phase."""
import sys, math
args = [a for a in sys.argv[1:] if not a.startswith('--')]; L = args[0]
T0 = float(args[1]) if len(args) > 1 else 0.0; T1 = float(args[2]) if len(args) > 2 else 1e9
PRE = 'mx' if '--pre' in sys.argv and sys.argv[sys.argv.index('--pre') + 1] == 'mx' else 'vb'; VERB = '--v' in sys.argv
def vec(s):
    p = dict(kv.split('=') for kv in s.split()); return float(p['X']), float(p['Y']), float(p['Z'])
rows = []
for line in open('Saved/Codex/SHME_V1_20260925/LTP/%s.ltp' % L, encoding='utf8', errors='ignore'):
    d = {}
    for kv in line.rstrip('\n').split('|')[2:]:
        if '=' in kv:
            k, v = kv.split('=', 1); d.setdefault(k, v)
    try:
        t = float(d['t']); rows.append((t, {s: (vec(d['%s_foot_%s' % (PRE, s)]), vec(d['%s_ball_%s' % (PRE, s)])) for s in 'lr'}, d.get('av_Phase27_SelectedObject', '')[-34:], float(d.get('cv_Speed', '0') or 0)))
    except Exception: pass
def pitch(a, b): return math.degrees(math.atan2(a[2] - b[2], max(1e-6, math.hypot(b[0] - a[0], b[1] - a[1]))))
def yaw(a, b): return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
res = {}
for s in 'lr':
    stand = [r[1][s][1][2] for r in rows if r[0] < rows[0][0] + 1.0] or [r[1][s][1][2] for r in rows]
    floor = sorted(stand)[len(stand) // 2]
    win = [r for r in rows if T0 <= r[0] <= T1]
    pen = min(((r[1][s][1][2] - floor), r[0], r[2]) for r in win)
    pit = max(((pitch(*r[1][s]) if r[1][s][1][2] < floor + 4 else -99), r[0], r[2]) for r in win)
    # contact phases: ball within 2 cm of the floor, ankle within 7 cm, ball slower than 150 cm/s of the ankle floor
    afl = sorted(r[1][s][0][2] for r in rows[:max(3, len(stand))])[len(stand) // 2]
    ph, phases = [], []
    prev = None
    for r in win:
        a, b = r[1][s]
        fast = prev is not None and r[0] > prev[0] and math.hypot(b[0] - prev[1][s][1][0], b[1] - prev[1][s][1][1]) / (r[0] - prev[0]) > 150.0
        prev = r
        if b[2] < floor + 2 and a[2] < afl + 7 and not fast: ph.append(r)
        else:
            if len(ph) >= 3: phases.append(ph)
            ph = []
    if len(ph) >= 3: phases.append(ph)
    worst = {'plant': (0, 0, ''), 'ball': (0, 0, ''), 'yaw': (0, 0, 0, '')}
    for ph in phases:
        a0, b0 = ph[0][1][s]; best = None
        for k in range(-8, 27):
            sv = k / 20.0; p0 = (a0[0] + sv * (b0[0] - a0[0]), a0[1] + sv * (b0[1] - a0[1]))
            mx = max(math.hypot(a[0] + sv * (b[0] - a[0]) - p0[0], a[1] + sv * (b[1] - a[1]) - p0[1]) for _, fb, _, _ in ph for a, b in [fb[s]])
            if best is None or mx < best[0]: best = (mx, sv)
        bt = max(math.hypot(r[1][s][1][0] - b0[0], r[1][s][1][1] - b0[1]) for r in ph)
        ys = [yaw(*r[1][s]) for r in ph]; dy = 0.0; rate = 0.0
        for i in range(1, len(ys)):
            d_ = (ys[i] - ys[i - 1] + 180) % 360 - 180; dy += d_; dt = ph[i][0] - ph[i - 1][0]
            if dt > 0: rate = max(rate, abs(d_) / dt)
        if VERB: print('  %s %.2f-%.2f %2d fr plant %5.1f (s=%.2f) ball %5.1f yaw %6.1f peak %5.0f deg/s pitch max %4.0f %s' % (s, ph[0][0], ph[-1][0], len(ph), best[0], best[1], bt, dy, rate, max(pitch(*r[1][s]) for r in ph), ph[0][2]))
        if best[0] > worst['plant'][0]: worst['plant'] = (best[0], ph[0][0], ph[0][2])
        if bt > worst['ball'][0]: worst['ball'] = (bt, ph[0][0], ph[0][2])
        if abs(dy) > abs(worst['yaw'][0]): worst['yaw'] = (dy, rate, ph[0][0], ph[0][2])
    res[s] = (pen, pit, worst)
    print('CONTACT250 %s %s %s | PEN %5.1f cm @%.2f (%s) | PITCH %4.0f deg @%.2f (%s) | PLANT %5.1f @%.2f (%s) | BALL %5.1f @%.2f | YAW %6.1f (peak %4.0f deg/s) @%.2f' % (
        L, PRE, s, -pen[0], pen[1], pen[2], pit[0], pit[1], pit[2], worst['plant'][0], worst['plant'][1], worst['plant'][2], worst['ball'][0], worst['ball'][1], worst['yaw'][0], worst['yaw'][1], worst['yaw'][2]))
