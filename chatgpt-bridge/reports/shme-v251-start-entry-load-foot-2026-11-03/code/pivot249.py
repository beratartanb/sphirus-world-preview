"""pivot249.py <label> [t0 t1] : FOOT TRANSLATION during ground contact (V2.49 metric). A planted foot may rotate (pivot) about any of its
points; it slides only if NO point of it stays put. Per contact phase of each foot (ball or ankle within 6 cm of the phase's lowest
ball height, at least 4 frames) the best fixed point p(s) = ankle + s * (ball - ankle), s in [-0.4, 1.3] (heel .. toe tip), is the one
with the smallest maximum travel; that travel is the foot's translation (slide). Also reports the foot yaw turned in the phase.
contact231's SLIP/DRAG (ball only) counts the toe arc of a heel pivot as a slide; this does not."""
import sys, math
L = sys.argv[1]; T0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0; T1 = float(sys.argv[3]) if len(sys.argv) > 3 else 1e9
def vec(s):
    p = dict(kv.split('=') for kv in s.split()); return float(p['X']), float(p['Y']), float(p['Z'])
rows = []
for line in open('Saved/Codex/SHME_V1_20260925/LTP/%s.ltp' % L, encoding='utf8', errors='ignore'):
    d = {}
    for kv in line.rstrip('\n').split('|')[2:]:
        if '=' in kv:
            k, v = kv.split('=', 1); d.setdefault(k, v)
    try:
        t = float(d['t'])
        if T0 <= t <= T1: rows.append((t, {s: (vec(d['mx_foot_' + s]), vec(d['mx_ball_' + s])) for s in 'lr'}, d.get('av_Phase27_SelectedObject', '')))
    except Exception: pass
worst = (0.0, None)
for s in 'lr':
    zfb = min(r[1][s][1][2] for r in rows) if rows else 0; zfa = min(r[1][s][0][2] for r in rows) if rows else 0   # floor heights of ball / ankle
    phase = []
    def close(ph):
        global worst
        if len(ph) < 4: return
        a0, b0 = ph[0][1][s]; best = None
        for k in range(-8, 27):
            sv = k / 20.0; p0 = (a0[0] + sv * (b0[0] - a0[0]), a0[1] + sv * (b0[1] - a0[1]))
            mx = max(math.hypot(a[0] + sv * (b[0] - a[0]) - p0[0], a[1] + sv * (b[1] - a[1]) - p0[1]) for _, fb, _ in ph for a, b in [fb[s]])
            if best is None or mx < best[1]: best = (sv, mx)
        y0 = math.degrees(math.atan2(b0[1] - a0[1], b0[0] - a0[0])); a1, b1 = ph[-1][1][s]; y1 = math.degrees(math.atan2(b1[1] - a1[1], b1[0] - a1[0]))
        dy = (y1 - y0 + 180) % 360 - 180
        print('  %s %.2f-%.2f  %2d fr  translation %5.1f cm  pivot s=%5.2f  foot yaw %6.1f  %s' % (s, ph[0][0], ph[-1][0], len(ph), best[1], best[0], dy, ph[len(ph) // 2][2][-30:]))
        if best[1] > worst[0]: worst = (best[1], '%s %.2f %s' % (s, ph[0][0], ph[len(ph) // 2][2][-30:]))
    for r in rows:
        a, b = r[1][s]
        if b[2] < zfb + 3.0 and a[2] < zfa + 6.0: phase.append(r)      # weight-bearing: ball on the floor AND heel/ankle down (a skim step is not contact)
        else: close(phase); phase = []
    close(phase)
print('PIVOT249 %s worst translation %.1f cm (%s)' % (L, worst[0], worst[1]))
