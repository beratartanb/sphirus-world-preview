"""settle253.py <label> [--v] : V2.53 stop SETTLE analysis on the visible skeleton for every stop (selected clip name contains 'Stop').
Frame = travel direction at stop entry (fwd) / left. From the stop entry to +1.6 s:
  capsule stop time (actor speed < 5 cm/s), last foot plant (both feet grounded and still),
  pelvis forward excursion relative to the final support centre (mid of both feet) after the last plant: peak / overshoot back / settle time
  (|v| < 2 cm/s for 0.15 s), pelvis height dip (min z after the plant vs final), trunk pitch proxy = chest - pelvis forward offset,
  head - chest forward offset, and each segment's stop time (forward speed < 2 cm/s for 0.15 s) -> stagger between pelvis, chest, head, hands.
Prints SETTLE253 lines."""
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
        t = float(d['t']); rows.append((t, d.get('av_Phase27_SelectedObject', ''), {k: vec(d[k]) for k in ('ax', 'vb_pelvis', 'vb_chest', 'vb_head', 'vb_sh_l', 'vb_sh_r', 'vb_foot_l', 'vb_foot_r', 'vb_ball_l', 'vb_ball_r')}))
    except Exception: pass
def fl(k):
    z = [r[2][k][2] for r in rows if r[0] < rows[0][0] + 1.0]; return sorted(z)[len(z) // 2]
FL = {k: fl(k) for k in ('vb_foot_l', 'vb_foot_r', 'vb_ball_l', 'vb_ball_r')}
def grounded(P, s): return P['vb_ball_' + s][2] < FL['vb_ball_' + s] + 2.0 and P['vb_foot_' + s][2] < FL['vb_foot_' + s] + 3.0
i = 1
while i < len(rows):
    t, o, P = rows[i]
    if 'Stop' in o and 'Stop' not in rows[i - 1][1]:
        # travel direction from the actor over the 0.15 s before the entry
        k0 = max(0, i - 9); a0, a1 = rows[k0][2]['ax'], P['ax']; dx, dy = a1[0] - a0[0], a1[1] - a0[1]; n = math.hypot(dx, dy)
        if n < 0.5: i += 1; continue
        F = (dx / n, dy / n); v0 = n / (t - rows[k0][0])
        seg = [r for r in rows[i:] if r[0] <= t + 1.8]
        def fw(r, k): return r[2][k][0] * F[0] + r[2][k][1] * F[1]
        stop_t = next((r[0] for j, r in enumerate(seg[1:], 1) if math.hypot(r[2]['ax'][0] - seg[j - 1][2]['ax'][0], r[2]['ax'][1] - seg[j - 1][2]['ax'][1]) / max(1e-4, r[0] - seg[j - 1][0]) < 5.0), None)
        # last plant: first frame after which both feet stay grounded and move < 0.3 cm/frame
        plant = None
        for j in range(1, len(seg)):
            ok = all(grounded(seg[m][2], s) and math.dist(seg[m][2]['vb_ball_' + s][:2], seg[m - 1][2]['vb_ball_' + s][:2]) < 0.3 for m in range(j, min(len(seg), j + 12)) for s in 'lr')
            if ok: plant = j; break
        if plant is None: i += 1; continue
        cen = lambda r: ((r[2]['vb_foot_l'][0] + r[2]['vb_foot_r'][0] + r[2]['vb_ball_l'][0] + r[2]['vb_ball_r'][0]) / 4, (r[2]['vb_foot_l'][1] + r[2]['vb_foot_r'][1] + r[2]['vb_ball_l'][1] + r[2]['vb_ball_r'][1]) / 4)
        C = cen(seg[-1]); cf = C[0] * F[0] + C[1] * F[1]
        post = seg[plant:]
        def stopped(k):
            for j in range(1, len(post) - 9):
                if all(abs(fw(post[m], k) - fw(post[m - 1], k)) / (post[m][0] - post[m - 1][0]) < 2.0 for m in range(j, j + 9)): return post[j][0] - post[0][0]
            return None
        pel = [fw(r, 'vb_pelvis') - cf for r in post]; pz = [r[2]['vb_pelvis'][2] for r in post]
        trunk = [fw(r, 'vb_chest') - fw(r, 'vb_pelvis') for r in post]; head = [fw(r, 'vb_head') - fw(r, 'vb_chest') for r in post]
        shf = [(fw(r, 'vb_sh_l') + fw(r, 'vb_sh_r')) / 2 - fw(r, 'vb_chest') for r in post]
        ip = max(range(len(pel)), key=lambda j: pel[j])
        st = {k: stopped(k) for k in ('vb_pelvis', 'vb_chest', 'vb_head', 'vb_sh_l')}
        print('SETTLE253 %s t=%.2f %-34s v0 %3.0f | capsule stop +%s | last plant +%.2f | pelvis fwd vs support: at plant %+.1f peak %+.1f (+%.2f) final %+.1f, min after peak %+.1f | pelvis z dip %.1f | trunk fwd %+.1f..%+.1f final %+.1f | head-chest %+.1f..%+.1f | shoulder-chest %+.1f..%+.1f | stop after plant: pelvis %s chest %s head %s shoulder %s' % (
            L, t, o[-34:], v0, '%.2f' % (stop_t - t) if stop_t else '-', post[0][0] - t, pel[0], pel[ip], post[ip][0] - post[0][0], pel[-1], min(pel[ip:]), max(pz) - min(pz[: max(2, len(pz) // 2)]) if False else (pz[-1] - min(pz)),
            min(trunk), max(trunk), trunk[-1], min(head), max(head), min(shf), max(shf), *['%.2f' % st[k] if st[k] is not None else '-' for k in ('vb_pelvis', 'vb_chest', 'vb_head', 'vb_sh_l')]))
        if VERB:
            for j in range(0, len(post), 3): print('   +%.2f pel %+.1f z %.1f trunk %+.1f head %+.1f' % (post[j][0] - post[0][0], pel[j], pz[j], trunk[j], head[j]))
        i += int(1.2 * 60)
    i += 1
# ---- V2.53 whole-stop window metrics (entry .. entry + 1.6 s): load, trunk, head, stop staggering ----
def whole(L):
    i = 1
    while i < len(rows):
        t, o, P = rows[i]
        if 'Stop' in o and 'Stop' not in rows[i - 1][1]:
            k0 = max(0, i - 9); a0, a1 = rows[k0][2]['ax'], P['ax']; dx, dy = a1[0] - a0[0], a1[1] - a0[1]; n = math.hypot(dx, dy)
            if n < 0.5: i += 1; continue
            F = (dx / n, dy / n); seg = [r for r in rows[i:] if r[0] <= t + 1.6]
            fw = lambda r, k: r[2][k][0] * F[0] + r[2][k][1] * F[1]
            z = [r[2]['vb_pelvis'][2] for r in seg]; zf = z[-1]
            tr = [fw(r, 'vb_chest') - fw(r, 'vb_pelvis') for r in seg]; trf = tr[-1]
            hd = [fw(r, 'vb_head') - fw(r, 'vb_chest') for r in seg]; hdf = hd[-1]
            sh = [(fw(r, 'vb_sh_l') + fw(r, 'vb_sh_r')) / 2 - fw(r, 'vb_chest') for r in seg]; shf = sh[-1]
            def settle_t(vals):
                for j in range(len(vals) - 2, 0, -1):
                    if abs(vals[j + 1] - vals[j]) / max(1e-3, seg[j + 1][0] - seg[j][0]) > 3.0: return seg[j + 1][0] - t
                return 0.0
            jz = min(range(len(z)), key=lambda j: z[j]); jt = max(range(len(tr)), key=lambda j: tr[j] - trf)
            print('WHOLE253 %s t=%.2f %-26s | pelvis load %.1f cm @+%.2f | trunk lean +%.1f cm @+%.2f (min after %+.1f) | head-chest %+.1f..%+.1f | shoulder-chest %+.1f..%+.1f | settled: pelvis z +%.2f trunk +%.2f head +%.2f shoulders +%.2f' % (
                L, t, o[-26:], zf - z[jz], seg[jz][0] - t, tr[jt] - trf, seg[jt][0] - t, min(tr[jt:]) - trf, min(hd) - hdf, max(hd) - hdf, min(sh) - shf, max(sh) - shf, settle_t(z), settle_t(tr), settle_t(hd), settle_t(sh)))
            i += int(1.2 * 60)
        i += 1
whole(L)
