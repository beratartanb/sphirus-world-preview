"""contactslip.py <label> [...] [--mesh=vb|mx] [--th=2.0] [--top=6] [--json]
Ground-relative contact slip of the rendered feet (V2.8; replaces the speed-gated skate_report for contact questions).

Why: skate_report.py counts a "plant" only while the ball moves slower than 45 cm/s and sits within 12 cm of its 1 s running
minimum - a fast slide therefore ends or splits the plant and is NOT counted, and a lifted-but-slow foot can be counted.
Here contact is decided by HEIGHT ONLY, against the floor (mesh root z on the flat QA floor), and the slip is measured at the
point that actually touches the ground, so a correct heel strike / heel-off / toe roll (rotation about the contact) is not slip:
  - ankle A = foot_<s>, ball B = ball_<s> (world); u = B - A (foot axis); n = world-down made orthogonal to u (sole normal)
  - calibration per run and foot: b0 / a0 = 3rd-percentile ball / ankle height over the floor (= flat stance on the floor)
  - ball contact: B_z - floor < b0 + TH; heel contact: A_z - floor < a0 + TH (TH default 2 cm)
  - contact point C: ball on the floor -> B (flat foot / heel-off / toe roll: rotation about B is not slip); heel only -> ankle xy
    (heel strike; the heel is under the ankle - its small arc is counted, conservative); a stance = consecutive contact frames
  - slip = horizontal path length of the SAME contact point between consecutive frames (type switches are not counted),
    net = horizontal distance between the first and last position of the dominant contact type
Phases: landing = first --land s (0.10) of a stance, toe-off = last --off s (0.15), mid-stance = the planted foot between them
(the primary number: a planted foot that moves). Output per run: stances, p50 / p90 / max per phase (cm), worst stances with time, stage, duration, contact-type sequence, and the
peak contact-point speed. --mesh=mx uses the Motion Matching driver mesh bones (mx_foot / mx_ball, harness "mbones") instead of
the visible body (vb_) -> retarget / visible-body contributions appear as the difference."""
import json, math, sys, pathlib, statistics as stt
def root():
    p = pathlib.Path(__file__).resolve()
    for q in p.parents:
        if (q / 'sphirus.uproject').exists(): return q
    raise SystemExit('project root not found')
E = root() / 'Saved/Codex/SHME_V1_20260925/Evidence'
args = [a for a in sys.argv[1:] if not a.startswith('--')]; opt = dict(a[2:].split('=', 1) if '=' in a else (a[2:], '1') for a in sys.argv[1:] if a.startswith('--'))
MESH = opt.get('mesh', 'vb'); TH = float(opt.get('th', 2.0)); TOP = int(opt.get('top', 6)); LAND = float(opt.get('land', 0.10)); OFF = float(opt.get('off', 0.15))
def key(kind, s): return ('vb_%s_%s' if MESH == 'vb' else 'mx_%s_%s') % (kind, s)
def load(lab):
    R = [r for r in json.load(open(E / (lab + '.json'))) if r.get('t') is not None and isinstance(r.get('mh_root'), list)]
    o = []
    for r in R:
        if o and abs(float(r['t']) - float(o[-1]['t'])) < 0.004: o[-1] = r
        else: o.append(r)
    return o
def sub(a, b): return [a[i] - b[i] for i in range(3)]
def add(a, b): return [a[i] + b[i] for i in range(3)]
def sc(a, k): return [x * k for x in a]
def dot(a, b): return sum(a[i] * b[i] for i in range(3))
def nrm(a):
    l = math.sqrt(dot(a, a)) or 1.0; return [x / l for x in a]
