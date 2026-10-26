"""screen229.py label [--from= --to= --step=]: where the visible character is on the player's screen (V2.29 visibility / framing audit).
Projects the visible pelvis, chest (spine_03), head and both balls through the logged camera pose (camera, camrot P/Y/R, fov; 16:9).
x = right, y = up, 1.0 = half the horizontal (x) / vertical (y) field. Flags OFF when the head AND the pelvis are outside |x|>1 or |y|>1
or behind the camera. Summary SCREEN229 {...}: frames off-screen, chest x / y range, worst frame."""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
def f(x, d=0.0):
    try: return float(x)
    except Exception: return d
def rot(r):
    s = str(r.get('camrot', '')); d = {}
    for tok in s.replace('=', ' ').split():
        pass
    try:
        p = float(s.split('P=')[1].split()[0]); y = float(s.split('Y=')[1].split()[0]); rl = float(s.split('R=')[1].split()[0])
    except Exception: return None
    return p, y, rl
def proj(cam, rr, fov, pt):
    p, y, _ = rr; cp, sp, cy, sy = math.cos(math.radians(p)), math.sin(math.radians(p)), math.cos(math.radians(y)), math.sin(math.radians(y))
    fw = (cp * cy, cp * sy, sp); rt = (-sy, cy, 0.0); up = (-sp * cy, -sp * sy, cp)
    d = (pt[0] - cam[0], pt[1] - cam[1], pt[2] - cam[2]); z = sum(d[i] * fw[i] for i in range(3))
    if z <= 1: return None
    th = math.tan(math.radians(fov) / 2.0); tv = th * 9.0 / 16.0
    return (sum(d[i] * rt[i] for i in range(3)) / z / th, sum(d[i] * up[i] for i in range(3)) / z / tv)
if __name__ == '__main__':
    opt = {a.split('=')[0]: a.split('=')[1] for a in sys.argv[1:] if a.startswith('--') and '=' in a}
    for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
        R = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('camera'), list) and isinstance(r.get('vb_head'), list)], key=lambda r: f(r['t']))
        off = 0; xs = []; ys = []; worst = (0, None); out = []
        for r in R:
            rr = rot(r)
            if rr is None: continue
            P = {k: proj(r['camera'], rr, f(r.get('fov'), 60), r[k]) for k in ('vb_head', 'vb_chest', 'vb_pelvis', 'vb_ball_l', 'vb_ball_r')}
            bad = all(P[k] is None or abs(P[k][0]) > 1 or abs(P[k][1]) > 1 for k in ('vb_head', 'vb_pelvis'))
            if bad: off += 1
            c = P['vb_chest']
            if c: xs.append(c[0]); ys.append(c[1])
            t = f(r['t'])
            if f(opt.get('--from'), -1) <= t <= f(opt.get('--to'), -1):
                out.append('%.2f chest %s head %s pelvis %s' % (t, '(%.2f,%.2f)' % c if c else 'behind', '(%.2f,%.2f)' % P['vb_head'] if P['vb_head'] else 'behind', '(%.2f,%.2f)' % P['vb_pelvis'] if P['vb_pelvis'] else 'behind'))
        for o in out: print(o)
        print('SCREEN229 %s %s' % (lab, json.dumps({'frames': len(R), 'offscreen_frames': off, 'chest_x': [round(min(xs), 2), round(max(xs), 2)] if xs else None, 'chest_y': [round(min(ys), 2), round(max(ys), 2)] if ys else None})))
