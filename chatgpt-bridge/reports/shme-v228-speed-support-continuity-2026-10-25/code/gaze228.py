"""gaze228.py label [label ...] [--t0=A --t1=B]: what the HEAD actually does during inspection. The harness logs the head bone's visible X and Z
axes (vax_head, vaz_head; world unit vectors) and the chest (spine_03) axes. The head forward axis is derived from an approved neutral
frame: at the first frame with InspectOn < 0.05 and speed < 5 (idle, head along the body), the local axis (X, Y = Z x X, or Z, with either
sign) whose world direction is closest to the actor facing is taken as FORWARD (printed); then per frame the head forward in the world ->
head yaw / pitch, compared with (a) the direction head -> InspectPoint (gaze error, deg), (b) the body facing (head-vs-body yaw = neck
yaw), (c) the chest forward (head-vs-chest yaw). Reports the yaw/pitch extremes while InspectOn > 0.5, the time to reach within 10 deg of
the target after the latch, and the error trend. No Euler component is read as head yaw."""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
def f(x, d=0.0):
    try: return float(x)
    except Exception: return d
def norm(v):
    l = math.sqrt(sum(a * a for a in v)); return [a / l for a in v] if l > 1e-9 else [1.0, 0.0, 0.0]
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def yawpitch(v): return math.degrees(math.atan2(v[1], v[0])), math.degrees(math.asin(max(-1.0, min(1.0, v[2]))))
def wrap(a): return (a + 180.0) % 360.0 - 180.0
t0 = t1 = None
for a in sys.argv[1:]:
    if a.startswith('--t0='): t0 = float(a[5:])
    if a.startswith('--t1='): t1 = float(a[5:])
for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
    p = E / (lab + '.json')
    if not p.exists(): print('GAZE228 %s MISSING' % lab); continue
    R = sorted([r for r in json.load(open(p)) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('vax_head'), list) and isinstance(r.get('vb_head'), list)], key=lambda r: f(r['t']))
    if not R: print('GAZE228 %s no head axes' % lab); continue
    def axes(r, bone):
        X = norm(r['vax_' + bone]); Z = norm(r['vaz_' + bone]); Y = norm(cross(Z, X)); return X, Y, Z
    neutral = next((r for r in R if f(r.get('cv_InspectOn')) < 0.05 and f(r.get('Speed2D')) < 5.0 and f(r['t']) > 1.0), R[0])
    face = [math.cos(math.radians(f(neutral.get('ay')))), math.sin(math.radians(f(neutral.get('ay')))), 0.0]
    X, Y, Z = axes(neutral, 'head')
    cands = {'+X': X, '-X': [-a for a in X], '+Y': Y, '-Y': [-a for a in Y], '+Z': Z, '-Z': [-a for a in Z]}
    fwd_name = max(cands, key=lambda k: dot(cands[k], face))
    def fwd(r, bone):
        X, Y, Z = axes(r, bone); c = {'+X': X, '-X': [-a for a in X], '+Y': Y, '-Y': [-a for a in Y], '+Z': Z, '-Z': [-a for a in Z]}; return c[fwd_name]
    print('GAZE228 %s head forward = local %s (neutral frame t %.2f, cos to facing %.3f)' % (lab[-28:], fwd_name, f(neutral['t']), dot(cands[fwd_name], face)))
    print('   t     On   head_yaw  pitch | gaze_err  yaw_vs_body  yaw_vs_chest | dist')
    on_frames = []; latch_t = None; reach_t = None
    for r in R:
        t = f(r['t'])
        if (t0 is not None and t < t0) or (t1 is not None and t > t1): continue
        on = f(r.get('cv_InspectOn'))
        hf = fwd(r, 'head'); hy, hp = yawpitch(hf)
        ip = r.get('cv_InspectPoint'); hb = r['vb_head']
        if isinstance(ip, list) and len(ip) == 3:
            tv = norm([ip[0] - hb[0], ip[1] - hb[1], ip[2] - hb[2]]); err = math.degrees(math.acos(max(-1.0, min(1.0, dot(hf, tv))))); dist = math.hypot(ip[0] - hb[0], ip[1] - hb[1])
        else: err = float('nan'); dist = float('nan')
        body_yaw = f(r.get('ay')); yb = wrap(hy - body_yaw)
        cf = fwd(r, 'spine_03') if isinstance(r.get('vax_spine_03'), list) else None
        yc = wrap(hy - yawpitch(cf)[0]) if cf else float('nan')
        if on > 0.5:
            on_frames.append((t, hy, hp, err, yb, yc))
            if latch_t is None: latch_t = t
            if reach_t is None and err < 10.0: reach_t = t
        if on > 0.05 and int(round(t * 30)) % 6 == 0:
            print('  %5.2f %4.2f %8.1f %6.1f | %8.1f %11.1f %12.1f | %5.0f' % (t, on, hy, hp, err, yb, yc, dist))
    if on_frames:
        print('   summary: InspectOn>0.5 for %.2f s | gaze err min %.1f max %.1f mean %.1f deg | head-vs-body yaw %+.1f..%+.1f | head-vs-chest yaw %+.1f..%+.1f | pitch %+.1f..%+.1f | within 10 deg after %s s' % (
            on_frames[-1][0] - on_frames[0][0], min(x[3] for x in on_frames), max(x[3] for x in on_frames), sum(x[3] for x in on_frames) / len(on_frames),
            min(x[4] for x in on_frames), max(x[4] for x in on_frames), min(x[5] for x in on_frames), max(x[5] for x in on_frames), min(x[2] for x in on_frames), max(x[2] for x in on_frames),
            ('%.2f' % (reach_t - latch_t)) if reach_t else 'never'))
    else: print('   InspectOn never > 0.5')
