"""xr_design.py (offline, Blender-bundled Python + numpy; no Unreal): Exterior World Redesign R1 - macro redesign of the REAR region
(house spur -> east side trail -> rib compression -> hollow crossing -> valley climb -> saddle glade + lookback to the roof).

usage: xr_design.py <recon dir> <out dir> [variant]
Reads recon/height_before.u16 + foliage.json + actors.json; writes to <out dir>:
  height_<v>.u16       designed heightmap (same 1017x1017 grid, untouched outside the region / protected zones)
  height_<v>.png       RG16 PNG of it (R = high byte, G = low byte) for the landscape RG import route of FrontRefugeE2/apply_height.py
  plan_<v>.json        file, verification samples, trail polyline + profile, landforms, zones, stats
  foliage_<v>.json     per changed component {mesh, cull, n, xf_after} (xf_before stays in recon/foliage.json = restore source)
  overlay_<v>.json     map overlay (trail, hollow, zones) for xr_maps.py
Design rules (Sphirus AGENTS / level-art skills): terrain first; existing instances are REDISTRIBUTED (count per component unchanged), nothing
added; house footprint + yard props + pond zone are protected (zero height change, no instance moves); every instance keeps its embedding
(z - ground) on the new ground."""
import sys, os, json, math, zlib, struct, random
import numpy as np

R, OUTD = sys.argv[1], sys.argv[2]
V = sys.argv[3] if len(sys.argv) > 3 else 'r1'
os.makedirs(OUTD, exist_ok=True)
OX, OY, N = -50040.0, -50225.0, 1017
H0 = np.fromfile(os.path.join(R, 'height_before.u16'), dtype='<u2').reshape(N, N)
Z0 = (H0.astype(np.float64) - 32768.0) * 100.0 / 128.0
F = json.load(open(os.path.join(R, 'foliage.json')))
rng = random.Random(1031)

# ---------------------------------------------------------------- region / protection
RX0, RX1, RY0, RY1 = -1500.0, 7500.0, -8200.0, 3200.0          # outer edit box (cm); 6 m feather inside it
i0, i1 = int((RX0 - OX) / 100), int((RX1 - OX) / 100) + 1
j0, j1 = int((RY0 - OY) / 100), int((RY1 - OY) / 100) + 1
xs = OX + np.arange(i0, i1) * 100.0; ys = OY + np.arange(j0, j1) * 100.0
X, Y = np.meshgrid(xs, ys)
Zr = Z0[j0:j1, i0:i1].copy()
ss = lambda a, b, v: np.clip((v - a) / (b - a), 0, 1) ** 2 * (3 - 2 * np.clip((v - a) / (b - a), 0, 1))
PROTECT = [(-350, 1870, -350, 1490, 'house+3.5m'), (450, 2650, -1150, 150, 'backyard props, steps, fence/gate, yard catalog'),
           (-3000, 2300, 1490, 9000, 'front, descent, pond basin and pond-side path (outside R1)')]


def rect_dist(x, y, r):
    dx = np.maximum(np.maximum(r[0] - x, 0), x - r[1]); dy = np.maximum(np.maximum(r[2] - y, 0), y - r[3])
    return np.hypot(dx, dy)


def protect_w(x, y):
    d = np.min(np.stack([rect_dist(x, y, r) for r in PROTECT]), axis=0)
    edge = np.minimum.reduce([x - RX0, RX1 - x, y - RY0, RY1 - y])
    return ss(0, 400, d) * ss(0, 600, edge)


P = protect_w(X, Y)


def seg_dist(x, y, a, b):
    vx, vy = b[0] - a[0], b[1] - a[1]; L2 = vx * vx + vy * vy
    t = np.clip(((x - a[0]) * vx + (y - a[1]) * vy) / L2, 0, 1)
    return np.hypot(x - a[0] - vx * t, y - a[1] - vy * t), t


def poly_dist(x, y, pts):
    """distance to a polyline and normalised arc position (0..1) of the closest point"""
    best = np.full(np.shape(x), 1e18); arc = np.zeros(np.shape(x)); acc = 0.0
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]; tot = sum(lens)
    for (a, b), L in zip(zip(pts, pts[1:]), lens):
        d, t = seg_dist(x, y, a, b); m = d < best
        best = np.where(m, d, best); arc = np.where(m, (acc + t * L) / tot, arc); acc += L
    return best, arc


# ---------------------------------------------------------------- macro / meso landforms (delta, cm)
# value-noise for irregular (not stamped) forms
PN = [rng.random() for _ in range(4096)]


