"""brake253.py <label> : V2.53 jog-stop body response per stop (clip name contains JogStop), window entry .. +1.6 s, travel frame from the
actor before the entry: pelvis height minimum (knee/hip load, cm below its value at the entry) and its time, head forward of the pelvis
(trunk + neck flexion) maximum increase over the entry value and its time, the time each of pelvis height / head-forward / shoulder-forward
last moves faster than 3 cm/s (settle order). Prints BRAKE253 lines."""
import sys, math
L = sys.argv[1]
def vec(s):
    p = dict(kv.split('=') for kv in s.split()); return float(p['X']), float(p['Y']), float(p['Z'])
rows = []
for line in open('Saved/Codex/SHME_V1_20260925/LTP/%s.ltp' % L, encoding='utf8', errors='ignore'):
    d = {}
    for kv in line.rstrip('\n').split('|')[2:]:
        if '=' in kv: k, v = kv.split('=', 1); d.setdefault(k, v)
    try: rows.append((float(d['t']), d.get('av_Phase27_SelectedObject', ''), {k: vec(d[k]) for k in ('ax', 'vb_pelvis', 'vb_head', 'vb_sh_l', 'vb_sh_r')}))
    except Exception: pass
i = 1
while i < len(rows):
    t, o, P = rows[i]
    if 'JogStop' in o and 'JogStop' not in rows[i - 1][1]:
        a0 = rows[max(0, i - 9)][2]['ax']; dx, dy = P['ax'][0] - a0[0], P['ax'][1] - a0[1]; n = math.hypot(dx, dy) or 1; F = (dx / n, dy / n)
        seg = [r for r in rows[i:] if r[0] <= t + 1.6]; fw = lambda r, k: r[2][k][0] * F[0] + r[2][k][1] * F[1]
        z = [r[2]['vb_pelvis'][2] for r in seg]; hf = [fw(r, 'vb_head') - fw(r, 'vb_pelvis') for r in seg]
        sf = [(fw(r, 'vb_sh_l') + fw(r, 'vb_sh_r')) / 2 - fw(r, 'vb_pelvis') for r in seg]
        jz = min(range(len(z)), key=lambda j: z[j]); jh = max(range(len(hf)), key=lambda j: hf[j])
        def last_move(v):
            for j in range(len(v) - 1, 0, -1):
                if abs(v[j] - v[j - 1]) / max(1e-3, seg[j][0] - seg[j - 1][0]) > 3.0: return seg[j][0] - t
            return 0.0
        print('BRAKE253 %s t=%.2f %-24s | pelvis min %.1f (-%.1f cm vs entry) @+%.2f | head fwd of pelvis +%.1f cm @+%.2f | last motion: pelvis z +%.2f head +%.2f shoulders +%.2f' % (
            L, t, o[-24:], z[jz], z[0] - z[jz], seg[jz][0] - t, hf[jh] - hf[0], seg[jh][0] - t, last_move(z), last_move(hf), last_move(sf)))
        i += 72
    i += 1
