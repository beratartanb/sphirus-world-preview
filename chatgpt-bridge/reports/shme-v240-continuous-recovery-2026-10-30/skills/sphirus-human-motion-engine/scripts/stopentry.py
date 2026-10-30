"""stopentry.py <label> [...] [--mesh=vb] : per stop (walk / jog / sprint release) the contact behaviour of the ENTRY into the stop.
For each release: capsule speed, the planted foot at release (lower ball) and its forward offset from the capsule (cm, body frame),
the stop side chosen by the ABP (LS_StopRight), the CP stop clip time at ownership (CP_StopEvalTime), and for 0.6 s after release:
the horizontal travel of every foot point that is on the floor (ball < its flat height + 2 cm) = entry slip, the lowest ball
height relative to its flat height (negative = penetration), and the settle time (both balls static < 1 cm/s). Uses the same
calibration as contactslip.py."""
import json, math, sys, pathlib, statistics as stt, bisect
def root():
    for q in pathlib.Path(__file__).resolve().parents:
        if (q / 'sphirus.uproject').exists(): return q
E = root() / 'Saved/Codex/SHME_V1_20260925/Evidence'
args = [a for a in sys.argv[1:] if not a.startswith('--')]; opt = dict(a[2:].split('=', 1) for a in sys.argv[1:] if a.startswith('--') and '=' in a)
MESH = opt.get('mesh', 'vb'); WIN = float(opt.get('win', 0.6))
def k(kind, s): return ('vb_%s_%s' if MESH == 'vb' else 'mx_%s_%s') % (kind, s)
def isrel(s): s = s.split('+')[-1]; return s == 'mv_stop' or '_rel_' in s
def mf(r, key):
    d = [r[key][i] - r['mh_root'][i] for i in range(3)]; y = math.radians(float(r['my']) + 90); f = (math.cos(y), math.sin(y))
    return (d[0] * f[0] + d[1] * f[1], -d[0] * f[1] + d[1] * f[0], d[2])
for lab in args:
    R = [r for r in json.load(open(E / (lab + '.json'))) if r.get('t') is not None and r.get('stage') and isinstance(r.get(k('ball', 'l')), list) and isinstance(r.get(k('ball', 'r')), list)]
    T = [float(r['t']) for r in R]
    b0 = {s: sorted(r[k('ball', s)][2] - r['mh_root'][2] for r in R)[int(0.03 * len(R))] for s in ('l', 'r')}
    print('== %s [%s] flat ball z L %.1f R %.1f' % (lab, MESH, b0['l'], b0['r']))
    for i in range(1, len(R)):
        if not isrel(str(R[i]['stage'])) or isrel(str(R[i - 1]['stage'])) or float(R[i].get('Speed2D', 0)) < 40: continue
        r0 = R[i]; zl = r0[k('ball', 'l')][2] - r0['mh_root'][2]; zr = r0[k('ball', 'r')][2] - r0['mh_root'][2]
        pl = 'L' if zl < zr else 'R'; off = mf(r0, k('ball', pl.lower()))[0]
        w = [q for q in range(i, len(R)) if T[q] - T[i] <= WIN]
        slip = {}; pen = {}
        for s in ('l', 'r'):
            tot = 0.0; mn = 9.9
            for a, b in zip(w, w[1:]):
                za = R[a][k('ball', s)][2] - R[a]['mh_root'][2]; zb = R[b][k('ball', s)][2] - R[b]['mh_root'][2]
                mn = min(mn, zb - b0[s])
                if za < b0[s] + 2.0 and zb < b0[s] + 2.0:
                    tot += math.hypot(R[b][k('ball', s)][0] - R[a][k('ball', s)][0], R[b][k('ball', s)][1] - R[a][k('ball', s)][1])
            slip[s] = tot; pen[s] = mn
        own = next((R[q] for q in w if str(R[q].get('av_CP_StopOwned')).lower() == 'true'), None)
        print('  t%6.2f %-14s v %4.0f | planted %s at %+5.1f cm | side %s clip t %s | entry slip L %4.1f R %4.1f cm | lowest ball L %+4.1f R %+4.1f' % (
            T[i], str(r0['stage'])[-14:], float(r0.get('Speed2D', 0)), pl, off, 'R' if str((own or {}).get('av_LS_StopRight')).lower() == 'true' else ('L' if own else '-'),
            str((own or {}).get('av_CP_StopEvalTime'))[:5], slip['l'], slip['r'], pen['l'], pen['r']))