def vn(x, y, s, o=0):
    x = x / s + o * 17.3; y = y / s - o * 9.1; ix, iy = np.floor(x).astype(int), np.floor(y).astype(int); fx, fy = x - ix, y - iy
    h = lambda a, b: np.array(PN)[(a * 73856093 ^ b * 19349663) & 4095]
    ux, uy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    return (h(ix, iy) * (1 - ux) + h(ix + 1, iy) * ux) * (1 - uy) + (h(ix, iy + 1) * (1 - ux) + h(ix + 1, iy + 1) * ux) * uy - .5


VARIANTS = {
 'r1': {'landforms': [  # name, polyline, peak cm at start, peak cm at end, sigma cm, end taper (fraction), irregularity
    ('house_spur', [(1000, -1350), (1050, -2300), (1150, -3400)], 180, 180, 900, .30, .30),
    ('east_rib', [(4700, -2600), (3900, -2400), (3250, -2280)], 260, 260, 430, .22, .25),
    ('ridge_gully', [(4900, -760), (4100, -700), (3350, -620)], -160, -160, 300, .20, .25),
    ('ridge_toe', [(3900, 1300), (3550, 550)], 120, 120, 420, .30, .30),
    ('hollow', [(1500, -5300), (1750, -4300), (2050, -3500), (2350, -2800), (2500, -2100), (2450, -1500), (2400, -1200)], -85, -85, 260, .15, .20)],
    'smooth': None, 'foot': None},
 'r2': {'landforms': [
    # spurs project OUT of the straight east wall: small where they leave the ridge, strongest at the toe (they end in the valley floor)
    ('spur_north', [(5600, -2900), (4500, -2550), (3550, -2300)], 80, 360, 520, .12, .22),     # right wall of the compression
    ('spur_south', [(5400, 500), (4400, 250), (3500, 150)], 60, 280, 480, .12, .22),           # frames the yard gate from the east
    ('bay_gully', [(5300, -1150), (4400, -1050), (3600, -950)], -60, -150, 380, .15, .25),     # concave bay between the spurs (optional pocket)
    ('house_spur', [(950, -1350), (1000, -2400), (1150, -3600)], 230, 260, 1000, .25, .30),   # rear rise: the house sits below a wooded spur
    ('hollow', [(1500, -5300), (1750, -4300), (2050, -3500), (2350, -2800), (2500, -2100), (2450, -1500), (2400, -1200)], -110, -90, 320, .12, .20),
    ('valley_shoulder', [(-300, -4300), (300, -5300)], 120, 160, 650, .25, .30)],              # west valley flank shoulder above the climb
    # old washboard terraces along the former trail band are removed by a broad blur before the new forms are added
    'smooth': (2350, 3700, -3600, 2100, 170.0),
    # floor/wall junction -> long concave foot slope: raise the floor up to 'foot' cm within 7 m west of the wall toe line
    'foot': ([(3350, 1900), (3250, 600), (3200, -900), (3250, -2000), (3150, -3000)], 120, 650)},
}
VARIANTS['r3'] = VARIANTS['r2']; VARIANTS['r4'] = VARIANTS['r2']; VARIANTS['r5'] = VARIANTS['r2']
LANDFORMS = VARIANTS[V]['landforms']
Zr_src = Zr.copy()
if VARIANTS[V]['smooth']:
    sx0, sx1, sy0, sy1, sg = VARIANTS[V]['smooth']
    k = int(3 * sg / 100); ker = np.exp(-(np.arange(-k, k + 1) * 100.0 / sg) ** 2 / 2); ker /= ker.sum()
    Zb = np.apply_along_axis(lambda r: np.convolve(np.pad(r, k, mode='edge'), ker, mode='valid'), 1, Zr)
    Zb = np.apply_along_axis(lambda c: np.convolve(np.pad(c, k, mode='edge'), ker, mode='valid'), 0, Zb)
    msk = ss(0, 500, np.minimum.reduce([X - sx0, sx1 - X, Y - sy0, sy1 - Y]))
    Zr = Zr * (1 - msk) + Zb * msk
D = np.zeros_like(Zr)
for name, pts, pk0, pk1, sg, tp, irr in LANDFORMS:
    d, t = poly_dist(X, Y, pts)
    taper = ss(0, tp, t) * ss(0, tp, 1 - t)
    pk = pk0 + (pk1 - pk0) * t
    D += pk * taper * (1 + irr * vn(X, Y, 650, int(abs(pk0) + abs(pk1)))) * np.exp(-(d / sg) ** 2)
