"""cam254.py <label> [t0 t1] [--v] : V2.54 FINAL camera framing per speed state (what the player sees), from the logged camera
transform (yaw = control yaw cy, pitch from the camera to the boom pivot apv; the logged camrot is empty): horizontal distance camera -> pelvis, camera height above the pelvis, camera yaw vs the body facing (3/4 view angle), the
character's horizontal screen position (-1 left .. +1 right) and its screen height (head..feet / visible height at that distance),
FOV. Summary per state (stand < 20, walk 20-200, jog 200-380, sprint > 380 cm/s) + the per-second rate of change of distance / screen size
(zoom pumping)."""
import sys, math
args = [a for a in sys.argv[1:] if not a.startswith('--')]; L = args[0]
T0 = float(args[1]) if len(args) > 1 else 0.0; T1 = float(args[2]) if len(args) > 2 else 1e9; VERB = '--v' in sys.argv
def vec(s):
    p = dict(kv.split('=') for kv in s.split()); return float(p['X']), float(p['Y']), float(p['Z'])
def rot(s):
    p = dict(kv.split('=') for kv in s.split()); return float(p.get('P', 0)), float(p.get('Y', 0)), float(p.get('R', 0))
rows = []
for line in open('Saved/Codex/SHME_V1_20260925/LTP/%s.ltp' % L, encoding='utf8', errors='ignore'):
    d = {}
    for kv in line.rstrip('\n').split('|')[2:]:
        if '=' in kv: k, v = kv.split('=', 1); d.setdefault(k, v)
    try:
        t = float(d['t'])
        if not (T0 <= t <= T1): continue
        c_ = vec(d['camera']); a_ = vec(d['apv']); pit = math.degrees(math.atan2(a_[2] - c_[2], max(1.0, math.hypot(a_[0] - c_[0], a_[1] - c_[1]))))
        rows.append((t, c_, (pit, float(d.get('cy', 0) or 0), 0.0), float(d.get('fov', 60) or 60), vec(d['vb_pelvis']), vec(d['vb_head']), vec(d['vb_ball_l']), vec(d['vb_ball_r']), vec(d['ax']), float(d.get('vwy', 0) or 0)))
    except Exception: pass
def ang(a): return (a + 180.0) % 360.0 - 180.0
st = {}; prev = None; pump = []
for i, (t, c, r, fov, pe, he, bl, br, ax, vwy) in enumerate(rows):
    sp = 0.0
    if i >= 2: sp = math.hypot(ax[0] - rows[i - 2][8][0], ax[1] - rows[i - 2][8][1]) / max(1e-4, t - rows[i - 2][0])
    pitch, yaw, _ = r; cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)); cp, spp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    fwd = (cp * cy, cp * sy, spp); right = (-sy, cy, 0.0); up = (-spp * cy, -spp * sy, cp)
    def proj(p):
        d = (p[0] - c[0], p[1] - c[1], p[2] - c[2]); z = sum(d[k] * fwd[k] for k in range(3)); x = sum(d[k] * right[k] for k in range(3)); y = sum(d[k] * up[k] for k in range(3))
        f = 1.0 / math.tan(math.radians(fov) / 2.0); return (x / max(z, 1.0) * f, y / max(z, 1.0) * f * 16 / 9, z)
    sx, sy_, z = proj(pe); hx, hy, _ = proj(he); fz = min(bl[2], br[2]); fx, fy, _ = proj((pe[0], pe[1], fz))
    size = (hy - fy) / 2.0                                         # fraction of the screen height head..feet
    dist = math.hypot(c[0] - pe[0], c[1] - pe[1]); hgt = c[2] - pe[2]
    face = vwy + 90.0; view = ang(yaw - face)                     # 0 = camera looks along the facing (behind)
    s_ = 'stand' if sp < 20 else 'walk' if sp < 200 else 'jog' if sp < 380 else 'sprint'
    a = st.setdefault(s_, []); a.append((dist, hgt, sx, size, fov, abs(view), fy, hy))
    if prev is not None and t > prev[0]: pump.append((t, (size - prev[1]) / (t - prev[0])))
    prev = (t, size)
    if VERB and i % 6 == 0: print('  %.2f v %4.0f %-6s dist %5.0f hgt %4.0f screen x %+.2f size %.2f fov %4.1f view %+5.0f' % (t, sp, s_, dist, hgt, sx, size, fov, view))
for s_ in ('stand', 'walk', 'jog', 'sprint'):
    a = st.get(s_)
    if not a: continue
    m = lambda k: sum(x[k] for x in a) / len(a)
    print('CAM254 %s %-6s n %4d | dist %5.0f hgt %4.0f | screen x %+.2f size %.2f feet y %+.2f head y %+.2f (-1 = bottom edge) | fov %4.1f | |view| %4.0f deg' % (L, s_, len(a), m(0), m(1), m(2), m(3), m(6), m(7), m(4), m(5)))
if pump: print('CAM254 %s size rate p95 %.2f /s max %.2f /s' % (L, sorted(abs(x[1]) for x in pump)[int(0.95 * (len(pump) - 1))], max(abs(x[1]) for x in pump)))
