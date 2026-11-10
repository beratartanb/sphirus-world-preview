# an_effort.py <recA.json> <recB.json> [labelA labelB]: same-input comparison per plan segment (effort off/on, B/C, ...).
# Per segment: E/EUse at end, min SpeedScale, AccScale; capsule speed max; reversal time (S press -> velocity heading
# flips past 90 deg from the start heading); time to 50/90 % of the segment's max speed; stop distance/time after
# release; body-capsule separation max (visible pelvis vs capsule, horizontal); pelvis drop (min of pelvis z - capsule z
# relative to the segment start); shoulder rock (p95-p5 of L-R shoulder elevation).
import json, sys, math
def load(fn): d = json.load(open(fn)); return d['plan'], d['rows']
def pct(v, p):
    v = sorted(v); return v[min(len(v) - 1, max(0, int(round(p * (len(v) - 1)))))] if v else float('nan')
def segstats(rows):
    t = 0; T = []
    for r in rows: T.append(t); t += r['gdt']
    sp = [math.hypot(r['vx'], r['vy']) for r in rows]; mx = max(sp) if sp else 0
    h0 = math.atan2(rows[0]['vy'], rows[0]['vx']) if sp and sp[0] > 30 else None
    rev = None
    if h0 is not None:
        for tt, r, s in zip(T, rows, sp):
            if s > 20 and math.cos(math.atan2(r['vy'], r['vx']) - h0) < 0: rev = tt; break
    t50 = next((tt for tt, s in zip(T, sp) if s >= 0.5 * mx), None) if mx > 50 else None
    t90 = next((tt for tt, s in zip(T, sp) if s >= 0.9 * mx), None) if mx > 50 else None
    stop_t = None; dist = 0
    if sp and sp[0] > 30:
        for tt, r, s in zip(T, rows, sp):
            if s < 5: stop_t = tt; break
            dist += s * r['gdt']
    sep = []; pz = []; rock = []
    for r in rows:
        ub = r.get('ub')
        if not isinstance(ub, dict): continue
        pv = ub['pelvis']; sep.append(math.hypot(pv[0] - r['x'], pv[1] - r['y'])); pz.append(pv[2] - r['z'])
        rock.append((ub['upperarm_l'][2] - ub['clavicle_l'][2]) - (ub['upperarm_r'][2] - ub['clavicle_r'][2]))
    mo = [r['mo'] for r in rows if r.get('mo')]
    return dict(t=t, vmax=mx, rev=rev, t50=t50, t90=t90, stop=stop_t, dist=dist if stop_t is not None else None,
                sep=max(sep) if sep else None, drop=(pz[0] - min(pz)) if pz else None, rock=(pct(rock, .95) - pct(rock, .05)) if rock else None,
                E=mo[-1][2] if mo else None, EUse=mo[-1][3] if mo else None, smin=min(m[0] for m in mo) if mo else None, acc=mo[-1][1] if mo else None)
f = lambda v, n=2: ('%.*f' % (n, v)) if isinstance(v, (int, float)) else '-'
pa, ra = load(sys.argv[1]); pb, rb = load(sys.argv[2]); la = sys.argv[3] if len(sys.argv) > 3 else 'A'; lb = sys.argv[4] if len(sys.argv) > 4 else 'B'
print('| seg | input | %s: vmax / rev / t50 / t90 / stop (s, cm) / sep / drop / rock / E,EUse / Smin / Acc | %s: same |' % (la, lb)); print('|---|---|---|---|')
for s in range(len(pa)):
    A = segstats([r for r in ra if r['s'] == s]); Bs = segstats([r for r in rb if r['s'] == s])
    def row(x): return '%s / %s / %s / %s / %s,%s / %s / %s / %s / %s,%s / %s / %s' % (f(x['vmax'], 0), f(x['rev']), f(x['t50']), f(x['t90']), f(x['stop']), f(x['dist'], 0), f(x['sep'], 0), f(x['drop'], 1), f(x['rock'], 1), f(x['E']), f(x['EUse']), f(x['smin']), f(x['acc']))
    print('| %d | %s | %s | %s |' % (s, pa[s][0] or 'release', row(A), row(Bs)))
