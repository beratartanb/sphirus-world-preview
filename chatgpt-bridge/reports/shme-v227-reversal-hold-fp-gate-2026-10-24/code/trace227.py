"""trace227.py label t0 t1 : per-frame trace of the V2.27 chain state (asset, selected time, database, ABP episode, hold/restart/dead/thr,
SHM227_Rev, speed, planted balls) between t0 and t1 s. Reads Saved/Codex/SHME_V1_20260925/Evidence/<label>.json."""
import json, sys, pathlib, math
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
lab, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
R = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('vb_ball_l'), list)], key=lambda r: float(r['t']))
def f(x):
    try: return float(x)
    except Exception: return float('nan')
def bb(x): return '1' if str(x) in ('True', 'true', '1', '1.0') else '.'
print('%-7s %-9s %5s %-14s A H R D T  %5s %5s %6s  %-7s %-7s %6s %6s' % ('t', 'asset', 'ct', 'db', 'rev', 'rdT', 'spd', 'intent', 'cRA', 'dL', 'dR'))
prev = None
for r in R:
    t = f(r['t'])
    if t < t0 or t > t1: prev = r; continue
    dl = dr = 0.0
    if prev is not None:
        dl = math.hypot(r['vb_ball_l'][0] - prev['vb_ball_l'][0], r['vb_ball_l'][1] - prev['vb_ball_l'][1])
        dr = math.hypot(r['vb_ball_r'][0] - prev['vb_ball_r'][0], r['vb_ball_r'][1] - prev['vb_ball_r'][1])
    zl = r['vb_ball_l'][2]; zr = r['vb_ball_r'][2]
    print('%-7.3f %-9s %5.2f %-14s %s %s %s %s %s  %5.2f %5.2f %6.1f  %-7s %-7s %5.1f%s %5.1f%s' % (
        t, str(r.get('av_Phase27_SelectedObject'))[-9:], f(r.get('av_Phase27_SelectedTime')), str(r.get('av_Phase27_SelectedDatabase', r.get('av_Phase27_Database', '')))[-14:],
        bb(r.get('av_SHM_RedirectActive')), bb(r.get('av_SHM227_Hold')), bb(r.get('av_SHM227_Restart')), bb(r.get('av_SHM227_Dead')), bb(r.get('av_SHM227_Thr')),
        f(r.get('av_SHM227_Rev')), f(r.get('RedirectTime', r.get('cv_RedirectTime', float('nan')))), f(r.get('Speed2D')),
        str(r.get('HasIntent', r.get('cv_HasIntent', '')))[:7], str(r.get('RedirectActive', r.get('cv_RedirectActive', '')))[:7], dl, '*' if zl < 4 else ' ', dr, '*' if zr < 4 else ' '))
    prev = r