if VARIANTS[V]['foot']:
    fpts, fpk, fw = VARIANTS[V]['foot']
    d, t = poly_dist(X, Y, fpts)
    west = X < np.interp(Y, [p[1] for p in fpts[::-1]], [p[0] for p in fpts[::-1]])
    # full raise on the toe line, fading over fw (floor side) and over 3.5 m up the wall: no step on either side
    D += fpk * np.where(west, 1 - ss(0, fw, d), 1 - ss(0, 350, d)) * ss(0, .1, t) * ss(0, .1, 1 - t)


# ---------------------------------------------------------------- trail (new rear route) + bench
TRAIL = [(1950, 2110), (2380, 1520), (2600, 700), (2700, -100), (2850, -1000), (2920, -1750), (2700, -2450), (2250, -3150),
         (1600, -3950), (1300, -4750), (1180, -5550), (1380, -6250)]
Z1 = Zr + D * P
# trail centreline profile on the shaped ground, smoothed (grade limited) and lowered by a shallow tread
sl = [0.0]
for a, b in zip(TRAIL, TRAIL[1:]):
    sl.append(sl[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
TL = sl[-1]; S = np.arange(0, TL + 1, 50.0)


def at(s):
    for k in range(len(TRAIL) - 1):
        if s <= sl[k + 1] or k == len(TRAIL) - 2:
            L = sl[k + 1] - sl[k]; t = (s - sl[k]) / L; a, b = TRAIL[k], TRAIL[k + 1]
            return a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])


def bil(Zg, x, y, gx0=OX + i0 * 100, gy0=OY + j0 * 100):
    fx, fy = (x - gx0) / 100.0, (y - gy0) / 100.0; ix, iy = int(math.floor(fx)), int(math.floor(fy)); ax, ay = fx - ix, fy - iy
    return (Zg[iy, ix] * (1 - ax) * (1 - ay) + Zg[iy, ix + 1] * ax * (1 - ay) + Zg[iy + 1, ix] * (1 - ax) * ay + Zg[iy + 1, ix + 1] * ax * ay)


TP = np.array([at(s) for s in S]); prof = np.array([bil(Z1, x, y) for x, y in TP])
k = 9 if V not in ('r3', 'r4', 'r5') else 15; prof_s = np.convolve(np.pad(prof, k, mode='edge'), np.ones(2 * k + 1) / (2 * k + 1), mode='same')[k:-k]
dt, at_ = poly_dist(X, Y, TRAIL)
tread_h = np.interp(at_ * TL, S, prof_s) - 9.0                       # 9 cm worn tread below the smoothed bench line
w_bench = np.exp(-(dt / 150.0) ** 2) * 0.85                          # bench: cross-slope flattened over ~1.5 m, soft edge
w_bench *= ss(0, .04, at_) * P                                       # no bench inside protection (house side start)
Zr_new = Z1 * (1 - w_bench) + tread_h * w_bench
DELTA = Zr_new - Zr_src
Z_after = Z0.copy(); Z_after[j0:j1, i0:i1] = Zr_new
H_after = np.clip(np.round(Z_after * 128.0 / 100.0 + 32768.0), 0, 65535).astype('<u2')
# exact zero change where the design does not touch (keeps unmodified samples bit-identical)
H_after[j0:j1, i0:i1] = np.where(np.abs(DELTA) < 0.5, H0[j0:j1, i0:i1], H_after[j0:j1, i0:i1])
Zf = (H_after.astype(np.float64) - 32768.0) * 100.0 / 128.0

# ---------------------------------------------------------------- vegetation / mass redistribution
def zb(Zg, x, y):
    fx, fy = (x - OX) / 100.0, (y - OY) / 100.0; ix, iy = int(math.floor(fx)), int(math.floor(fy)); ax, ay = fx - ix, fy - iy
    return (Zg[iy, ix] * (1 - ax) * (1 - ay) + Zg[iy, ix + 1] * ax * (1 - ay) + Zg[iy + 1, ix] * (1 - ax) * ay + Zg[iy + 1, ix + 1] * ax * ay)


def slope_deg(x, y):
    gx = (zb(Zf, x + 100, y) - zb(Zf, x - 100, y)) / 200; gy = (zb(Zf, x, y + 100) - zb(Zf, x, y - 100)) / 200
    return math.degrees(math.atan(math.hypot(gx, gy)))


def pw(x, y):
    return float(protect_w(np.array([x]), np.array([y]))[0])


