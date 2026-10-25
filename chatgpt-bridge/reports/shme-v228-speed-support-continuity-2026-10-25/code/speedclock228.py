"""speedclock228.py label [label ...]: clip clock vs capsule clock for the first authored SHM226 clip span of a run. Per frame: t since the
request, clip time ct, actual capsule speed along the OLD travel direction (actor position derivative), the clip design table speed at ct
(capsule_rev_table.json, measured 30 FPS table the clips were generated against), the difference and its integral (= designed-vs-actual
capsule displacement, the world drift a design-fixed planted foot must show), plus the brake-foot world x for both feet. Also prints the
clock offset estimate: the ct at which the table speed equals the actual speed at entry minus the actual ct_entry."""
import json, sys, bisect, pathlib
B = pathlib.Path(__file__).resolve().parents[2]
E = B / 'Saved/Codex/SHME_V1_20260925/Evidence'
T = json.load(open(B / 'Saved/Codex/SHME_V225_20261023/capsule_rev_table.json'))
def f(x, d=0.0):
    try: return float(x)
    except Exception: return d
def tab_v(fam, ct):
    v = T[fam]['v']; dt = T[fam]['dt']; i = ct / dt; k = int(i)
    if k >= len(v) - 1: return v[-1]
    return v[k] + (v[k + 1] - v[k]) * (i - k)
def ct_for_speed(fam, s):
    v = T[fam]['v']; dt = T[fam]['dt']
    for k in range(len(v) - 1):
        if (v[k] - s) * (v[k + 1] - s) <= 0 and v[k] != v[k + 1]: return (k + (v[k] - s) / (v[k] - v[k + 1])) * dt
    return None
for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
    R = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('ax'), list) and isinstance(r.get('vb_ball_l'), list)], key=lambda r: f(r['t']))
    n = len(R); Tm = [f(r['t']) for r in R]
    k0 = next((k for k in range(n) if 'JogRev' in str(R[k].get('av_Phase27_SelectedObject'))), None)
    if k0 is None: print('SPEEDCLOCK %s no authored clip' % lab); continue
    name = str(R[k0].get('av_Phase27_SelectedObject')); fam = 'F_B' if '_F_B_' in name else 'B_F'
    sgn = 1.0 if fam == 'F_B' else -1.0          # old travel direction along world x: F_B = forward (+x), B_F = backpedal (-x)
    k1 = k0
    while k1 + 1 < n and 'JogRev' in str(R[k1 + 1].get('av_Phase27_SelectedObject')): k1 += 1
    v_entry = (R[k0]['ax'][0] - R[k0 - 1]['ax'][0]) / (Tm[k0] - Tm[k0 - 1]) * sgn
    ct0 = f(R[k0].get('av_Phase27_SelectedTime')); cts = ct_for_speed(fam, v_entry)
    print('SPEEDCLOCK %s clip %s entry t %.3f ct %.3f actual v %.0f table v(ct) %.0f | table ct for that speed %s -> clip clock ahead of the capsule by %s s' % (
        lab[-26:], name[-10:], Tm[k0], ct0, v_entry, tab_v(fam, ct0), None if cts is None else round(cts, 3), None if cts is None else round(ct0 - cts, 3)))
    print('   dt    ct   v_act v_tab  diff   integ | ballL_x  ballR_x (world, rel. to entry actor x)')
    integ = 0.0; x0 = R[k0]['ax'][0]
    for k in range(k0, min(k1, k0 + 40) + 1):
        dt = Tm[k] - Tm[k - 1]
        va = (R[k]['ax'][0] - R[k - 1]['ax'][0]) / dt * sgn if dt > 0 else 0.0
        ct = f(R[k].get('av_Phase27_SelectedTime')); vt = tab_v(fam, ct)
        integ += (va - vt) * dt
        if (k - k0) % max(1, int(round(0.0333 / max(dt, 1e-3)))) == 0:
            print('  %5.2f %5.3f %6.0f %5.0f %6.0f %7.1f | %7.1f %7.1f' % (Tm[k] - Tm[k0], ct, va, vt, va - vt, integ, R[k]['vb_ball_l'][0] - x0, R[k]['vb_ball_r'][0] - x0))
