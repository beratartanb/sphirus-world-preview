"""paint_masks.py (offline, Blender Python + numpy): landscape paint-layer weight masks for the Pine Forest Pack landscape material
on the XR2 x9 terrain. 1017x1017 u8 per layer, same grid as the heightmap (origin -50040/-50225, 100 cm per sample):
  Forest      needle floor under the canopy (default everywhere inside the play ring)
  Ground      bare, trodden soil: house pad, landing, yard, shelf foot, 0-3 m around the house and the worn pockets
  GroundPath  the treads (routes A/B/connectors/spurs; width breathes, edges ragged)
  ForestField moss/grass field: the far-shore glade, the saddle, the west clearing, canopy gaps (lighter, mossy)
  WetPuddle   wet margin 0-120 cm above water, inlet floor, the drip hollow behind the house
  SandBeach   unused (0)
usage: paint_masks.py <variant>  -> Saved/Codex/PineForestRedesign_20261104/design/weight_<layer>_<variant>.png + .u8 + preview"""
import sys, os, json, math, zlib, struct
import numpy as np
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, 'Tools/ExteriorWorld_XR2_20261031'); import xr2_layout as LY
V = sys.argv[1] if len(sys.argv) > 1 else 'p1'
OUT = 'Saved/Codex/PineForestRedesign_20261104/design'; os.makedirs(OUT, exist_ok=True)
OX, OY, N = -50040.0, -50225.0, 1017; WATER = -100.0
HF = 'Saved/Codex/ExteriorWorld_XR2_20261031/design/height_x9.u16'
H = np.fromfile(HF, dtype='<u2').reshape(N, N); Z = (H.astype(np.float64) - 32768.0) * 100.0 / 128.0
plan = json.load(open('Saved/Codex/ExteriorWorld_XR2_20261031/design/plan_x9.json'))
RX0, RX1, RY0, RY1 = -7600.0, 6600.0, -9600.0, 11200.0
i0, i1 = int((RX0 - OX) / 100), int((RX1 - OX) / 100) + 1; j0, j1 = int((RY0 - OY) / 100), int((RY1 - OY) / 100) + 1
xs = OX + np.arange(i0, i1) * 100.0; ys = OY + np.arange(j0, j1) * 100.0; X, Y = np.meshgrid(xs, ys); Zr = Z[j0:j1, i0:i1]
rng = np.random.RandomState(1104)
ss = lambda a, b, v: np.clip((v - a) / (b - a), 0, 1) ** 2 * (3 - 2 * np.clip((v - a) / (b - a), 0, 1))
PN = rng.rand(4096)


def vn(x, y, s, o=0):
    x = np.asarray(x, float) / s + o * 17.3; y = np.asarray(y, float) / s - o * 9.1
    ix, iy = np.floor(x).astype(int), np.floor(y).astype(int); fx, fy = x - ix, y - iy
    h = lambda a, b: PN[(a * 73856093 ^ b * 19349663) & 4095]
    ux, uy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    return (h(ix, iy) * (1 - ux) + h(ix + 1, iy) * ux) * (1 - uy) + (h(ix, iy + 1) * (1 - ux) + h(ix + 1, iy + 1) * ux) * uy - .5


def poly_dist(x, y, pts, closed=False):
    pts = list(pts) + ([pts[0]] if closed else []); best = np.full(np.shape(x), 1e18); arc = np.zeros(np.shape(x)); acc = 0.0
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]; tot = sum(lens)
    for (a, b), L in zip(zip(pts, pts[1:]), lens):
        vx, vy = b[0] - a[0], b[1] - a[1]; L2 = vx * vx + vy * vy
        t = np.clip(((x - a[0]) * vx + (y - a[1]) * vy) / L2, 0, 1); d = np.hypot(x - a[0] - vx * t, y - a[1] - vy * t); m = d < best
        best = np.where(m, d, best); arc = np.where(m, (acc + t * L) / tot, arc); acc += L
    return best, arc