def analyse(lab):
    R = load(lab); out = {'label': lab, 'mesh': MESH, 'feet': {}}
    allst = []
    for s in ('l', 'r'):
        rows = [r for r in R if isinstance(r.get(key('foot', s)), list) and isinstance(r.get(key('ball', s)), list)]
        if len(rows) < 20: out['feet'][s] = 'no data'; continue
        fl = [float(r['mh_root'][2]) for r in rows]
        A = [r[key('foot', s)] for r in rows]; B = [r[key('ball', s)] for r in rows]
        U = [sub(b, a) for a, b in zip(A, B)]
        N = []
        for u in U:
            d = [0.0, 0.0, -1.0]; un = nrm(u); n = sub(d, sc(un, dot(d, un))); N.append(nrm(n))
        bz = [b[2] - f for b, f in zip(B, fl)]
        # calibration: frames where the foot axis is level (|u_z| small) and the ball is near its lowest -> flat stance
        b0 = sorted(bz)[max(0, int(0.03 * len(bz)))]
        az = [a[2] - f for a, f in zip(A, fl)]; a0 = sorted(az)[max(0, int(0.03 * len(az)))]
        # flat stance = ball on the floor AND ankle at its own lowest (the ankle->ball axis slopes ~20 deg even when flat)
        flat = [i for i in range(len(rows)) if bz[i] < b0 + 0.6 and az[i] < a0 + 0.8]
        # heel phase (heel strike, toes still up): the ankle sits within TH of its flat-stance height -> contact point = ankle xy
        # (the heel is under / just behind the ankle; rotating about the heel moves the ankle xy by <= ~1-2 cm, counted as slip).
        # ball phase (flat foot, heel-off, toe roll): the ball is on the floor -> contact point = ball (rolling about it = no slip)
        h = None; H = A
        heel_c = [az[i] < a0 + TH for i in range(len(rows))]; ball_c = [bz[i] < b0 + TH for i in range(len(rows))]
        T = [float(r['t']) for r in rows]; i = 0
        while i < len(rows):
            if not (heel_c[i] or ball_c[i]): i += 1; continue
            j = i
            while j + 1 < len(rows) and (heel_c[j + 1] or ball_c[j + 1]) and T[j + 1] - T[j] < 0.2: j += 1
            if T[j] - T[i] >= 0.05:
                path = 0.0; vmax = 0.0; seq = []; pts = {'H': [], 'B': [], 'F': []}
                def cp(k):
                    if ball_c[k]: return ('F' if heel_c[k] else 'B'), B[k][:2]
                    return 'H', H[k][:2]
                prev = None; part = {'land': 0.0, 'mid': 0.0, 'off': 0.0}
                for k in range(i, j + 1):
                    ty, p = cp(k); pts[ty].append(p)
                    if not seq or seq[-1] != ty: seq.append(ty)
                    if prev and prev[0] == ty:
                        d = math.hypot(p[0] - prev[1][0], p[1] - prev[1][1]); path += d; vmax = max(vmax, d / max(T[k] - T[k - 1], 1e-3))
                        # phase within the stance: landing (first LAND s), toe-off (last OFF s), mid-stance (the planted foot)
                        ph = 'land' if T[k] - T[i] <= LAND else ('off' if T[j] - T[k] < OFF else 'mid')
                        part[ph] += d
                    prev = (ty, p)
                dom = max(pts, key=lambda q: len(pts[q])); P_ = pts[dom]
                net = math.hypot(P_[-1][0] - P_[0][0], P_[-1][1] - P_[0][1]) if len(P_) > 1 else 0.0
                allst.append({'foot': s, 't0': round(T[i], 2), 'dur': round(T[j] - T[i], 2), 'stage': str(rows[i].get('stage')), 'seq': ''.join(seq),
                              'path': round(path, 2), 'net': round(net, 2), 'vmax': round(vmax, 1), 'land': round(part['land'], 2), 'mid': round(part['mid'], 2), 'off': round(part['off'], 2)})
            i = j + 1
        out['feet'][s] = {'b0': round(b0, 2), 'a0': round(a0, 2), 'flat_frames': len(flat)}
    out['stances'] = len(allst)
    for k in ('path', 'mid', 'off', 'land'):
        ps = sorted(x[k] for x in allst)
        if ps: out[k] = {'p50': round(ps[len(ps) // 2], 2), 'p90': round(ps[int(0.9 * (len(ps) - 1))], 2), 'max': round(ps[-1], 2)}
    out['worst'] = sorted(allst, key=lambda x: -x['mid'])[:TOP]; out['all'] = allst
    return out
res = [analyse(l) for l in args]
if 'json' in opt: print(json.dumps(res, indent=1))
else:
    for o in res:
        f_ = lambda k: '%s/%s/%s' % tuple(o.get(k, {}).get(q, '-') for q in ('p50', 'p90', 'max'))
        print('%-26s [%s] stances %d | MID-STANCE slip p50/p90/max %s cm | toe-off %s | landing %s | total %s' % (o['label'], o['mesh'], o['stances'], f_('mid'), f_('off'), f_('land'), f_('path')))
        for w in o['worst']: print('    %s t%6.2f %-18s dur %.2f %-5s mid %5.1f off %5.1f land %5.1f net %5.1f vmax %5.1f' % (w['foot'], w['t0'], w['stage'][-18:], w['dur'], w['seq'], w['mid'], w['off'], w['land'], w['net'], w['vmax']))