def tdist(x, y):
    return float(poly_dist(np.array([x]), np.array([y]), TRAIL)[0][0])


HOLLOW = next(l[1] for l in LANDFORMS if l[0] == 'hollow')
SADDLE = (1450.0, -6250.0); ROOF = (760.0, 600.0); EYE = (1380.0, -6100.0)
OPEN = {  # canopy openings (no big trunks)
    'saddle_glade': lambda x, y: math.hypot(x - SADDLE[0], y - SADDLE[1]) < (700 if V not in ('r3', 'r4', 'r5') else 520),
    'lookback_corridor': lambda x, y: float(seg_dist(np.array([x]), np.array([y]), EYE, ROOF)[0][0]) < 420 and y < -1400,
    'hollow_light': lambda x, y: float(poly_dist(np.array([x]), np.array([y]), HOLLOW[1:-1])[0][0]) < 230,
    'gully_pocket': lambda x, y: math.hypot(x - 3900, y + (700 if V == 'r1' else 1050)) < 350,
}
GROVES = [  # dense STANDS (name, centre, radii cm, rotation deg, min spacing cm): the forest is organised into masses, not scattered
    ('mother_grove', (900, -2700), (1100, 800), 80, 380),       # on the house spur: dark backdrop above the yard
    ('east_ridge_N', (4600, -3400), (900, 1300), 5, 400),       # east ridge face north of the rib
    ('east_ridge_S', (4800, 700), (800, 1100), 0, 400),         # east ridge face south of the gully pocket
    ('rib_grove', (3750, -2350), (700, 420), 10, 400),          # on the east rib: right wall of the compression
    ('portal_east', (3250, -300), (420, 320), 30, 360),         # trail portal opposite the gate
    ('portal_west', (2600, -1450), (330, 260), 0, 360),         # trail portal west, between the yard corner and the hollow
    ('valley_west', (600, -4800), (800, 1200), 15, 420),        # west flank above the climbing trail
    ('valley_east', (2900, -4500), (700, 900), -10, 420),       # east flank across the hollow
    ('crest', (1500, -7250), (2300, 450), 0, 420),              # north crest band: skyline closure behind the saddle
]
if V in ('r3', 'r4', 'r5'):   # r2 review: climb/crossing read as bare slope (no 3-10 m mass), saddle glade unframed
    GROVES += [('climb_frame_W', (800, -4250), (380, 300), 20, 330),   # trunk group on the uphill (west) side of the steep climb
               ('crossing_frame', (2650, -3350), (380, 300), -30, 340), # east of the hollow crossing: the turn has a mass to turn around
               ('saddle_frame_N', (1700, -6950), (650, 300), 10, 340)]  # behind the glade: the release opens INTO a framed room
SPARSE = {  # thinned to a minimum spacing (light, legible ground planes), not emptied
    'yard_east_flat': (lambda x, y: 2400 < x < 3400 and -1200 < y < 1600, 950 if V == 'r1' else 1300),
    'valley_floor': (lambda x, y: float(poly_dist(np.array([x]), np.array([y]), HOLLOW)[0][0]) < (350 if V in ('r4', 'r5') else 650), 800 if V == 'r1' else 1000),
    'bay': (lambda x, y: V != 'r1' and math.hypot(x - 3900, y + 1050) < 650, 1100),
}


def in_ell(x, y, g):
    (cx, cy), (rx, ry), rot = g[1], g[2], math.radians(g[3])
    dx, dy = x - cx, y - cy; u_ = dx * math.cos(rot) + dy * math.sin(rot); v_ = -dx * math.sin(rot) + dy * math.cos(rot)
    return (u_ / rx) ** 2 + (v_ / ry) ** 2


def in_region(x, y):
    return RX0 + 600 < x < RX1 - 600 and RY0 + 600 < y < RY1 - 600 and pw(x, y) > 0.99


BIG = ('SM_PineTree', 'SM_Fir_Tree', 'SM_Oak')
def role(r):
    n = r['mesh'].split('/')[-1]; ht = r['mesh_bounds'][1][2] * 2
    if any(n.startswith(b) for b in BIG) and ht > 800: return 'big'
    if 'Juvenile' in n or 'Young' in n or n.startswith('Pine_08'): return 'young'
    if n.startswith('SM_Bush'): return 'shrub'
    if r['collision'].startswith('QUERY'): return 'hard'           # rocks, trunks, stumps, embankments
    return 'ground'