def inside(x, y, poly):
    c = np.zeros(np.shape(x), bool)
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        cond = (ay > y) != (by > y); xint = (bx - ax) * (y - ay) / ((by - ay) if by != ay else 1e-9) + ax; c ^= cond & (x < xint)
    return c


# slope (deg) and relative height above water
gy, gx = np.gradient(Zr, 100.0); slope = np.degrees(np.arctan(np.hypot(gx, gy)))
RING = [tuple(p) for p in plan['ring']]; ins = inside(X, Y, RING)
# ---- GroundPath: treads with breathing width and ragged edges
PATH = np.zeros_like(Zr)
for name, pts, hw in (('A_front', LY.ROUTE_A[:4], 55), ('A', LY.ROUTE_A[3:], 85), ('B', LY.ROUTE_B, 75), ('connect', LY.CONNECT, 55), ('descent', LY.DESCENT, 55),
                      ('spur_inlet', LY.SPUR_INLET, 40), ('spur_bay', LY.SPUR_BAY, 40), ('spur_west', LY.SPUR_WEST, 40), ('west_loop', LY.WEST_LOOP, 28)):
    d, arc = poly_dist(X, Y, pts)
    breathe = 1.0 + 0.35 * vn(arc * 9000, np.zeros_like(arc), 700, 3) * 2 + 0.25 * vn(X, Y, 450, 5) * 2
    w = hw * breathe; edge = 45 + 30 * (vn(X, Y, 300, 8) + .5)
    strength = (0.9 if name in ('A', 'B', 'A_front', 'connect', 'descent') else 0.6 if name.startswith('spur') else 0.35)
    PATH = np.maximum(PATH, strength * (1 - ss(w - edge * 0.3, w + edge, d)))
# ---- Ground: trodden / bare pockets (house pad + 3 m, landing, backyard work pocket, shelf foot, saddle seat, west felling clearing)
GROUND = np.zeros_like(Zr)
for (cx, cy), r, s in (((760, 600), 1350, 0.85), ((620, 2620), 420, 0.8), ((600, -800), 520, 0.75), ((1950, 2110), 300, 0.6), ((2680, 5000), 260, 0.5), ((3650, 8000), 300, 0.6), ((-1950, -100), 520, 0.55), ((1450, -6250), 380, 0.5)):
    GROUND = np.maximum(GROUND, s * (1 - ss(r * 0.55, r * 1.15, np.hypot(X - cx, Y - cy) + 90 * vn(X, Y, 350, 11))))
GROUND = np.maximum(GROUND, 0.6 * PATH)      # the tread core is bare too (GroundPath blends over it)
# ---- ForestField: light mossy field in the glade, the saddle, the west clearing, canopy-gap pockets; never on steep ground
FIELD = np.zeros_like(Zr)
for (cx, cy), r, s in (((-900, 8750), 760, 0.95), ((1450, -6250), 560, 0.8), ((-1950, -100), 420, 0.5), ((620, 2620), 380, 0.35), ((3900, -1050), 360, 0.6), ((-3300, 3500), 500, 0.5), ((-2900, 6200), 450, 0.5)):
    FIELD = np.maximum(FIELD, s * (1 - ss(r * 0.5, r * 1.1, np.hypot(X - cx, Y - cy) + 120 * vn(X, Y, 400, 13))))
