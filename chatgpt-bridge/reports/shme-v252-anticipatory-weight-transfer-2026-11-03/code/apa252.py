"""apa252.py <label> : every walk start-transfer step in a run - pelvis / chest position on the stance->swing axis (0 = stance foot,
1 = swing foot) at swing toe-off, the stance foot translation (min-travel point) from the start to toe-off + 0.2 s, and the clip."""
import sys, math
L = sys.argv[1]
def vec(s):
    p = dict(kv.split('=') for kv in s.split()); return float(p['X']), float(p['Y']), float(p['Z'])
rows = []
for line in open('Saved/Codex/SHME_V1_20260925/LTP/%s.ltp' % L, encoding='utf8', errors='ignore'):
    d = {}
    for kv in line.rstrip('\n').split('|')[2:]:
        if '=' in kv: k, v = kv.split('=', 1); d.setdefault(k, v)
    try: rows.append((float(d['t']), d))
    except Exception: pass
def cen(d, s):
    a = vec(d['vb_foot_' + s]); b = vec(d['vb_ball_' + s]); return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), a, b
i = 0
while i < len(rows):
    t, d = rows[i]; o = d.get('av_Phase27_SelectedObject', '')
    if 'StartTransfer' in o and (i == 0 or 'StartTransfer' not in rows[i - 1][1].get('av_Phase27_SelectedObject', '')):
        sw = 'l' if o.split('_APA')[0].endswith('Lfoot') else 'r'; st = 'r' if sw == 'l' else 'l'
        b0 = vec(d['vb_ball_' + sw])[2]; j = i; toe = None
        while j < len(rows) and rows[j][0] < t + 0.8:
            if vec(rows[j][1]['vb_ball_' + sw])[2] > b0 + 1.5: toe = j; break
            j += 1
        if toe is not None:
            dd = rows[toe][1]; sc = cen(dd, st)[0]; wc = cen(dd, sw)[0]; dx, dy = wc[0] - sc[0], wc[1] - sc[1]; n2 = dx * dx + dy * dy or 1
            pe = vec(dd['vb_pelvis']); ch = vec(dd['vb_chest'])
            tp = ((pe[0] - sc[0]) * dx + (pe[1] - sc[1]) * dy) / n2; tc = ((ch[0] - sc[0]) * dx + (ch[1] - sc[1]) * dy) / n2
            seg = [r for r in rows[i:] if r[0] <= rows[toe][0] + 0.2]
            best = None
            for k in range(-8, 27):
                s_ = k / 20.0
                pts = [(vec(r[1]['vb_foot_' + st])[0] + s_ * (vec(r[1]['vb_ball_' + st])[0] - vec(r[1]['vb_foot_' + st])[0]), vec(r[1]['vb_foot_' + st])[1] + s_ * (vec(r[1]['vb_ball_' + st])[1] - vec(r[1]['vb_foot_' + st])[1])) for r in seg]
                mx = max(math.hypot(p[0] - pts[0][0], p[1] - pts[0][1]) for p in pts)
                if best is None or mx < best: best = mx
            print('APA252 %s t=%.2f %-34s swing %s toe-off +%.3f s | pelvis t %.2f chest t %.2f | stance foot translation %.1f cm' % (L, t, o[-34:], sw, rows[toe][0] - t, tp, tc, best))
    i += 1