out_comps, stats = [], {'moved': {}, 'regrounded': 0, 'refused_slots': 0}
# 1) collect the region population
pop = []   # (comp idx, inst idx, role)
for ci, r in enumerate(F):
    ro = role(r)
    for ii, t in enumerate(r['xf']):
        if in_region(t[0], t[1]):
            pop.append((ci, ii, ro))
kept_big = []; move_big = []
for ci, ii, ro in pop:
    if ro != 'big': continue
    x, y = F[ci]['xf'][ii][:2]
    bad = tdist(x, y) < 260 or any(f(x, y) for f in OPEN.values())
    (move_big if bad else kept_big).append((ci, ii))
# thin only the explicit SPARSE zones (keep the rest of the matrix as it stands)
kept2 = []
for ci, ii in sorted(kept_big, key=lambda k: rng.random()):
    x, y = F[ci]['xf'][ii][:2]
    zone = next((v for v in SPARSE.values() if v[0](x, y)), None)
    if zone is None or all(math.hypot(x - F[a]['xf'][b][0], y - F[a]['xf'][b][1]) >= zone[1] for a, b in kept2):
        kept2.append((ci, ii))
    else:
        move_big.append((ci, ii))
kept_big = kept2
stats['sparse_thinned'] = len(move_big)


def free(x, y, sp, placed, trail_clear=300):
    if not in_region(x, y) or tdist(x, y) < trail_clear or any(f(x, y) for f in OPEN.values()) or slope_deg(x, y) > 34        or any(v[0](x, y) for v in SPARSE.values()):
        return False
    return all(math.hypot(x - px, y - py) >= sp for px, py in placed)


placed = [tuple(F[a]['xf'][b][:2]) for a, b in kept_big]
newpos = {}
# 2) fill groves (dense, irregular: rejection sampling inside each ellipse, grove order = importance)
slots = []
for g in GROVES:
    want = int(math.pi * g[2][0] * g[2][1] / (g[4] ** 2) * (0.62 if V == 'r1' else 0.85))
    have = sum(1 for p in placed if in_ell(p[0], p[1], g) < 1)
    tries = 0
    while have < want and tries < 4000:
        tries += 1
        a = rng.random() * 2 * math.pi; rr = math.sqrt(rng.random())
        rot = math.radians(g[3]); u_, v_ = g[2][0] * rr * math.cos(a), g[2][1] * rr * math.sin(a)
        x, y = g[1][0] + u_ * math.cos(rot) - v_ * math.sin(rot), g[1][1] + u_ * math.sin(rot) + v_ * math.cos(rot)
        if free(x, y, g[4] * (0.8 + 0.5 * rng.random()), placed + slots):
            slots.append((x, y)); have += 1
stats['grove_slots'] = len(slots)
# extra trees beyond grove slots go to the east ridge / crest bands (outer enclosure), never into openings
for ci, ii in move_big:
    if slots:
        x, y = slots.pop(0)
    else:
        for _ in range(3000):
            x, y = rng.uniform(4400, 6800), rng.uniform(-7600, 1800)
            if rng.random() < 0.5:
                x, y = rng.uniform(-1000, 6800), rng.uniform(-7900, -6900)
            if free(x, y, 520, placed):
                break
        else:
            for _ in range(4000):
                x, y = rng.uniform(RX0 + 700, RX1 - 700), rng.uniform(RY0 + 700, RY1 - 700)
                if free(x, y, 300, placed):
                    break
            else:
                stats['refused_slots'] += 1; continue
    placed.append((x, y)); newpos[(ci, ii)] = (x, y, rng.uniform(0, 360))
if V in ('r3', 'r4', 'r5') and slots:   # consolidate: matrix trees (outside every stand, off the corridors) fill the remaining stand slots
    matrix = [k for k in kept_big if not any(in_ell(F[k[0]]['xf'][k[1]][0], F[k[0]]['xf'][k[1]][1], g) < 1.3 for g in GROVES)]
    rng.shuffle(matrix); n_cons = min(len(matrix), len(slots))
    for key in matrix[:len(slots)]:
        x, y = slots.pop(0); newpos[key] = (x, y, rng.uniform(0, 360))
    stats['matrix_consolidated'] = n_cons
stats['moved']['big'] = len([k for k in newpos if role(F[k[0]]) == 'big'])
stats['big_in_region'] = len(kept_big) + len(move_big); stats['big_unused_slots'] = len(slots)

