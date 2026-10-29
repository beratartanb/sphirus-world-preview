"""upper237.py <label> <t0> <t1> : reversal / brake upper body on the SAME frames as the legs (visible mesh): signed travel speed along the
first travel direction, clip + time, planted balls, trunk pitch (pelvis -> neck, + forward along the first travel), head pitch vs trunk,
both hands fore-aft relative to the pelvis along the first travel (the arm swing), and the hand swing amplitude over a sliding 0.3 s window."""
import sys, os, math
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'SHME_V231_20261026'))
from ltp231 import load, short
lab, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); R = load(lab); W = [r for r in R if t0 - 0.4 <= r['t'] <= t1]
v0 = next(r for r in W if r['t'] >= t0); vx, vy = v0.get('avx', 0) or 0, v0.get('avy', 0) or 0
pv = W[0]; prev = None; F = None
for r in W:
    if prev is not None and F is None:
        dx, dy = r['mx_root'][0] - prev['mx_root'][0], r['mx_root'][1] - prev['mx_root'][1]
        if math.hypot(dx, dy) > 0.5: F = (dx / math.hypot(dx, dy), dy / math.hypot(dx, dy))
    prev = r
F = F or (1.0, 0.0); hist = []
prev = None
for r in W:
    p = r['vb_pelvis']; n = r['vx_neck_01']; h = r['vb_head']
    along = lambda a: (a[0] - p[0]) * F[0] + (a[1] - p[1]) * F[1]
    tp = math.degrees(math.atan2(along(n), n[2] - p[2])); hp = math.degrees(math.atan2(along(h) - along(n), h[2] - n[2])) - tp
    hl, hr = along(r['vx_hand_l']), along(r['vx_hand_r'])
    sv = 0.0
    if prev: sv = ((r['mx_root'][0] - prev['mx_root'][0]) * F[0] + (r['mx_root'][1] - prev['mx_root'][1]) * F[1]) / max(r['t'] - prev['t'], 1e-3)
    hist.append((r['t'], hl, hr)); win = [x for x in hist if x[0] > r['t'] - 0.3]
    amp = max(x[1] for x in win) - min(x[1] for x in win)
    if r['t'] >= t0:
        print('%.2f in(%.1f,%.1f) v%+5.0f %-28s %.2f ball z L%5.1f R%5.1f | trunk %+5.1f head %+5.1f | hand L %+5.1f R %+5.1f swingL(0.3s) %4.1f' % (r['t'], r['lix'], r['liy'], sv,
            short(r['av_Phase27_SelectedObject'])[:28], r['av_Phase27_SelectedTime'], r['vb_ball_l'][2] - r['mx_root'][2], r['vb_ball_r'][2] - r['mx_root'][2], tp, hp, hl, hr, amp))
    prev = r
