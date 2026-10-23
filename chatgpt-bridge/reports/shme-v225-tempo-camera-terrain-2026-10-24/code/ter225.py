"""ter224.py <run> [--seg=name:x0:x1,...] : per-foot STEPPING read-out on a terrain course (V2.24). Per segment (capsule x range) and foot:
  swing_min_cm : lowest ball height over the LOCAL ground trace (gzl / gzr) while the foot is in swing (ball moving > 60 cm/s and not
                 within 1.5 cm of its loaded floor) - a value < 2 cm over a rise means the foot does not clear the terrain
  skim_cm      : contact221-style path travelled by a swing foot inside 0-4 cm of the local ground above 60 cm/s
  catch        : frames where the swing foot's local ground is HIGHER than the foot (ball below the ground trace) = toe through the mesh
  plant_slip   : worst planted-contact net displacement (contact221 per foot in the segment window)
  pelvis_h     : visible pelvis height over the local ground mean (min..max); trunk pitch (pelvis->chest) min..max
Segments default to the V2.21 courses: bump B1 (7500-7700), threshold R10 (7780-7830), ramp Dra (7900-8100), step D15 (8280-8330),
xslope (9150-9300); a segment is skipped when no row falls in it."""
import json, sys, math, pathlib, subprocess
P = next(q for q in pathlib.Path(__file__).resolve().parents if (q / 'sphirus.uproject').exists()); E = P / 'Saved/Codex/SHME_V1_20260925/Evidence'
args = [a for a in sys.argv[1:] if not a.startswith('--')]; opt = dict((a[2:].split('=', 1) + [''])[:2] for a in sys.argv[1:] if a.startswith('--'))
SEG = [s.split(':') for s in opt['seg'].split(',')] if opt.get('seg') else [('B1', 7480, 7700), ('B2', 8290, 8500), ('R10', 7770, 7840), ('Dra', 7900, 8120), ('dn15', 7840, 7990), ('up15', 8240, 8400), ('dn28', 8740, 8900), ('XS', 9150, 9320), ('flat', 7100, 7450)]
def V(r, k): x = r.get(k); return x if isinstance(x, list) and len(x) == 3 else None
for lab in args:
    R = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and V(r, 'vb_ball_l') and V(r, 'ax') and r.get('gzl') is not None], key=lambda r: float(r['t']))
    # loaded floor per foot (10th percentile of ball height over its ground while static)
    fl = {}
    for s in 'lr':
        hs = sorted(V(r, 'vb_ball_' + s)[2] - float(r['gz' + s]) for r in R); fl[s] = hs[max(0, int(0.1 * len(hs)))]
    print('TER224 %s  floor L %.1f R %.1f' % (lab, fl['l'], fl['r']))
    for name, x0, x1 in SEG:
        x0, x1 = float(x0), float(x1); W = [(i, r) for i, r in enumerate(R) if x0 <= r['ax'][0] <= x1]
        if len(W) < 4: continue
        T0, T1 = float(W[0][1]['t']), float(W[-1][1]['t'])
        subprocess.run([sys.executable, str(P / 'Tools/SHME_V221_20261021/contact221.py'), lab, '--t0=%s' % T0, '--t1=%s' % T1, '--json'], capture_output=True)
        try: C = json.loads((P / 'Saved/Codex/SHME_V216_20261018/contact' / (lab + '.json')).read_text())
        except Exception: C = None
        out = []
        for s in 'lr':
            smin = 99.0; skim = 0.0; catch = 0; prev = None
            for i, r in W:
                b = V(r, 'vb_ball_' + s); h = b[2] - float(r['gz' + s])
                if prev is not None:
                    dt = float(r['t']) - float(prev['t']); pb = V(prev, 'vb_ball_' + s); d = math.hypot(b[0] - pb[0], b[1] - pb[1]); v = d / dt if dt > 0 else 0
                    if v > 60 and h - fl[s] > 1.5:
                        smin = min(smin, h); skim += d if h < 4.0 else 0.0
                    if h - fl[s] < -1.5: catch += 1   # V2.25 fix: relative to the foot's own flat-floor calibration (the raw h < -1 counted planted frames on flat ground, 1-2 cm under the trace, as catches)
                prev = r
            ps = max([c['net_cm'] for c in C['feet'][s]['contacts']] or [0]) if C else -1
            out.append('%s swing_min %5.1f skim %5.1f catch %2d plant_slip %5.1f' % (s.upper(), smin if smin < 99 else float('nan'), skim, catch, ps))
        ph = [V(r, 'vb_pelvis')[2] - (float(r['gzl']) + float(r['gzr'])) / 2 for i, r in W]
        pit = []
        for i, r in W:
            p, c = V(r, 'vb_pelvis'), V(r, 'vb_chest'); yaw = math.radians(float(r.get('ay') or 0)); f = (math.cos(yaw), math.sin(yaw)); d = (c[0] - p[0], c[1] - p[1], c[2] - p[2]); pit.append(math.degrees(math.atan2(d[0] * f[0] + d[1] * f[1], d[2])))
        print('   %-5s [%6.2f %6.2f] sp %3.0f..%3.0f | %s | %s | pelvis_h %5.1f..%5.1f pitch %5.1f..%5.1f' % (name, T0, T1, min(float(r['Speed2D']) for i, r in W), max(float(r['Speed2D']) for i, r in W), out[0], out[1], min(ph), max(ph), min(pit), max(pit)))