# 3) young trees: off the tread / lookback; feather grove edges facing the openings and the hollow banks
edge_pts = []
for g in GROVES:
    for a in np.linspace(0, 2 * math.pi, 26, endpoint=False):
        rot = math.radians(g[3]); s_ = 1.05 + 0.25 * rng.random(); u_, v_ = g[2][0] * s_ * math.cos(a), g[2][1] * s_ * math.sin(a)
        edge_pts.append((g[1][0] + u_ * math.cos(rot) - v_ * math.sin(rot), g[1][1] + u_ * math.sin(rot) + v_ * math.cos(rot)))
for k_, (x, y) in enumerate(at(s) for s in np.arange(800, TL, 380)):
    side = 1 if k_ % 2 else -1; edge_pts.append((x + side * rng.uniform(260, 420), y + side * rng.uniform(-150, 150)))
rng.shuffle(edge_pts)
if V in ('r4', 'r5'):   # r3 review: the 3-10 m band at the climb was bare and pushed shrubs formed a hedge -> rooted clusters instead of lines
    CL = []
    for k_, s_ in enumerate(np.arange(600, TL - 300, 800.0)):
        x0, y0 = at(s_); x1, y1 = at(min(s_ + 50, TL)); tx, ty = x1 - x0, y1 - y0; tn = math.hypot(tx, ty) or 1.0
        side = (1 if k_ % 2 else -1) * (1 if rng.random() > 0.2 else -1); off = rng.uniform(380, 650)
        cx, cy = x0 - ty / tn * off * side, y0 + tx / tn * off * side
        if RX0 + 700 < cx < RX1 - 700 and RY0 + 700 < cy < RY1 - 700 and pw(cx, cy) > 0.6 and tdist(cx, cy) > 330 and not OPEN['lookback_corridor'](cx, cy) and not OPEN['saddle_glade'](cx, cy):
            CL.append((cx, cy))
    if V == 'r5':
        for s_, side, off in ((6450, 1, 420), (6950, -1, 380), (7450, 1, 450), (7950, -1, 400), (8400, 1, 520)):
            x0, y0 = at(s_); x1, y1 = at(min(s_ + 50, TL)); tx, ty = x1 - x0, y1 - y0; tn = math.hypot(tx, ty) or 1.0
            CL.append((x0 - ty / tn * off * side, y0 + tx / tn * off * side))
    stats['clusters'] = len(CL)
    cpts = []
    for cx, cy in CL:
        for m_ in range(rng.randint(3, 5)):
            a = rng.uniform(0, 2 * math.pi); r_ = rng.uniform(60, 170); cpts.append((cx + math.cos(a) * r_, cy + math.sin(a) * r_))
    edge_pts = edge_pts + cpts[::-1]     # pop() takes from the end: clusters first
    SHRUB_PTS = [(cx + rng.uniform(-200, 200), cy + rng.uniform(-200, 200)) for cx, cy in CL for _ in range(3)]
yplaced = []
for ci, ii, ro in pop:
    if ro != 'young': continue
    x, y = F[ci]['xf'][ii][:2]
    lb = OPEN['lookback_corridor'](x, y); bad = tdist(x, y) < 170 or lb or OPEN['saddle_glade'](x, y)
    if not bad and rng.random() < (0.40 if V in ('r4', 'r5') else 0.30) and (V != 'r5' or tdist(x, y) > 1200):   # part of the uniform matrix moves to the edges (layering instead of scatter)
        bad = not any(in_ell(x, y, g) < 1.4 for g in GROVES)
    if not bad:
        yplaced.append((x, y)); continue
    while edge_pts:
        ex, ey = edge_pts.pop()
        if (in_region(ex, ey) or (V in ('r4', 'r5') and pw(ex, ey) > 0.6 and RY0 + 700 < ey < RY1 - 700)) and tdist(ex, ey) > 200 and not OPEN['lookback_corridor'](ex, ey) and not OPEN['saddle_glade'](ex, ey) \
           and slope_deg(ex, ey) < 36 and all(math.hypot(ex - a, ey - b) > 170 for a, b in yplaced):
            newpos[(ci, ii)] = (ex, ey, rng.uniform(0, 360)); yplaced.append((ex, ey)); break
stats['moved']['young'] = len([k for k in newpos if role(F[k[0]]) == 'young'])

