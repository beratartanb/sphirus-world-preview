"""chain226.py: where does the authored foot path first break between the clip and the visible foot?
For a run and a time window: per frame the selected clip + time (av_Phase27_*), the clip's ROOT-RELATIVE ball position (clipfoot226.json)
mapped into the world with a calibration fitted on steady loop frames (mesh yaw + offset + the capsule), the measured visible ball (vb_),
the MM-mesh ik_foot (mx_) and the split: clip-vs-visible (whole chain), and, across variants (FootPlacement / LegIK / warping off), which
stage carries the difference. Usage: chain226.py label t0 t1 [--foot=l|r] [--calib=t0:t1]
Prints per frame: t | clip@time | capsule x | clip-pred ball | visible ball | mx ik_foot | pred-vis (cm) | contact
and a summary: max |pred-vis| inside the clip, at which t, and the capsule-vs-clip-root progress difference."""
import json, sys, math, pathlib
P = pathlib.Path(__file__).resolve().parents[2]; E = P / 'Saved/Codex/SHME_V1_20260925/Evidence'
CF = json.load(open(P / 'Saved/Codex/SHME_V226_20261024/clipfoot226.json'))
lab = sys.argv[1]; t0 = float(sys.argv[2]); t1 = float(sys.argv[3])
foot = next((a.split('=')[1] for a in sys.argv[4:] if a.startswith('--foot=')), 'r')
cal = next((a.split('=')[1] for a in sys.argv[4:] if a.startswith('--calib=')), None)
R = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('ax'), list) and isinstance(r.get('vb_ball_l'), list)], key=lambda r: float(r['t']))
def clipname(r): return str(r.get('av_Phase27_SelectedObject')).split('.')[-1]
def sample(clip, tau, col):
    c = CF.get(clip)
    if not c: return None
    rows = c['rows']; dt = c['dt']; k = tau / dt; i = int(k); w = k - i
    if i >= len(rows) - 1: return rows[-1][col]
    a, b = rows[i][col], rows[i + 1][col]; return [a[j] + (b[j] - a[j]) * w for j in range(3)]
COL = {'root': 1, 'pelvis': 2, 'foot_l': 3, 'foot_r': 4, 'ball_l': 5, 'ball_r': 6}
# ---- calibration: on steady loop frames (a loop clip selected, before t0) fit yaw + offset so that  vb_ball = ax + Rz(yaw) * (clip_rel + off)
def fit(frames):
    best = None
    for yaw in range(-180, 180, 1):
        c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)); errs = []; offs = []
        for r, rel in frames:
            vb = r['vb_ball_' + foot]; ax = r['ax']
            rx, ry = c * rel[0] - s * rel[1], s * rel[0] + c * rel[1]
            offs.append((vb[0] - ax[0] - rx, vb[1] - ax[1] - ry, vb[2] - ax[2] - rel[2]))
        o = tuple(sum(v[i] for v in offs) / len(offs) for i in range(3))
        e = sum(math.dist(v, o) for v in offs) / len(offs)
        if best is None or e < best[0]: best = (e, yaw, o)
    return best
if cal:
    c0, c1 = [float(x) for x in cal.split(':')]
else: c0, c1 = t0 - 1.2, t0 - 0.1
cframes = []
for r in R:
    t = float(r['t'])
    if c0 <= t <= c1:
        cn = clipname(r); tau = float(r.get('av_Phase27_SelectedTime') or 0)
        if cn in CF:
            rel = sample(cn, tau, COL['ball_' + foot])
            if rel: cframes.append((r, rel))
if len(cframes) < 5: print('CHAIN226 %s: not enough calibration frames (%d) in %.2f..%.2f' % (lab, len(cframes), c0, c1)); sys.exit(0)
err, yaw, off = fit(cframes)
print('CHAIN226 %s foot %s | calibration %.2f..%.2f on %d loop frames: mesh yaw %d deg, offset (%.1f %.1f %.1f), residual %.1f cm' % (lab, foot, c0, c1, len(cframes), yaw, off[0], off[1], off[2], err))
c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
def pred(rel): return (R0[0] + c * (rel[0] + off[0]) - s * (rel[1] + off[1]), R0[1] + s * (rel[0] + off[0]) + c * (rel[1] + off[1]), R0[2] + rel[2] + off[2])
worst = (0, None); rows = []
for r in R:
    t = float(r['t'])
    if t0 <= t <= t1:
        cn = clipname(r); tau = float(r.get('av_Phase27_SelectedTime') or 0); R0 = r['ax']
        rel = sample(cn, tau, COL['ball_' + foot]) if cn in CF else None
        vb = r['vb_ball_' + foot]; mx = r.get('mx_ik_foot_' + foot)
        if rel:
            pw = pred(rel); d = math.dist(pw[:2], vb[:2]); dz = pw[2] - vb[2]
            if d > worst[0]: worst = (d, t)
            rows.append('%.2f %-22s %.2f | cap %7.1f | pred %7.1f %6.1f %5.1f | vis %7.1f %6.1f %5.1f | mx %s | d %5.1f dz %5.1f | C %s' % (t, cn[-22:], tau, R0[0], pw[0], pw[1], pw[2], vb[0], vb[1], vb[2], ('%7.1f %6.1f %5.1f' % tuple(mx)) if isinstance(mx, list) else '-', d, dz, 'Y' if r.get('cv_Contact' + foot.upper()) in (True, 'True', 1) else '.'))
        else:
            rows.append('%.2f %-22s %.2f | cap %7.1f | pred   (no clip data) | vis %7.1f %6.1f %5.1f' % (t, cn[-22:], tau, R0[0], vb[0], vb[1], vb[2]))
print('\n'.join(rows)); print('CHAIN226 worst |pred - visible| %.1f cm at %.2f' % worst)