FIELD *= (1 - ss(14, 26, slope))
FIELD = np.maximum(FIELD, 0.45 * ss(0.62, 0.78, vn(X, Y, 1400, 21) + .5) * (1 - ss(10, 22, slope)) * ins)   # scattered canopy-gap pockets
# ---- WetPuddle: wet margin above the water line, inlet gully floor, drip hollow behind the house
rel = Zr - WATER
WET = 0.9 * ss(-5, 25, rel) * (1 - ss(60, 140, rel)) * (1 - ss(12, 24, slope))
d_in, _ = poly_dist(X, Y, [(2000, 7000), (2650, 7300), (3150, 7650), (3650, 8000)]); WET = np.maximum(WET, 0.7 * (1 - ss(120, 260, d_in)))
WET = np.maximum(WET, 0.6 * (1 - ss(150, 320, np.hypot(X - 1250, Y - (-60)))))                          # rear damp corner (downpipe)
WET *= (1 - PATH * 0.5)
# ---- underwater floor: Ground (dark silt), no path/field
under = rel < -10
# ---- Forest = remainder
layers = {'GroundPath': PATH, 'Ground': GROUND, 'ForestField': FIELD, 'WetPuddle': WET}
tot = np.zeros_like(Zr)
order = ['WetPuddle', 'GroundPath', 'Ground', 'ForestField']   # priority order when weights compete
acc = np.zeros_like(Zr); final = {}
for k in order:
    w = np.clip(layers[k], 0, 1) * (1 - acc); final[k] = w; acc = np.clip(acc + w, 0, 1)
final['Forest'] = 1 - acc
final['Ground'] = np.where(under, 1.0, final['Ground']); final['Forest'] = np.where(under, 0.0, final['Forest'])
for k in ('GroundPath', 'ForestField', 'WetPuddle'):
    final[k] = np.where(under, 0.0, final[k])
final['SandBeach'] = np.zeros_like(Zr)
# outside the design window: Forest 1 (the far landscape never seen from the ring)
full = {}
for k, w in final.items():
    F = np.zeros((N, N), np.float64)
    if k == 'Forest': F[:] = 1.0
    F[j0:j1, i0:i1] = w; full[k] = F


def write_png(path, u8):
    raw = b''.join(b'\x00' + u8[r].tobytes() for r in range(N)); ch = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    open(path, 'wb').write(b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', N, N, 8, 0, 0, 0, 0)) + ch(b'IDAT', zlib.compress(raw, 6)) + ch(b'IEND', b''))


samples = {}
for k, F in full.items():
    u8 = np.clip(np.round(F * 255), 0, 255).astype(np.uint8); u8.tofile('%s/weight_%s_%s.u8' % (OUT, k, V)); write_png('%s/weight_%s_%s.png' % (OUT, k, V), u8)
    sj, si = np.nonzero(u8 > 0)
    pick = [(int(si[q]), int(sj[q]), int(u8[sj[q], si[q]])) for q in rng.choice(len(sj), min(40, len(sj)), replace=False)] if len(sj) else []
    samples[k] = pick + [(0, 0, int(u8[0, 0])), (508, 508, int(u8[508, 508]))]
# preview composite (RGB): path red, ground brown, field light green, wet blue, forest dark green
prev = np.zeros((j1 - j0, i1 - i0, 3), np.float64)
col = {'Forest': (0.10, 0.28, 0.12), 'Ground': (0.42, 0.32, 0.22), 'GroundPath': (0.75, 0.55, 0.35), 'ForestField': (0.45, 0.65, 0.30), 'WetPuddle': (0.20, 0.35, 0.55)}
for k, c in col.items():
    prev += final[k][..., None] * np.array(c)[None, None, :]
prev[under] = (0.08, 0.12, 0.2)
pv = np.clip(np.round(prev * 255), 0, 255).astype(np.uint8)
raw = b''.join(b'\x00' + pv[r].tobytes() for r in range(pv.shape[0])); ch = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
open('%s/weights_preview_%s.png' % (OUT, V), 'wb').write(b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', pv.shape[1], pv.shape[0], 8, 2, 0, 0, 0)) + ch(b'IDAT', zlib.compress(raw, 6)) + ch(b'IEND', b''))
json.dump({'variant': V, 'grid': [OX, OY, N], 'window': [i0, i1, j0, j1], 'layers': list(full), 'samples': samples, 'cover_pct': {k: round(float(final[k].mean() * 100), 1) for k in final}},
          open('%s/weights_%s.json' % (OUT, V), 'w'), indent=1)
print('MASKS', V, {k: round(float(final[k].mean() * 100), 1) for k in final})