# 4) shrubs / soft ground cover off the tread; litter (DeadLeaves/Branch) may stay on the tread
for ci, ii, ro in pop:
    if ro not in ('shrub', 'ground'): continue
    n = F[ci]['mesh'].split('/')[-1]
    if ro == 'ground' and ('DeadLeaves' in n or 'DeadBranch' in n):
        continue
    x, y = F[ci]['xf'][ii][:2]; d = tdist(x, y)
    lim = 140 if ro == 'shrub' else 75
    if d < lim:
        # push perpendicular away from the trail to 1.4-2.6 m (keeps the plant's local group, interrupts edges unevenly)
        best = None
        for s in np.arange(0, TL, 25.0):
            px, py = at(s)
            dd = math.hypot(x - px, y - py)
            if best is None or dd < best[0]:
                best = (dd, px, py)
        _, px, py = best; ang = math.atan2(y - py, x - px) if d > 1 else rng.uniform(0, 2 * math.pi)
        if V in ('r4', 'r5') and ro == 'shrub' and SHRUB_PTS:
            newpos[(ci, ii)] = SHRUB_PTS.pop() + (rng.uniform(0, 360),); continue
        dist = rng.uniform(lim + 60, lim + (380 if V in ('r4', 'r5') else 200))
        jx, jy = (rng.uniform(-150, 150), rng.uniform(-150, 150)) if V in ('r4', 'r5') else (0.0, 0.0)
        newpos[(ci, ii)] = (px + math.cos(ang) * dist + jx, py + math.sin(ang) * dist + jy, None)
stats['moved']['soft'] = len([k for k in newpos if role(F[k[0]]) in ('shrub', 'ground')])

# 5) hard masses: rocks/embankments to the rib toe outcrop (compression) + hollow crossing; trunks off the tread, lying downslope
OUTCROP = [(3150, -2150), (3250, -2420), (3350, -2000), (3050, -2650), (3420, -2280)]
CROSSING = [(2050, -3350), (2380, -3050), (2120, -3000)]
if V in ('r3', 'r4', 'r5'):   # r2 put the crossing stones ON the tread (capsule blocked at 58 m): stones frame the crossing, >= 2 m off the tread;
    # the climb gets a bank outcrop on its uphill side
    OUTCROP = [(3150, -2150), (3250, -2420), (3350, -2000), (900, -4550), (1000, -3950)]
    CROSSING = [(2000, -2950), (2480, -3330), (1850, -3150)]
hard = [(ci, ii) for ci, ii, ro in pop if ro == 'hard']
if V in ('r4', 'r5'):
    for ci, r in enumerate(F):
        if role(r) != 'hard': continue
        for ii, t in enumerate(r['xf']):
            if (ci, ii) not in hard and RX0 < t[0] < RX1 and RY0 < t[1] < RY1 and tdist(t[0], t[1]) < 220                and min(float(rect_dist(np.array([t[0]]), np.array([t[1]]), rr)[0]) for rr in PROTECT[:2]) > 0:
                hard.append((ci, ii)); stats.setdefault('hard_buffer_cleared', []).append([r['mesh'].split('/')[-1], t[0], t[1]])
big_rocks = sorted([k for k in hard if any(s in F[k[0]]['mesh'] for s in ('Embankment', 'GroundRock'))], key=lambda k: -F[k[0]]['mesh_bounds'][1][2])
for k_, key in enumerate(big_rocks[:len(OUTCROP)]):
    x, y = OUTCROP[k_]; newpos[key] = (x, y, rng.uniform(0, 360))
    assert V not in ('r3', 'r4', 'r5') or tdist(x, y) >= 200, ('outcrop on the tread', x, y, tdist(x, y))
stones = [k for k in hard if 'PineStone' in F[k[0]]['mesh'] and k not in newpos]
for k_, key in enumerate(stones[:len(CROSSING)]):
    x, y = CROSSING[k_]; newpos[key] = (x, y, rng.uniform(0, 360))
    assert V not in ('r3', 'r4', 'r5') or tdist(x, y) >= 200, ('crossing stone on the tread', x, y, tdist(x, y))
for key in hard:
    if key in newpos: continue
    x, y = F[key[0]]['xf'][key[1]][:2]
    if tdist(x, y) < 220:
        for _ in range(200):
            a = rng.uniform(0, 2 * math.pi); nx, ny = x + math.cos(a) * rng.uniform(300, 600), y + math.sin(a) * rng.uniform(300, 600)
            if in_region(nx, ny) and tdist(nx, ny) > 260:
                newpos[key] = (nx, ny, None); break
stats['moved']['hard'] = len([k for k in newpos if role(F[k[0]]) == 'hard'])

