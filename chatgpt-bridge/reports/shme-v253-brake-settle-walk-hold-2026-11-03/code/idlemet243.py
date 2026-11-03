"""idlemet243.py <label>... : long-idle metrics from LTP (window = Speed2D < 3 after first stop); hold flag, visible clip, pelvis interfoot axis."""
import sys, re, math
LTP = 'Saved/Codex/SHME_V1_20260925/LTP/'
def vec(s):
    m = re.findall(r'[XYZ]=(-?[\d.]+)', s); return tuple(float(x) for x in m)
for lab in sys.argv[1:]:
    rows = []
    for ln in open(LTP + lab + '.ltp', encoding='utf8', errors='ignore'):
        if 'LTP|' not in ln: continue
        d = dict(kv.split('=', 1) for kv in ln.strip().split('|')[2:] if '=' in kv)
        try: rows.append(d)
        except: pass
    def f(d, k, dflt=0.0):
        try: return float(d.get(k, dflt))
        except: return dflt
    # idle window: first t>4 with Speed2D<3 until Speed2D>3 again
    t0 = t1 = None
    for d in rows:
        t = f(d, 't'); s = f(d, 'Speed2D')
        if t0 is None and t > 4.0 and s < 3: t0 = t
        elif t0 is not None and t1 is None and s > 3 and t > t0 + 1.0: t1 = t; break
    win = [d for d in rows if t0 is not None and t0 <= f(d, 't') <= (t1 or 1e9)]
    holds = sorted(set(d.get('av_SHM_IdleHold', '?') for d in win)); clips = {}
    for d in win:
        c = d.get('av_Phase27_SelectedObject', '?').split('/')[-1].split('.')[-1]; clips[c] = clips.get(c, 0) + 1
    seltimes = [f(d, 'av_Phase27_SelectedTime') for d in win]
    # pelvis along interfoot axis (right +): project pelvis onto unit vector from ball_l to ball_r
    axis = []; pz = []; px = []; py = []; ch = []
    for d in win:
        bl = vec(d['vb_ball_l']); br = vec(d['vb_ball_r']); p = vec(d['vb_pelvis']); c = vec(d['vb_chest'])
        mid = [(bl[i] + br[i]) / 2 for i in range(3)]; ax = [br[i] - bl[i] for i in range(2)]; n = math.hypot(*ax) or 1
        axis.append(((p[0] - mid[0]) * ax[0] + (p[1] - mid[1]) * ax[1]) / n); px.append(p[0]); py.append(p[1]); pz.append(p[2]); ch.append(c[2])
    def p2p(a): return (max(a) - min(a)) if a else 0
    # onset: first time |axis - axis[0]| > 1.5 cm
    ons = next((f(d, 't') - t0 for d, a in zip(win, axis) if abs(a - axis[0]) > 1.5), None)
    print(f"{lab:36s} win {t0:.2f}-{(t1 or 0):.2f} hold {holds} clips {clips} seltime {min(seltimes):.2f}->{max(seltimes):.2f} | pelvis p2p x/y/z {p2p(px):.2f}/{p2p(py):.2f}/{p2p(pz):.2f} chest z {p2p(ch):.2f} | interfoot axis {min(axis):.1f}..{max(axis):.1f} onset {ons}")
