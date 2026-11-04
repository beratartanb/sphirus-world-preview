"""brakepair253.py <label_before> <label_after> : same scenario, same frames (fixed step) - per jog stop the difference AFTER - BEFORE of
pelvis height (knee/hip load) and of head / shoulder forward of the pelvis (trunk flexion), max and time, plus when the two runs re-converge
(|diff| < 0.3 cm). Prints PAIR253 lines."""
import sys, math
def load(L):
    R = []
    for line in open('Saved/Codex/SHME_V1_20260925/LTP/%s.ltp' % L, encoding='utf8', errors='ignore'):
        d = {}
        for kv in line.rstrip('\n').split('|')[2:]:
            if '=' in kv: k, v = kv.split('=', 1); d.setdefault(k, v)
        try:
            p = lambda s: tuple(float(x.split('=')[1]) for x in s.split())
            R.append((float(d['t']), d.get('av_Phase27_SelectedObject', ''), {k: p(d[k]) for k in ('ax', 'vb_pelvis', 'vb_head', 'vb_sh_l', 'vb_sh_r')}))
        except Exception: pass
    return R
A, B = load(sys.argv[1]), load(sys.argv[2]); n = min(len(A), len(B))
i = 1
while i < n:
    if 'JogStop' in B[i][1] and 'JogStop' not in B[i - 1][1]:
        t = B[i][0]; a0 = B[max(0, i - 9)][2]['ax']; dx, dy = B[i][2]['ax'][0] - a0[0], B[i][2]['ax'][1] - a0[1]; m = math.hypot(dx, dy) or 1; F = (dx / m, dy / m)
        fw = lambda P, k: P[k][0] * F[0] + P[k][1] * F[1]
        js = [j for j in range(i, min(n, i + 96))]
        dz = [B[j][2]['vb_pelvis'][2] - A[j][2]['vb_pelvis'][2] for j in js]
        dh = [(fw(B[j][2], 'vb_head') - fw(B[j][2], 'vb_pelvis')) - (fw(A[j][2], 'vb_head') - fw(A[j][2], 'vb_pelvis')) for j in js]
        ds = [((fw(B[j][2], 'vb_sh_l') + fw(B[j][2], 'vb_sh_r')) / 2 - fw(B[j][2], 'vb_pelvis')) - ((fw(A[j][2], 'vb_sh_l') + fw(A[j][2], 'vb_sh_r')) / 2 - fw(A[j][2], 'vb_pelvis')) for j in js]
        kz = min(range(len(dz)), key=lambda k: dz[k]); kh = max(range(len(dh)), key=lambda k: dh[k]); ks = max(range(len(ds)), key=lambda k: ds[k])
        conv = lambda v, k0: next((B[js[k]][0] - t for k in range(k0, len(v)) if all(abs(x) < 0.3 for x in v[k:k + 6])), None)
        print('PAIR253 t=%.2f %-22s | pelvis lower by %.1f cm @+%.2f (back within 0.3 cm @+%s) | head fwd +%.1f cm @+%.2f (@+%s) | shoulders fwd +%.1f cm @+%.2f (@+%s)' % (
            t, B[i][1][-22:], -dz[kz], B[js[kz]][0] - t, '%.2f' % conv(dz, kz) if conv(dz, kz) is not None else '-', dh[kh], B[js[kh]][0] - t, '%.2f' % conv(dh, kh) if conv(dh, kh) is not None else '-',
            ds[ks], B[js[ks]][0] - t, '%.2f' % conv(ds, ks) if conv(ds, ks) is not None else '-'))
        i += 72
    i += 1
