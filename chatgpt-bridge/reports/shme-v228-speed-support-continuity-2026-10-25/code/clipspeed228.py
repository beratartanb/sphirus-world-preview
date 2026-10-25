"""clipspeed228.py label [label ...] [--all]: did the capsule follow the clip clock? For the first authored SHM226 clip span: per frame
(every 2nd frame unless --all) t since entry, ct, actual capsule speed along the actor forward axis (actor position derivative projected on
the actor yaw), the ABP designed speed SHM228_DesV, the command SHM228_Cmd, flags (SHM228_On / component ClipSpeedOn), the running
integral of (actual - DesV) = capsule-vs-design displacement (the drift a design-fixed planted foot must show), and both balls' world x.
Summary line: entry offset, max |actual - DesV| after the first 3 frames, final integral, planted-foot drift from plant225-like criterion."""
import json, sys, math, pathlib
B = pathlib.Path(__file__).resolve().parents[2]; E = B / 'Saved/Codex/SHME_V1_20260925/Evidence'
def f(x, d=0.0):
    try: return float(x)
    except Exception: return d
def b(x): return str(x) in ('True', 'true', '1', '1.0')
ALL = '--all' in sys.argv
for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
    p = E / (lab + '.json')
    if not p.exists(): print('CLIPSPEED %s MISSING' % lab); continue
    R = sorted([r for r in json.load(open(p)) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('ax'), list) and isinstance(r.get('vb_ball_l'), list)], key=lambda r: f(r['t']))
    n = len(R); T = [f(r['t']) for r in R]
    spans = []; k = 0
    while k < n:
        if 'JogRev' in str(R[k].get('av_Phase27_SelectedObject')):
            j = k
            while j + 1 < n and 'JogRev' in str(R[j + 1].get('av_Phase27_SelectedObject')): j += 1
            spans.append((k, j)); k = j + 1
        else: k += 1
    if not spans: print('CLIPSPEED %s no authored clip' % lab); continue
    for (k0, k1) in spans:
        name = str(R[k0].get('av_Phase27_SelectedObject'))[-10:]
        print('CLIPSPEED %s clip %s entry t %.3f ct %.3f (%d frames)' % (lab[-28:], name, T[k0], f(R[k0].get('av_Phase27_SelectedTime')), k1 - k0 + 1))
        print('   dt    ct   v_act  desV   cmd  On cOn  diff   integ | ballL_x ballR_x')
        integ = 0.0; x0 = R[k0]['ax'][0]; mx = 0.0; rows = 0
        for k in range(k0, k1 + 1):
            dt = T[k] - T[k - 1]
            yaw = math.radians(f(R[k].get('ay'))); fx, fy = math.cos(yaw), math.sin(yaw)
            va = ((R[k]['ax'][0] - R[k - 1]['ax'][0]) * fx + (R[k]['ax'][1] - R[k - 1]['ax'][1]) * fy) / dt if dt > 0 else 0.0
            dv = f(R[k].get('av_SHM228_DesV')); cmd = f(R[k].get('av_SHM228_Cmd'))
            on = b(R[k].get('av_SHM228_On')); con = b(R[k].get('cv_ClipSpeedOn'))
            if abs(dv) > 1: integ += (va - dv) * dt
            if k - k0 >= 3 and abs(dv) > 1: mx = max(mx, abs(va - dv))
            if ALL or (k - k0) % 2 == 0:
                print('  %5.2f %5.3f %6.0f %5.0f %5.0f  %s  %s  %6.0f %7.1f | %7.1f %7.1f' % (T[k] - T[k0], f(R[k].get('av_Phase27_SelectedTime')), va, dv, cmd, '1' if on else '.', '1' if con else '.', va - dv if abs(dv) > 1 else 0.0, integ, R[k]['vb_ball_l'][0] - x0, R[k]['vb_ball_r'][0] - x0))
            rows += 1
            if rows > 70: break
        print('   summary: max|v_act-desV| after frame 3 = %.0f cm/s, integral(v_act-desV) = %.1f cm' % (mx, integ))
        break
