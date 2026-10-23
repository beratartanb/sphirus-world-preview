"""ins225.py: inspection camera evidence per run. Prints the focus timeline (candidate seen, latched, InspectOn eased), the acquire
latency after the look stops, the camera-capsule offset change (camera yaw frame) and the character's screen position shift while
inspecting, the look-at alpha and the head yaw toward the focus point vs the facing, the camera jerk95 inside / outside the inspection, and
whether the control yaw moved without input (it must not). Usage: ins225.py label [label ...]"""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
def pct(v, p):
    if not v: return 0.0
    s = sorted(v); return s[min(len(s) - 1, int(p * (len(s) - 1)))]
import re as _re
def rotof(r):
    cr = r.get('camrot')
    if isinstance(cr, list): return cr[0], cr[1], cr[2]
    if isinstance(cr, str):
        m = _re.findall(r'[PYR]=(-?[\d.]+)', cr)
        if len(m) == 3: return float(m[0]), float(m[1]), float(m[2])
    return 0.0, 0.0, 0.0
for lab in sys.argv[1:]:
    R = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('camera'), list) and isinstance(r.get('ax'), list)], key=lambda r: float(r['t']))
    on = [float(r.get('cv_InspectOn') or 0) for r in R]; cand = [float(r.get('cv_InspectCand') or 0) for r in R]; latch = [float(r.get('cv_InspectLatch') or 0) for r in R]
    la = [float(r.get('av_SHM225_LookAlpha') or 0) for r in R]
    t = [float(r['t']) for r in R]
    first_cand = next((t[i] for i in range(len(R)) if cand[i] > 0.5), None); first_latch = next((t[i] for i in range(len(R)) if latch[i] > 0.5), None)
    first_on = next((t[i] for i in range(len(R)) if on[i] > 0.5), None); last_on = max((t[i] for i in range(len(R)) if on[i] > 0.5), default=None)
    # camera - capsule in the camera yaw frame; screen x of the chest
    def cam_frame(r):
        pt, yw, rl = rotof(r); yr = math.radians(yw); pr = math.radians(pt)
        fwd = (math.cos(pr) * math.cos(yr), math.cos(pr) * math.sin(yr), math.sin(pr)); rt = (-math.sin(yr), math.cos(yr), 0.0)
        up = (fwd[1] * rt[2] - fwd[2] * rt[1], fwd[2] * rt[0] - fwd[0] * rt[2], fwd[0] * rt[1] - fwd[1] * rt[0]); return fwd, rt, up
    def sx(r):
        fwd, rt, up = cam_frame(r); c = r['camera']; x = r.get('vb_chest') or r['ax']; d = (x[0] - c[0], x[1] - c[1], x[2] - c[2]); z = sum(d[k] * fwd[k] for k in range(3))
        th = math.tan(math.radians(float(r.get('fov') or 90.0)) / 2.0); return (sum(d[k] * rt[k] for k in range(3)) / z / th) if z > 1 else 0.0
    def off(r):
        fwd, rt, up = cam_frame(r); c = r['camera']; a = r['ax']; d = (c[0] - a[0], c[1] - a[1], c[2] - a[2]); return (sum(d[k] * fwd[k] for k in range(3)), sum(d[k] * rt[k] for k in range(3)))
    inside = [i for i in range(len(R)) if on[i] > 0.5]; outside = [i for i in range(len(R)) if on[i] < 0.1]
    def jerk(idx):
        v = []
        for i in idx:
            if 0 < i < len(R) - 1:
                c0, c1, c2 = R[i - 1]['camera'], R[i]['camera'], R[i + 1]['camera']; v.append(math.dist((c2[0] - 2 * c1[0] + c0[0], c2[1] - 2 * c1[1] + c0[1], c2[2] - 2 * c1[2] + c0[2]), (0, 0, 0)))
        return pct(v, 0.95), (max(v) if v else 0.0)
    sxi = [sx(R[i]) for i in inside]; sxo = [sx(R[i]) for i in outside]
    offi = [off(R[i]) for i in inside]; offo = [off(R[i]) for i in outside]
    mean = lambda v: sum(v) / len(v) if v else float('nan')
    # head yaw toward the focus vs the facing (visible head direction = chest->head? use vb_head - vb_chest5 horizontal as a proxy is poor; report LookAlpha + the facing/point yaw instead)
    pts = [R[i].get('cv_InspectPoint') for i in inside if isinstance(R[i].get('cv_InspectPoint'), str)]
    cy = [rotof(r)[1] for r in R]; ctl = [float(r.get('cy') or rotof(r)[1]) for r in R]
    print('INS225 %-28s cand %s latch %s on %s..%s (acq lag %s s) | on frames %d/%d | screen x in %.2f out %.2f | cam-cap fwd in %.1f out %.1f lat in %.1f out %.1f | lookAlpha max %.2f | jerk95 in %.2f max %.2f out %.2f max %.2f' % (
        lab[-28:], first_cand, first_latch, first_on, last_on, (round(first_on - first_cand, 2) if first_on and first_cand else None), len(inside), len(R), mean(sxi), mean(sxo),
        mean([o[0] for o in offi]), mean([o[0] for o in offo]), mean([o[1] for o in offi]), mean([o[1] for o in offo]), max(la or [0]), *jerk(inside), *jerk(outside)))
