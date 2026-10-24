"""inspect226.py: inspection evidence per run and phase. Phases from the InspectOn timeline (first on-window); 'before' = the 0.8 s standing
before the candidate appears, 'inspecting' = the on-window, 'after' = 0.8 s after it ends. Per phase: camera-capsule distance, FOV, the
character's screen x (chest), and the VISIBLE head / neck / pelvis yaw toward the focus point (world axes vax_*, parsed from the telemetry
strings). Also the control yaw change without input inside the window (must be 0) and the hit-actor sequence. Usage: inspect226.py label..."""
import json, sys, math, re, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
FIX = next((a.split('=')[1] for a in sys.argv[1:] if a.startswith('--point=')), None)
FIXP = [float(x) for x in FIX.split(',')] if FIX else None
def vec(s):
    if isinstance(s, list): return s
    m = re.findall(r'[XYZ]=(-?[\d.]+)', str(s))
    if len(m) == 3: return [float(x) for x in m]
    m = re.findall(r'(-?[\d.]+)/(-?[\d.]+)/(-?[\d.]+)', str(s))
    return [float(x) for x in m[0]] if m else None
def yaw_of(v): return math.degrees(math.atan2(v[1], v[0]))
def wrap(a): return (a + 180.0) % 360.0 - 180.0
for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
    R = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('camera'), list)], key=lambda r: float(r['t']))
    T = [float(r['t']) for r in R]; on = [float(r.get('cv_InspectOn') or 0) for r in R]
    i0 = next((i for i in range(len(R)) if on[i] > 0.5), None)
    if i0 is None: print('INSPECT226 %-26s no inspection window' % lab[-26:]); continue
    i1 = next((i for i in range(i0, len(R)) if on[i] < 0.5), len(R) - 1)
    ic = next((i for i in range(len(R)) if float(R[i].get('cv_InspectCand') or 0) > 0.5), i0)
    def stats(ia, ib):
        S = R[ia:ib + 1]
        if not S: return None
        d = [math.dist(r['camera'][:2], r['ax'][:2]) for r in S]; fov = [float(r.get('fov') or 0) for r in S]
        hy = []; ny = []; py = []
        for r in S:
            pt = vec(r.get('cv_InspectPoint')) or vec(r.get('av_SHM225_LookPoint')) or FIXP; h = vec(r.get('vax_head')); n = vec(r.get('vax_neck_01')); p = vec(r.get('vax_pelvis'))
            if pt and h and p:
                to = yaw_of((pt[0] - r['ax'][0], pt[1] - r['ax'][1], 0.0)); hy.append(wrap(yaw_of(h) - to)); py.append(wrap(yaw_of(p) - to))
                if n: ny.append(wrap(yaw_of(n) - to))
        m = lambda v: (sum(abs(x) for x in v) / len(v)) if v else float('nan')
        # bone-axis yaw per phase (the axis convention per bone is unknown: compare CHANGES between phases, not absolute errors)
        ay = {}
        for key in ('vax_head', 'vax_neck_01', 'vax_pelvis', 'vax_spine_03'):
            vs = [vec(r.get(key)) for r in S]; vs = [v for v in vs if v]
            if vs: ay[key] = math.degrees(math.atan2(sum(v[1] for v in vs), sum(v[0] for v in vs)))
        tt = []
        for r in S:
            pt = vec(r.get('cv_InspectPoint')) or vec(r.get('av_SHM225_LookPoint')) or FIXP
            if pt: tt.append(yaw_of((pt[0] - r['ax'][0], pt[1] - r['ax'][1], 0.0)))
        return dict(dist=sum(d) / len(d), fov=sum(fov) / len(fov), head=m(hy), neck=m(ny), pelvis=m(py), n=len(S), ay=ay, to=(sum(tt) / len(tt)) if tt else None)
    pre = stats(max(0, ic - 24), max(0, ic - 1)); ins = stats(i0, i1); post = stats(min(len(R) - 1, i1 + 1), min(len(R) - 1, i1 + 24))
    cy = [float(r.get('cy') or 0) for r in R[i0:i1 + 1]]; hits = []
    for r in R[ic:i1 + 1]:
        h = str(r.get('cv_InspectHitName'))
        if not hits or hits[-1] != h: hits.append(h)
    turns = {}
    for key in ('vax_pelvis', 'vax_spine_03', 'vax_neck_01', 'vax_head'):
        if key in pre['ay'] and key in ins['ay']: turns[key[4:]] = wrap(ins['ay'][key] - pre['ay'][key])
    need = wrap(ins['to'] - pre['ay'].get('vax_pelvis', 0.0)) if ins.get('to') is not None and 'vax_pelvis' in pre['ay'] else float('nan')
    print('INSPECT226 %-26s cand %.2f on %.2f..%.2f | cam-cap dist before %.0f / inspecting %.0f / after %.0f | fov %.1f / %.1f | bone yaw TURN from before to inspecting: %s (target direction relative to the pelvis axis before: %.1f) | control yaw range inside %.1f deg | hits %s' % (
        lab[-26:], T[ic], T[i0], T[i1], pre['dist'], ins['dist'], post['dist'], pre['fov'], ins['fov'], {k: round(v, 1) for k, v in turns.items()}, need, max(cy) - min(cy), hits[:3]))