# 6) build per-component transform lists: moved -> new xy/yaw, all region instances -> regrounded (embedding kept)
for ci, r in enumerate(F):
    xf = [list(t) for t in r['xf']]; changed = False
    for ii, t in enumerate(xf):
        x, y, z = t[0], t[1], t[2]
        if not (RX0 < x < RX1 and RY0 < y < RY1) and (ci, ii) not in newpos:
            continue
        emb = z - zb(Z0, x, y)
        if (ci, ii) in newpos:
            nx, ny, yaw = newpos[(ci, ii)]
            t[0], t[1] = round(nx, 1), round(ny, 1)
            if yaw is not None: t[4] = round(yaw, 2)
            t[2] = round(zb(Zf, nx, ny) + min(emb, 30.0), 1); changed = True
        else:
            nz = zb(Zf, x, y) + emb
            if abs(nz - z) > 0.5:
                t[2] = round(nz, 1); changed = True; stats['regrounded'] += 1
    if changed:
        out_comps.append({'mesh': r['mesh'], 'cull': r['cull'], 'n': len(xf), 'xf_after': xf})

# ---------------------------------------------------------------- write
H_after.tofile(os.path.join(OUTD, 'height_%s.u16' % V))
hi, lo = (H_after >> 8).astype(np.uint8), (H_after & 255).astype(np.uint8)
rgb = np.dstack([hi, lo, np.zeros_like(hi)])
raw = b''.join(b'\x00' + rgb[r].tobytes() for r in range(N))
ch = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
open(os.path.join(OUTD, 'height_%s.png' % V), 'wb').write(b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', N, N, 8, 2, 0, 0, 0)) + ch(b'IDAT', zlib.compress(raw, 6)) + ch(b'IEND', b''))
dj, di = np.nonzero(np.abs(Zf - Z0) > 1.0)
samp = []
for _ in range(60):
    q = rng.randrange(len(dj)); samp.append({'x': int(di[q]), 'y': int(dj[q]), 'height': int(H_after[dj[q], di[q]])})
for (x, y) in ((0, 0), (500, 500), (1016, 1016), (508, 508)):
    samp.append({'x': x, 'y': y, 'height': int(H_after[y, x])})
prof_after = [round(float(zb(Zf, x, y)) / 100, 2) for x, y in TP]
grade = [round(math.degrees(math.atan((prof_after[k + 1] - prof_after[k]) * 100 / 50.0)), 1) for k in range(len(prof_after) - 1)]
stats.update({'trail_len_m': round(TL / 100, 1), 'trail_z_start_end_m': [prof_after[0], prof_after[-1]], 'trail_max_grade_deg': max(abs(g) for g in grade),
              'delta_cm_min_max': [round(float(DELTA.min()), 1), round(float(DELTA.max()), 1)], 'changed_samples': int((np.abs(Zf - Z0) > 1.0).sum()),
              'comps_changed': len(out_comps)})
json.dump({'variant': V, 'file': 'height_%s.png' % V, 'samples': samp, 'trail': TRAIL, 'trail_profile_m': prof_after, 'trail_grade_deg': grade,
           'landforms': LANDFORMS, 'protect': PROTECT, 'groves': GROVES, 'open': list(OPEN), 'saddle': SADDLE, 'eye': EYE, 'roof': ROOF, 'stats': stats},
          open(os.path.join(OUTD, 'plan_%s.json' % V), 'w'), indent=1)
json.dump(out_comps, open(os.path.join(OUTD, 'foliage_%s.json' % V), 'w'))
ov = {'polys': [{'pts': TRAIL, 'rgb': [0.95, 0.2, 0.6], 'w': 3}, {'pts': HOLLOW, 'rgb': [0.2, 0.45, 0.95], 'w': 2},
                {'pts': [EYE, ROOF], 'rgb': [1.0, 0.9, 0.2], 'w': 1}],
      'discs': [{'xy': SADDLE, 'r': 700, 'rgb': [1, 0.95, 0.4], 'a': 0.9, 'ring': 2.0}]}
for g in GROVES:
    rot = math.radians(g[3]); pts = []
    for a in np.linspace(0, 2 * math.pi, 40):
        u_, v_ = g[2][0] * math.cos(a), g[2][1] * math.sin(a); pts.append((g[1][0] + u_ * math.cos(rot) - v_ * math.sin(rot), g[1][1] + u_ * math.sin(rot) + v_ * math.cos(rot)))
    ov['polys'].append({'pts': pts, 'rgb': [0.1, 0.6, 0.2], 'w': 1})
json.dump(ov, open(os.path.join(OUTD, 'overlay_%s.json' % V), 'w'))
print('DESIGN', V, json.dumps(stats))
