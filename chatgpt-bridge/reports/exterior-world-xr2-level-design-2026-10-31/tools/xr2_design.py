"""xr2_design.py (offline, Blender-bundled Python + numpy; no Unreal): XR2 whole-exterior level-design blockout.

usage: xr2_design.py <recon dir> <out dir> [variant]
Reads recon/height_before.u16 + foliage.json + actors.json (ExteriorRedesign_20261031/recon = the restore source) and writes:
  height_<v>.u16 / .png   designed heightmap (RG16 PNG for the landscape RG import route of xr_apply.py)
  plan_<v>.json           verification samples, routes + profiles, landforms, ring, zones, stats
  foliage_<v>.json        per changed component {mesh, cull, n, xf_after}
  spawn_<v>.json          structural actors to spawn (cliff rocks, deadfall, logs, wade limit) with their collision footprints
  overlay_<v>.json        map overlay

Masterplan (Tools/ExteriorWorld_XR2_20261031/xr2_layout.py holds the shared polylines):
  * one closed WORLD RING of natural barriers: a steep (> walkable 44.8 deg) bank on the outside of the ring, clad with cliff rock /
    deadfall where it is seen from a route, enclosure trees behind it. The ring passes 8-15 m behind every destination.
  * Route A (pond path) and Route B (rear trail, R1 alignment + r6 climb re-route) as worn, benched treads with grade limits.
  * side pockets (SE inlet gully, east bay, west felling clearing, faint west-shore loop) with honest endpoints.
  * interior barriers: east-bank rock shelf (pond path compression, no shortcut to the rear trail), backyard north windthrow
    (the yard is a room whose exit is the gate), shallow-water wade limit (no walking across the pond floor).
  * off-route forest floor made slower to cross with deadwood; big trees regrouped from treads and glades into stands.
Protected (zero height change, no instance moves): house + 3.5 m, backyard props/gate, pond water body."""
import sys, os, json, math, zlib, struct, random
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xr2_layout as LY

R, OUTD = sys.argv[1], sys.argv[2]
V = sys.argv[3] if len(sys.argv) > 3 else 'x1'
os.makedirs(OUTD, exist_ok=True)
OX, OY, N = -50040.0, -50225.0, 1017
H0 = np.fromfile(os.path.join(R, 'height_before.u16'), dtype='<u2').reshape(N, N)
Z0 = (H0.astype(np.float64) - 32768.0) * 100.0 / 128.0
F = json.load(open(os.path.join(R, 'foliage.json')))
rng = random.Random(2031)
WATER = -100.0

RX0, RX1, RY0, RY1 = -7600.0, 6600.0, -9600.0, 11200.0
i0, i1 = int((RX0 - OX) / 100), int((RX1 - OX) / 100) + 1
j0, j1 = int((RY0 - OY) / 100), int((RY1 - OY) / 100) + 1
xs = OX + np.arange(i0, i1) * 100.0; ys = OY + np.arange(j0, j1) * 100.0
X, Y = np.meshgrid(xs, ys)
Zr = Z0[j0:j1, i0:i1].copy(); Zsrc = Zr.copy()
ss = lambda a, b, v: np.clip((v - a) / (b - a), 0, 1) ** 2 * (3 - 2 * np.clip((v - a) / (b - a), 0, 1))
PROTECT = [(-350, 1870, -350, 1490, 'house+3.5m'), (450, 2650, -1150, 150, 'backyard props, steps, fence/gate')]


def rect_dist(x, y, r):
    dx = np.maximum(np.maximum(r[0] - x, 0), x - r[1]); dy = np.maximum(np.maximum(r[2] - y, 0), y - r[3])
    return np.hypot(dx, dy)


def protect_w(x, y):
    d = np.min(np.stack([rect_dist(x, y, r) for r in PROTECT]), axis=0)
    edge = np.minimum.reduce([x - RX0, RX1 - x, y - RY0, RY1 - y])
    return ss(0, 450, d) * ss(0, 800, edge)


WATERBODY = Zsrc < WATER - 20                     # the existing pond body (below 20 cm depth) keeps its exact floor
P = protect_w(X, Y) * (1 - WATERBODY)


def seg_dist(x, y, a, b):
    vx, vy = b[0] - a[0], b[1] - a[1]; L2 = vx * vx + vy * vy
    t = np.clip(((x - a[0]) * vx + (y - a[1]) * vy) / L2, 0, 1)
    return np.hypot(x - a[0] - vx * t, y - a[1] - vy * t), t


def poly_dist(x, y, pts, closed=False):
    pts = list(pts) + ([pts[0]] if closed else [])
    best = np.full(np.shape(x), 1e18); arc = np.zeros(np.shape(x)); acc = 0.0
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]; tot = sum(lens)
    for (a, b), L in zip(zip(pts, pts[1:]), lens):
        d, t = seg_dist(x, y, a, b); m = d < best
        best = np.where(m, d, best); arc = np.where(m, (acc + t * L) / tot, arc); acc += L
    return best, arc


def inside(x, y, poly):
    x = np.asarray(x, float); y = np.asarray(y, float); c = np.zeros(np.shape(x), bool)
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        cond = (ay > y) != (by > y)
        xint = (bx - ax) * (y - ay) / ((by - ay) if by != ay else 1e-9) + ax
        c ^= cond & (x < xint)
    return c


PN = [rng.random() for _ in range(4096)]
PNA = np.array(PN)


def vn(x, y, s, o=0):
    x = np.asarray(x, float) / s + o * 17.3; y = np.asarray(y, float) / s - o * 9.1
    ix_, iy_ = np.floor(x).astype(int), np.floor(y).astype(int); fx_, fy_ = x - ix_, y - iy_
    h = lambda a, b: PNA[(a * 73856093 ^ b * 19349663) & 4095]
    ux, uy = fx_ * fx_ * (3 - 2 * fx_), fy_ * fy_ * (3 - 2 * fy_)
    return (h(ix_, iy_) * (1 - ux) + h(ix_ + 1, iy_) * ux) * (1 - uy) + (h(ix_, iy_ + 1) * (1 - ux) + h(ix_ + 1, iy_ + 1) * ux) * uy - .5


# ================================================================ 1. macro / meso landforms
# R1 rear forms (r5 values) with the r6 bolder spur toes (+4.5 / +5.5 m); hollow re-routed east of the r6 climb
LANDFORMS = [  # name, polyline, peak cm start, peak cm end, sigma cm, end taper, irregularity
    ('spur_north', [(5600, -2900), (4500, -2550), (3550, -2300)], 80, 520, 520, .12, .22),
    ('spur_south', [(5400, 500), (4400, 250), (3500, 150)], 60, 420, 480, .12, .22),
    ('bay_gully', [(5300, -1150), (4400, -1050), (3600, -950)], -60, -150, 380, .15, .25),
    ('house_spur', [(950, -1350), (1000, -2400), (1150, -3600)], 230, 260, 1000, .25, .30),
    ('hollow', [(2300, -5300), (2250, -4300), (2200, -3500), (2350, -2800), (2500, -2100), (2450, -1500), (2400, -1200)], -110, -90, 320, .12, .20),
    ('valley_shoulder', [(-300, -4300), (300, -5300)], 120, 160, 650, .25, .30),
    # pond: the far (south) shore rises behind the glade into a wooded bank; the SW sedge flat stays low
    ('south_bank', [(-3500, 9900), (-1000, 10000), (1800, 9800)], 160, 160, 700, .2, .3),
    ('glade_terrace', [(-1500, 8800), (-400, 8750)], 45, 45, 380, .3, .1),
    # SE inlet gully: a stream valley cut into the SE hill, open to the pond, closed at its head (rock step)
    ('inlet_gully', [(2000, 7000), (2650, 7300), (3150, 7650), (3650, 8000), (4100, 8300)], -60, -330, 380, .08, .15),
    ('inlet_flank_N', [(2900, 6700), (3700, 7200), (4400, 7700)], 140, 260, 380, .2, .25),
    # west woods: the felling clearing sits on a small bench below the NW knoll
]
# flats: (centre, radius cm, blend) -> ground blended toward its own local mean (benches / glades / landing)
FLATS = [((-1950, -100), 600, 0.85), ((-900, 8750), 600, 0.6), ((620, 2620), 330, 0.5), ((1450, -6250), 520, 0.5), ((3650, 8000), 300, 0.7)]
X8 = V not in ('x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7')
if X8:   # x7 review (D06 back view): the glade flat cut a smooth 2-3 m wall into the south bank -> gentler, wider glade blend
    FLATS[1] = ((-900, 8650), 900, 0.3)
D = np.zeros_like(Zr)
for name, pts, pk0, pk1, sg, tp, irr in LANDFORMS:
    d, t = poly_dist(X, Y, pts)
    D += (pk0 + (pk1 - pk0) * t) * ss(0, tp, t) * ss(0, tp, 1 - t) * (1 + irr * vn(X, Y, 650, int(abs(pk0) + abs(pk1)))) * np.exp(-(d / sg) ** 2)
# R1: old washboard terraces along the former trail band are blurred away; floor/wall junction becomes a long concave foot slope
sx0, sx1, sy0, sy1, sg = 2350, 3700, -3600, 2100, 170.0
k = int(3 * sg / 100); ker = np.exp(-(np.arange(-k, k + 1) * 100.0 / sg) ** 2 / 2); ker /= ker.sum()
Zb = np.apply_along_axis(lambda r: np.convolve(np.pad(r, k, mode='edge'), ker, mode='valid'), 1, Zr)
Zb = np.apply_along_axis(lambda c: np.convolve(np.pad(c, k, mode='edge'), ker, mode='valid'), 0, Zb)
msk = ss(0, 500, np.minimum.reduce([X - sx0, sx1 - X, Y - sy0, sy1 - Y]))
Zr = Zr * (1 - msk) + Zb * msk
fpts = [(3350, 1900), (3250, 600), (3200, -900), (3250, -2000), (3150, -3000)]
d, t = poly_dist(X, Y, fpts)
west = X < np.interp(Y, [p[1] for p in fpts[::-1]], [p[0] for p in fpts[::-1]])
D += 120 * np.where(west, 1 - ss(0, 650, d), 1 - ss(0, 350, d)) * ss(0, .1, t) * ss(0, .1, 1 - t)

# ================================================================ 2. world ring: steep natural bank on its outside
RING = [(-600, -7300), (500, -7700), (1500, -7800), (2600, -7500), (3400, -6900), (4000, -6000), (4300, -5000), (4400, -4000), (4900, -3200),
        (5200, -2400), (4800, -1700), (4500, -1100), (4500, -200), (4300, 800), (3900, 1800), (3400, 2650), (3120, 3400), (3080, 4300),
        (3130, 5200), (3050, 6100), (3300, 6750), (3950, 7250), (4650, 7900), (4800, 8650), (4300, 9250), (3200, 9550), (2000, 9550),
        (800, 9600), (-400, 9750), (-1600, 9700), (-2700, 9400), (-3700, 8900), (-4600, 8100), (-5100, 7000), (-5300, 5800), (-5300, 4400),
        (-5200, 3000), (-5000, 1800), (-4800, 600), (-4600, -700), (-4300, -2000), (-3800, -3200), (-3000, -4400), (-2200, -5500), (-1500, -6500)]
# per-vertex bank height (cm): taller where the inside is low or a route looks at it
RING_H = [300, 320, 340, 320, 300, 280, 280, 280, 260, 260, 280, 300, 300, 280, 280, 330, 380, 400, 400, 380, 340, 320, 330, 340, 320, 300,
          300, 300, 320, 320, 300, 300, 280, 280, 270, 270, 270, 270, 270, 270, 280, 300, 320, 320, 320]
assert len(RING_H) == len(RING)
if V not in ('x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7'):
    RING_H[27:30] = [260, 250, 260]
FACE = 120.0                                   # horizontal width of the steep face (cm)
rd, rarc = poly_dist(X, Y, RING, closed=True)
ins = inside(X, Y, RING)
# irregular face line: +-90 cm wander, height +-20 %
wander = 180 * vn(X, Y, 900, 7)
sd = np.where(ins, -rd, rd) + wander                     # > 0 outside
cum = [0.0]
RC = RING + [RING[0]]
for a, b in zip(RC, RC[1:]):
    cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
hv = np.interp(rarc * cum[-1], cum, RING_H + [RING_H[0]]) * (1 + 0.4 * vn(X, Y, 1100, 3))
RINGD = hv * ss(0, FACE, sd) * (1 - ss(1800, 4500, sd)) + 60 * ss(-250, 0, sd) * (1 - ss(0, FACE, sd))   # small toe swell inside
D += RINGD
# interior barrier lines: a steep bank on one side (side +1 = left of the polyline direction is raised), clad with rock below
INNER = [('W1_valley_wall', [(-650, -650), (-950, -1650), (-1500, -2700), (-2100, -3600), (-2700, -4300), (-3350, -4750)], 260, -1)]
if V not in ('x1', 'x2', 'x3', 'x4'):   # x5: the backyard is cut into the slope - a cut bank closes the yard on the north (exit = gate)
    INNER.append(('W0_yard_bank', [(-650, -650), (-450, -1500), (300, -1800), (1200, -1850), (1900, -1750), (2450, -1500)], 230, -1))
for nm, pts, hh, side in INNER:
    best = np.full(X.shape, 1e18); sgn = np.zeros(X.shape); tt = np.zeros(X.shape); acc = 0.0
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    for (a, b), Ls in zip(zip(pts, pts[1:]), lens):
        d_, t_ = seg_dist(X, Y, a, b); m_ = d_ < best
        cr = (b[0] - a[0]) * (Y - a[1]) - (b[1] - a[1]) * (X - a[0])
        best = np.where(m_, d_, best); sgn = np.where(m_, np.sign(cr), sgn); tt = np.where(m_, (acc + t_ * Ls) / sum(lens), tt); acc += Ls
    sdl = best * sgn * side + 140 * vn(X, Y, 800, 11)
    endtap = ss(0, .04, 1 - tt) * np.where(tt >= 0.999, 1 - ss(0, 250, best), 1.0) if nm.startswith('W0') else 1.0
    D += hh * (1 + 0.3 * vn(X, Y, 900, 12)) * ss(0, FACE, sdl) * (1 - ss(1500, 3500, sdl)) * (np.where(tt <= 0.0005, 1 - ss(0, 300, best), 1.0) if V not in ('x3', 'x4', 'x5') else 1.0) * endtap

Z1 = Zr + D * P
for (cx, cy), rad, bl in FLATS:
    m_ = np.hypot(X - cx, Y - cy) < rad * 0.6
    zt = float(np.mean(Z1[m_]))
    wf = bl * (1 - ss(rad * (0.3 if X8 else 0.55), rad, np.hypot(X - cx, Y - cy))) * P
    Z1 = Z1 * (1 - wf) + zt * wf

# ================================================================ 3. routes: benched worn treads with grade limits
CLIMB_R6 = [(2250, -3150), (1850, -3800), (1750, -4500), (1700, -5200), (1550, -5800), (1380, -6250)]   # r6: through the shrub gap
ROUTE_B = LY.ROUTE_B
assert ROUTE_B[7:] == CLIMB_R6
ROUTES = [  # name, pts, half tread width, bench half width, depth cm, min z above water, class
    ('A_front', LY.ROUTE_A[:4], 60, 120, 8, None, 'main'),
    ('A', LY.ROUTE_A[3:], 95, 160, 12, 40, 'main'),
    ('B', ROUTE_B, 80, 150, 10, None, 'main'),
    ('connect', LY.CONNECT, 60, 110, 6, None, 'main'),
    ('descent', LY.DESCENT, 60, 110, 6, None, 'main'),
    ('west_loop', LY.WEST_LOOP, 40, 70, 3, 25, 'faint'),
    ('spur_inlet', LY.SPUR_INLET, 45, 90, 4, None, 'spur'),
    ('spur_bay', LY.SPUR_BAY, 45, 90, 4, None, 'spur'),
    ('spur_west', LY.SPUR_WEST, 45, 90, 4, None, 'spur'),
]


def at(pts, s, cum_):
    for k_ in range(len(pts) - 1):
        if s <= cum_[k_ + 1] or k_ == len(pts) - 2:
            L = cum_[k_ + 1] - cum_[k_]; t_ = (s - cum_[k_]) / L; a, b = pts[k_], pts[k_ + 1]
            return a[0] + t_ * (b[0] - a[0]), a[1] + t_ * (b[1] - a[1])


def zb(Zg, x, y, gx0=OX + i0 * 100, gy0=OY + j0 * 100):
    fx_, fy_ = (x - gx0) / 100.0, (y - gy0) / 100.0; ix_, iy_ = int(math.floor(fx_)), int(math.floor(fy_)); ax, ay = fx_ - ix_, fy_ - iy_
    return (Zg[iy_, ix_] * (1 - ax) * (1 - ay) + Zg[iy_, ix_ + 1] * ax * (1 - ay) + Zg[iy_ + 1, ix_] * (1 - ax) * ay + Zg[iy_ + 1, ix_ + 1] * ax * ay)


Zp = Z1.copy(); RINFO = {}
corr = np.full(Zp.shape, 1e18)                 # distance to the nearest main/spur tread (for clearance masks)
for name, pts, hw, bw, dep, minz, cls in ROUTES:
    cum_ = [0.0]
    for a, b in zip(pts, pts[1:]):
        cum_.append(cum_[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    S = np.arange(0, cum_[-1] + 1, 50.0); TP = np.array([at(pts, s, cum_) for s in S])
    prof = np.array([zb(Zp, x, y) for x, y in TP])
    if minz is not None:
        prof = np.maximum(prof, WATER + minz)
    kk = 13 if cls == 'main' else 7
    prof_s = np.convolve(np.pad(prof, kk, mode='edge'), np.ones(2 * kk + 1) / (2 * kk + 1), mode='same')[kk:-kk]
    if minz is not None:
        prof_s = np.maximum(prof_s, WATER + minz)
    dt, a_ = poly_dist(X, Y, pts)
    tread = np.interp(a_ * cum_[-1], S, prof_s) - dep * (1 - ss(hw * 0.6, hw, dt))
    w = np.exp(-(dt / bw) ** 2) * (0.9 if cls == 'main' else 0.75)
    w *= np.where(protect_w(X, Y) > 0.98, 1.0, protect_w(X, Y))      # no bench inside protection
    w *= 1 - WATERBODY
    Zp = Zp * (1 - w) + tread * w
    if cls != 'faint':
        corr = np.minimum(corr, dt)
    RINFO[name] = {'pts': pts, 'len_m': round(cum_[-1] / 100, 1), 'class': cls, 'hw': hw}

Znew = Zp
DELTA = Znew - Zsrc
Z_after = Z0.copy(); Z_after[j0:j1, i0:i1] = Znew
H_after = np.clip(np.round(Z_after * 128.0 / 100.0 + 32768.0), 0, 65535).astype('<u2')
H_after[j0:j1, i0:i1] = np.where(np.abs(DELTA) < 0.5, H0[j0:j1, i0:i1], H_after[j0:j1, i0:i1])
Zf = (H_after.astype(np.float64) - 32768.0) * 100.0 / 128.0


def zf(x, y):
    return zb(Zf, x, y, OX, OY)


def slope_deg(x, y):
    gx_ = (zf(x + 100, y) - zf(x - 100, y)) / 200; gy_ = (zf(x, y + 100) - zf(x, y - 100)) / 200
    return math.degrees(math.atan(math.hypot(gx_, gy_)))


ALLR = [(n, p) for n, p, *_ in ROUTES]
MAIN_PTS = [p for n, p, hw, bw, dep, mz, cls in ROUTES if cls in ('main', 'spur')]
FAINT_PTS = [p for n, p, hw, bw, dep, mz, cls in ROUTES if cls == 'faint']


def rdist(x, y, which=None):
    L_ = MAIN_PTS if which == 'main' else FAINT_PTS if which == 'faint' else MAIN_PTS + FAINT_PTS
    return min(float(poly_dist(np.array([x]), np.array([y]), p)[0][0]) for p in L_)


def in_ring(x, y, margin=0):
    if not bool(inside(np.array([x]), np.array([y]), RING)[0]):
        return False
    return float(poly_dist(np.array([x]), np.array([y]), RING, True)[0][0]) >= margin


def prot(x, y):
    return float(protect_w(np.array([x]), np.array([y]))[0])


# ================================================================ 4. open places (no big trunks) and stands
OPEN = {'glade': ((-900, 8750), 700), 'landing': ((620, 2620), 380), 'saddle': ((1450, -6250), 560), 'west_clearing': ((-1950, -100), 560),
        'inlet_head': ((3650, 8000), 320), 'bay_pocket': ((3900, -1050), 360), 'veranda_front': ((950, 1950), 350)}
LOOKS = [((1380, -6100), (760, 600), 420), ((-900, 8650), (760, 900), 0)]       # saddle -> roof (canopy corridor); glade view is over water


def is_open(x, y):
    if any(math.hypot(x - c[0], y - c[1]) < r for c, r in OPEN.values()):
        return True
    return any(r > 0 and float(seg_dist(np.array([x]), np.array([y]), a, b)[0][0]) < r and y < -1400 for a, b, r in LOOKS)


STANDS = [  # (name, centre, radii, rot deg, min spacing): dense enclosing stands that receive trees removed from treads / glades
    ('mother_grove', (900, -2700), (1100, 800), 80, 360), ('east_terrace', (4000, 4800), (700, 1600), 0, 380),
    ('glade_back', (-800, 9700), (1600, 450), 0, 380), ('saddle_back', (1500, -7150), (1300, 380), 5, 380),
    ('valley_east', (2900, -4800), (700, 1000), -10, 400), ('narrows_rib', (3750, -2350), (700, 420), 10, 380),
    ('west_shoulder', (-3600, 2200), (900, 700), 30, 380), ('sw_bank', (-4300, 7400), (900, 1200), -30, 400),
    ('inlet_flank', (3600, 6900), (800, 380), 30, 380), ('nw_knoll', (-2300, -4300), (1100, 800), 40, 420),
]


def in_ell(x, y, g):
    (cx, cy), (rx, ry), rot = g[1], g[2], math.radians(g[3])
    dx, dy = x - cx, y - cy; u_ = dx * math.cos(rot) + dy * math.sin(rot); v_ = -dx * math.sin(rot) + dy * math.cos(rot)
    return (u_ / rx) ** 2 + (v_ / ry) ** 2


# ================================================================ 5. foliage redistribution (counts unchanged)
def role(r):
    n = r['mesh'].split('/')[-1]; ht = r['mesh_bounds'][1][2] * 2
    if any(n.startswith(b) for b in ('SM_PineTree', 'SM_Fir_Tree', 'SM_Oak')) and ht > 800: return 'big'
    if 'Juvenile' in n or 'Young' in n or n.startswith('Pine_08'): return 'young'
    if n.startswith('SM_Bush'): return 'shrub'
    if r['collision'].startswith('QUERY'): return 'hard'
    return 'ground'


CLEAR = {'main': {'big': 230, 'young': 160, 'shrub': 120, 'hard': 240, 'ground': 75}, 'spur': {'big': 170, 'young': 120, 'shrub': 90, 'hard': 200, 'ground': 55},
         'faint': {'big': 120, 'young': 90, 'shrub': 60, 'hard': 160, 'ground': 0}}
BOX = (RX0 + 300, RX1 - 300, RY0 + 300, RY1 - 300)
pop = [(ci, ii, role(r)) for ci, r in enumerate(F) for ii, t in enumerate(r['xf']) if BOX[0] < t[0] < BOX[1] and BOX[2] < t[1] < BOX[3]]
newpos = {}; stats = {'moved': {}, 'regrounded': 0}


def need_move(x, y, ro):
    if prot(x, y) < 0.99:
        return False
    dm = rdist(x, y, 'main'); df = rdist(x, y, 'faint')
    lim_m = CLEAR['main'][ro]; lim_f = CLEAR['faint'][ro]
    if dm < lim_m or df < lim_f:
        return True
    return ro == 'big' and is_open(x, y)


# forest composition (x4+): light, open SHORES and VALLEY FLOOR (ground planes the eye reads), dark dense STANDS on banks and spurs.
# Big trees in a sparse zone are thinned to its minimum spacing; the surplus moves into stand slots (counts unchanged).
HOLLOW_PTS = next(l_[1] for l_ in LANDFORMS if l_[0] == 'hollow')
def sparse_zone(x, y):
    if V in ('x1', 'x2', 'x3'):
        return None
    if zf(x, y) < WATER + 90 and not (x > 2300 and 3500 < y < 6800):
        return ('shore', 900)
    if y < -3600 and float(poly_dist(np.array([x]), np.array([y]), HOLLOW_PTS)[0][0]) < 450:
        return ('valley_floor', 1000)
    return None
_kept = []; THIN = set()
for ci, ii, ro in sorted([p_ for p_ in pop if p_[2] == 'big'], key=lambda k_: rng.random()):
    x, y = F[ci]['xf'][ii][:2]
    if need_move(x, y, ro):
        continue
    z_ = sparse_zone(x, y)
    if z_ and any(math.hypot(x - a, y - b) < z_[1] for a, b, zn in _kept if zn == z_[0]):
        THIN.add((ci, ii)); continue
    _kept.append((x, y, z_[0] if z_ else None))
stats['thinned_big'] = len(THIN)
_need_move0 = need_move
def need_move(x, y, ro, _k=None):
    return _need_move0(x, y, ro)
placed_big = [tuple(F[ci]['xf'][ii][:2]) for ci, ii, ro in pop if ro == 'big' and not need_move(*F[ci]['xf'][ii][:2], ro) and (ci, ii) not in THIN]


def free_slot(x, y, sp, placed, clear=280):
    if not in_ring(x, y, 150) or prot(x, y) < 0.99 or rdist(x, y) < clear or is_open(x, y) or slope_deg(x, y) > 36 or zf(x, y) < WATER + 10:
        return False
    return all(math.hypot(x - px, y - py) >= sp for px, py in placed)


slots = []
for g in STANDS:
    want = int(math.pi * g[2][0] * g[2][1] / (g[4] ** 2) * (0.8 if V in ('x1', 'x2', 'x3') else 1.05)); have = sum(1 for p in placed_big if in_ell(p[0], p[1], g) < 1)
    tries = 0
    while have < want and tries < 3000:
        tries += 1; a = rng.random() * 2 * math.pi; rr = math.sqrt(rng.random()); rot = math.radians(g[3])
        u_, v_ = g[2][0] * rr * math.cos(a), g[2][1] * rr * math.sin(a)
        x, y = g[1][0] + u_ * math.cos(rot) - v_ * math.sin(rot), g[1][1] + u_ * math.sin(rot) + v_ * math.cos(rot)
        if free_slot(x, y, g[4] * (0.8 + 0.5 * rng.random()), placed_big + slots):
            slots.append((x, y)); have += 1
stats['stand_slots'] = len(slots)
# hero oaks: the two oaks farthest from the house views go to the far-shore glade and the saddle
oaks = sorted([(ci, ii) for ci, ii, ro in pop if F[ci]['mesh'].split('/')[-1].startswith('SM_Oak')],
              key=lambda k_: -math.hypot(F[k_[0]]['xf'][k_[1]][0] - 760, F[k_[0]]['xf'][k_[1]][1] - 600))
HERO = {'glade': (-1500, 9250, 30.0), 'saddle': (1950, -6650, 200.0)}
for key_, (hx, hy, hyaw) in zip(oaks[:2], HERO.values()):
    newpos[key_] = (hx, hy, hyaw)
stats['hero_oaks'] = [[F[k_[0]]['mesh'].split('/')[-1], F[k_[0]]['xf'][k_[1]][:2]] for k_ in oaks[:2]]
for ci, ii, ro in pop:
    if (ci, ii) in newpos:
        continue
    x, y = F[ci]['xf'][ii][:2]
    if not need_move(x, y, ro) and (ci, ii) not in THIN:
        continue
    if ro == 'big':
        while slots:
            sx_, sy_ = slots.pop(0)
            if free_slot(sx_, sy_, 300, placed_big):
                newpos[(ci, ii)] = (sx_, sy_, rng.uniform(0, 360)); placed_big.append((sx_, sy_)); break
        else:
            for _ in range(2000):   # outer enclosure band just inside the ring
                a = rng.uniform(0, 2 * math.pi); x2, y2 = x + math.cos(a) * rng.uniform(600, 2500), y + math.sin(a) * rng.uniform(600, 2500)
                if free_slot(x2, y2, 400, placed_big, 400):
                    newpos[(ci, ii)] = (x2, y2, rng.uniform(0, 360)); placed_big.append((x2, y2)); break
    else:
        # small plants: off the tread to 1-3.5 m from its edge on their own side, irregular (no hedge line)
        best = None
        for p_ in MAIN_PTS + FAINT_PTS:
            dd, _ = poly_dist(np.array([x]), np.array([y]), p_)
            if best is None or dd[0] < best[0]:
                best = (float(dd[0]), p_)
        for _ in range(60):
            a = rng.uniform(0, 2 * math.pi); r_ = rng.uniform(150, 450)
            x2, y2 = x + math.cos(a) * r_, y + math.sin(a) * r_
            if prot(x2, y2) > 0.99 and not need_move(x2, y2, ro) and zf(x2, y2) > WATER + 5 and (ro != 'hard' or rdist(x2, y2) > 300):
                newpos[(ci, ii)] = (x2, y2, None if ro != 'hard' else rng.uniform(0, 360)); break
for ro in ('big', 'young', 'shrub', 'hard', 'ground'):
    stats['moved'][ro] = sum(1 for k_ in newpos if role(F[k_[0]]) == ro)
stats['unused_stand_slots'] = len(slots)

out_comps = []
for ci, r in enumerate(F):
    xf = [list(t) for t in r['xf']]; changed = False
    for ii, t in enumerate(xf):
        x, y, z = t[0], t[1], t[2]
        if not (RX0 < x < RX1 and RY0 < y < RY1) and (ci, ii) not in newpos:
            continue
        emb = z - zb(Z0, x, y, OX, OY)
        if (ci, ii) in newpos:
            nx, ny, yaw = newpos[(ci, ii)]
            t[0], t[1] = round(nx, 1), round(ny, 1)
            if yaw is not None: t[4] = round(yaw, 2)
            t[2] = round(zf(nx, ny) + min(emb, 30.0), 1); changed = True
        else:
            nz = zf(x, y) + emb
            if abs(nz - z) > 0.5:
                t[2] = round(nz, 1); changed = True; stats['regrounded'] += 1
    if changed:
        out_comps.append({'mesh': r['mesh'], 'cull': r['cull'], 'n': len(xf), 'xf_after': xf})

# ================================================================ 6. structural spawns (cliff rock, deadfall, logs, wade limit)
MB = {  # mesh: (extent xyz, origin xyz) from probe_assets.json (cm, unscaled)
    'CliffRock01': ([309, 94, 193], [15, 18, 142]), 'CliffRock02': ([282, 86, 190], [16, 32, 144]), 'CliffRockCurve01': ([262, 150, 193], [21, 17, 142]),
    'CliffRockCurve02': ([218, 123, 191], [-2, 36, 143]), 'PineCliff02': ([313, 111, 155], [-3, -26, 139]), 'PineCliff03': ([303, 83, 147], [10, 1, 143]),
    'ForestEmbankment01': ([474, 197, 141], [-1, 71, 110]), 'FallenTree01': ([454, 167, 100], [320, 11, 66]),
    'PineDeadTrunk01': ([312, 59, 36], [13, 8, 22]), 'PineDeadTrunk02': ([218, 42, 35], [5, 1, 26]), 'PineDeadTrunk03': ([239, 34, 37], [24, 4, 28]),
    'PineGroundRock01': ([245, 183, 77], [5, -8, 55]), 'PineGroundRock05': ([252, 176, 81], [13, -3, 61])}
PATHS = {'CliffRock01': '/Game/PineForestPack/Meshes/Cliffs/SM_CliffRock01', 'CliffRock02': '/Game/PineForestPack/Meshes/Cliffs/SM_CliffRock02',
         'CliffRockCurve01': '/Game/PineForestPack/Meshes/Cliffs/SM_CliffRockCurve01', 'CliffRockCurve02': '/Game/PineForestPack/Meshes/Cliffs/SM_CliffRockCurve02',
         'PineCliff02': '/Game/PineForestPack/Meshes/Cliffs/SM_PineCliff02', 'PineCliff03': '/Game/PineForestPack/Meshes/Cliffs/SM_PineCliff03',
         'ForestEmbankment01': '/Game/PineForestPack/Meshes/Cliffs/SM_ForestEmbankment01', 'FallenTree01': '/Game/PineForestPack/Meshes/TerrainPatches/SM_FallenTree01',
         'PineDeadTrunk01': '/Game/PineForestPack/Meshes/TerrainPatches/SM_PineDeadTrunk01', 'PineDeadTrunk02': '/Game/PineForestPack/Meshes/TerrainPatches/SM_PineDeadTrunk02',
         'PineDeadTrunk03': '/Game/PineForestPack/Meshes/TerrainPatches/SM_PineDeadTrunk03', 'PineGroundRock01': '/Game/PineForestPack/Meshes/Cliffs/SM_PineGroundRock01', 'PineGroundRock05': '/Game/PineForestPack/Meshes/Cliffs/SM_PineGroundRock05'}
SPAWN = []
# measured bounds of the landmark meshes (probe_assets.json, editor measure job); landmarks are placed only when measured
try:
    _PA = json.load(open(os.path.join(os.path.dirname(os.path.normpath(OUTD)), 'recon', 'probe_assets.json')))['meshes']
except Exception:
    _PA = {}
for _p, _v in _PA.items():
    if _v and _p.split('/')[-1].replace('SM_', '') not in MB:
        MB[_p.split('/')[-1].replace('SM_', '')] = (_v['ext'], _v['org']); PATHS[_p.split('/')[-1].replace('SM_', '')] = _p


def spawn(kind, mesh, x, y, yaw, sc, zoff_frac, label, block=True, pitch=0.0, roll=0.0, z=None):
    (ex, ey, ez), (ox, oy, oz) = MB[mesh]
    c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    fx_, fy_ = x + (ox * c - oy * s) * sc[0], y + (ox * s + oy * c) * sc[1]
    gz = zf(fx_, fy_) if z is None else z
    pz = gz - (oz - ez) * sc[2] - zoff_frac * 2 * ez * sc[2]          # bottom of the bounds sinks zoff_frac of the height
    SPAWN.append({'kind': kind, 'mesh': PATHS[mesh] or mesh, 'label': label, 'x': round(x, 1), 'y': round(y, 1), 'z': round(pz, 1), 'yaw': round(yaw, 1),
                  'pitch': round(pitch, 1), 'roll': round(roll, 1), 'scale': [round(v, 3) for v in sc], 'fx': round(fx_, 1), 'fy': round(fy_, 1),
                  'hx': round(ex * sc[0], 1), 'hy': round(ey * sc[1], 1), 'top_cm': round(pz + (oz + ez) * sc[2] - gz, 1), 'block': block})


def tread_clear(min_cm=250):
    # the last spawn must not reach a main / spur tread (its oriented footprint's far end included); otherwise drop it
    lx = SPAWN[-1]; c_, s_ = math.cos(math.radians(lx['yaw'])), math.sin(math.radians(lx['yaw']))
    for a_ in (-1.0, -0.5, 0.0, 0.5, 1.0):
        px_, py_ = lx['fx'] + a_ * lx['hx'] * c_, lx['fy'] + a_ * lx['hx'] * s_
        if rdist(px_, py_, 'main') < min_cm + lx['hy'] * 0.7:
            SPAWN.pop(); stats['dropped_on_tread'] = stats.get('dropped_on_tread', 0) + 1; return False
    return True


def ring_point(s):
    return at(RING + [RING[0]], s, cum)


def ring_normal(s):
    a = ring_point(max(s - 50, 0)); b = ring_point(min(s + 50, cum[-1])); tx, ty = b[0] - a[0], b[1] - a[1]; L = math.hypot(tx, ty) or 1
    nx, ny = ty / L, -tx / L                                   # candidate normal; flip so it points OUTSIDE
    px, py = ring_point(s)
    if bool(inside(np.array([px + nx * 300]), np.array([py + ny * 300]), RING)[0]):
        nx, ny = -nx, -ny
    return nx, ny, math.degrees(math.atan2(ty, tx))


CLIFFS = ['CliffRock01', 'CliffRock02', 'CliffRockCurve01', 'CliffRockCurve02', 'PineCliff02', 'PineCliff03']
# rock-clad ring sections (arc metres along the ring from vertex 0), chosen where a route or destination sees the bank
ring_xy = lambda k_: RING[k_]
def arc_of(xy):
    d, a = poly_dist(np.array([xy[0]]), np.array([xy[1]]), RING, True); return float(a[0]) * cum[-1]
ROCK_SECTIONS = []
for c_, half, sp in (((-400, 9750), 1500, 780) if not X8 else ((-900, 9700), 1800, 620), ((1500, -7800), 1300, 820), ((3120, 4300), 1900, 700), ((4650, 7900), 1100, 760),
                      ((-2600, -4900), 1300, 820), ((-5250, 2500), 900, 900), ((4500, -600), 700, 800)):
    a0 = arc_of(c_); ROCK_SECTIONS.append((a0 - half, a0 + half, sp))
nrock = 0
for a0, a1, sp in ROCK_SECTIONS:
    s = a0
    while s < a1:
        ss_ = s % cum[-1]; px, py = ring_point(ss_); nx, ny, tyaw = ring_normal(ss_)
        m = rng.choice(CLIFFS); scl = rng.uniform(1.45, 2.0)
        sc = (scl, scl * rng.uniform(0.95, 1.25), scl * rng.uniform(0.9, 1.15))
        yaw = tyaw + rng.uniform(-14, 14) + (180 if rng.random() < 0.5 else 0)
        # stand on the inside foot of the bank, half its thickness into the face
        spawn('ring_rock', m, px + nx * MB[m][0][1] * sc[1] * 0.35, py + ny * MB[m][0][1] * sc[1] * 0.35, yaw, sc, 0.22, 'XR2_RingRock_%02d' % nrock,
              z=zf(px - nx * 80, py - ny * 80))
        nrock += 1; s += sp * rng.uniform(0.85, 1.1)
# interior line W1: rock band along its foot (low side), deadfall in the gaps
for nm, pts, hh, side in INNER:
    cumi = [0.0]
    for a, b in zip(pts, pts[1:]):
        cumi.append(cumi[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    s = 250.0; k_ = 0
    while s < cumi[-1] - 100:
        px, py = at(pts, s, cumi); qx, qy = at(pts, min(s + 60, cumi[-1]), cumi); tx, ty = qx - px, qy - py; L_ = math.hypot(tx, ty) or 1
        lx_, ly_ = -ty / L_ * side, tx / L_ * side                        # unit normal toward the RAISED side
        if nm.startswith('W0'):
            if k_ % 2 == 0:
                spawn('inner_bank', 'ForestEmbankment01', px - lx_ * 40, py - ly_ * 40, math.degrees(math.atan2(ty, tx)) + (180 if side > 0 else 0) + rng.uniform(-8, 8),
                      (1.15, 1.1, 1.1), 0.25, 'XR2_W0_Bank_%02d' % k_, z=zf(px - lx_ * 150, py - ly_ * 150))
            m = rng.choice(['FallenTree01', 'PineDeadTrunk01']); scl = rng.uniform(1.3, 1.5)
            spawn('inner_deadfall', m, px + lx_ * 220, py + ly_ * 220, math.degrees(math.atan2(ty, tx)) + rng.uniform(-20, 20), (scl, scl, scl), 0.15, 'XR2_W0_Deadfall_%02d' % k_)
            tread_clear()
        elif k_ % 3 != 2:
            m = rng.choice(CLIFFS); scl = rng.uniform(1.4, 1.8); sc = (scl, scl * rng.uniform(1.0, 1.2), scl)
            spawn('inner_rock', m, px + lx_ * 60, py + ly_ * 60, math.degrees(math.atan2(ty, tx)) + rng.uniform(-12, 12) + (180 if rng.random() < .5 else 0), sc, 0.22,
                  'XR2_%s_Rock_%02d' % (nm[:2], k_), z=zf(px - lx_ * 120, py - ly_ * 120))
        else:
            m = rng.choice(['FallenTree01', 'PineDeadTrunk01']); scl = rng.uniform(1.35, 1.6)
            spawn('inner_deadfall', m, px - lx_ * 80, py - ly_ * 80, math.degrees(math.atan2(ty, tx)) + rng.uniform(-25, 25), (scl, scl, scl), 0.15, 'XR2_%s_Deadfall_%02d' % (nm[:2], k_))
            tread_clear()
        k_ += 1; s += rng.uniform(620, 760)
# deadfall on the bank top where the ring is near a route and has no rock
ndf = 0; s = 0.0
while s < cum[-1]:
    px, py = ring_point(s)
    near = rdist(px, py) < 2600
    clad = any(a0 <= s <= a1 or a0 <= s + cum[-1] <= a1 for a0, a1, _ in ROCK_SECTIONS)
    if near and not clad:
        nx, ny, tyaw = ring_normal(s)
        m = 'FallenTree01' if rng.random() < 0.35 else rng.choice(['PineDeadTrunk01', 'PineDeadTrunk03'])
        scl = rng.uniform(1.2, 1.6)
        yaw = tyaw + rng.uniform(-35, 35) + (180 if rng.random() < 0.5 else 0)
        spawn('ring_deadfall', m, px + nx * 120, py + ny * 120, yaw, (scl, scl, scl), 0.18, 'XR2_RingDeadfall_%02d' % ndf)
        if tread_clear(): ndf += 1
    s += rng.uniform(780, 1050)
# interior barriers --------------------------------------------------------------
# backyard north windthrow: the yard becomes a room whose exit is the gate (east)
for k_, (x, y, yaw) in enumerate([] if V not in ('x1', 'x2', 'x3', 'x4') else [(-250, -1450, 12), (450, -1700, -8), (1150, -1500, 20), (1850, -1650, -15), (2350, -1450, 35), (-450, -900, 95),
                                  (800, -2050, 160), (1600, -2100, 5)]):
    m = 'FallenTree01' if k_ % 3 == 0 else 'PineDeadTrunk01'
    scl = 1.35 + 0.1 * (k_ % 3)
    spawn('yard_windthrow', m, x, y, yaw + rng.uniform(-6, 6), (scl, scl, scl), 0.15, 'XR2_YardWindthrow_%02d' % k_)
# r6: spur toes become rock outcrops; the narrows gets its right-hand rock wall; the saddle a rock seat under the hero oak
for k_, (m, x, y, yaw, scl) in enumerate([('CliffRockCurve01', 3500, -2280, 200, 1.7), ('CliffRock02', 3720, -2650, 185, 1.6),
                                         ('PineCliff02', 3420, 120, 160, 1.6), ('CliffRock01', 3650, 520, 175, 1.5),
                                         ('CliffRockCurve02', 4300, 8350, 230, 1.8), ('PineCliff03', 4550, 8000, 250, 1.7)]):
    spawn('r6_outcrop', m, x, y, yaw, (scl, scl, scl), 0.25, 'XR2_Outcrop_%02d' % k_)
# off-route deadwood as WINDTHROW PATCHES (storm-felled groups lying roughly with the wind), placed where they cut a shortcut or
# give an off-route area a reason to be slow; never on a tread. A few single logs give texture elsewhere.
WINDTHROW = [  # name, centre, radius cm, n, fall yaw (deg, Unreal), why
    ('west_woods', (-2600, -2300), 700, 5, 130, 'west woods -> climb shortcut'), ('nw_house', (-900, -2000), 600, 4, 120, 'house west -> house spur'),
    ('valley_west', (200, -4100), 700, 5, 140, 'west woods -> climb shortcut'), ('valley_east', (3100, -4600), 600, 4, 160, 'east ridge foot'),
    ('west_shoulder', (-4000, 1300), 650, 4, 110, 'west loop -> west woods shortcut'), ('sw_bank', (-4400, 7100), 600, 4, 80, 'SW corner'),
    ('glade_east', (1400, 8900), 500, 3, 200, 'glade -> SE slope'), ('hollow_low', (2800, -3700), 450, 3, 120, 'hollow side'),
    ('house_spur_N', (600, -3500), 650, 4, 100, 'backyard -> valley shortcut (behind the yard windthrow)')]
nlog = 0; logs = []
for wn, (cx, cy), rad, n, fyaw, why in WINDTHROW:
    got = 0; tries = 0
    while got < n and tries < 600:
        tries += 1; a = rng.uniform(0, 2 * math.pi); r_ = rad * math.sqrt(rng.random()); x, y = cx + math.cos(a) * r_, cy + math.sin(a) * r_
        if not in_ring(x, y, 300) or prot(x, y) < 0.99 or zf(x, y) < WATER + 20 or is_open(x, y) or slope_deg(x, y) > 32:
            continue
        if rdist(x, y, 'main') < 400 or rdist(x, y, 'faint') < 260 or any(math.hypot(x - a_, y - b_) < 240 for a_, b_ in logs):
            continue
        m = rng.choice(['PineDeadTrunk01', 'PineDeadTrunk01', 'PineDeadTrunk03', 'FallenTree01'])
        scl = rng.uniform(1.2, 1.6)
        spawn('windthrow', m, x, y, fyaw + rng.uniform(-22, 22), (scl, scl, scl), 0.15, 'XR2_Windthrow_%s_%d' % (wn, got))
        lx = SPAWN[-1]
        if rdist(lx['fx'], lx['fy'], 'main') < 300 + lx['hx'] * 0.6 or rdist(lx['fx'], lx['fy'], 'faint') < 150 + lx['hx'] * 0.6:
            SPAWN.pop(); continue
        logs.append((x, y)); got += 1; nlog += 1
tries = 0; single = 0
while tries < 6000 and single < 14:
    tries += 1
    x, y = rng.uniform(-5200, 5000), rng.uniform(-7600, 9600)
    if not in_ring(x, y, 350) or prot(x, y) < 0.99 or zf(x, y) < WATER + 20 or is_open(x, y) or slope_deg(x, y) > 30:
        continue
    if rdist(x, y, 'main') < 450 or rdist(x, y, 'faint') < 300 or any(math.hypot(x - a, y - b) < 900 for a, b in logs):
        continue
    m = rng.choice(['PineDeadTrunk02', 'PineDeadTrunk03', 'PineDeadTrunk01'])
    scl = rng.uniform(1.0, 1.4)
    spawn('single_log', m, x, y, rng.uniform(0, 360), (scl, scl, scl), 0.15, 'XR2_Log_%02d' % single)
    lx = SPAWN[-1]
    if rdist(lx['fx'], lx['fy'], 'main') < 300 + lx['hx'] * 0.6:
        SPAWN.pop(); continue
    logs.append((x, y)); single += 1
# landmarks: one memorable object per place, each a reason to go there and a cue seen from the previous decision point
LANDMARKS = [  # key, mesh, x, y, yaw, scale, sink frac, z mode ('ground' | 'water' | 'shore'), block
    ('boat_landing', 'Boat_01', 330, 2980, 105, 1.0, 0.12, 'shore', True),          # old rowboat pulled up at the landing: the first cue from the veranda
    ('glade_seat', 'PineGroundRock01', -1250, 9050, 20, 0.75, 0.4, 'ground', True),  # sitting rock under the hero oak, facing the house across the water
    ('chopping_block', 'Wood_Cutting_Set_12', -1850, -50, 30, 1.2, 0.0, 'ground', True),  # old felling place
    ('saddle_seat', 'PineGroundRock01', 1200, -6550, 70, 0.9, 0.35, 'ground', True),
]
for key_, m, x, y, yaw, scl, sink, zm, blk in (LANDMARKS if V not in ('x1', 'x2', 'x3', 'x4', 'x5', 'x6') else []):
    if m not in MB:
        stats.setdefault('landmark_missing', []).append(m); continue
    if zm == 'water':
        spawn('landmark', m, x, y, yaw, (scl, scl, scl), 0.0, 'XR2_Landmark_' + key_, block=blk, z=WATER - 8)
    elif zm == 'shore':
        spawn('landmark', m, x, y, yaw, (scl, scl, scl), sink, 'XR2_Landmark_' + key_, block=blk, z=max(zf(x, y), WATER - 25))
    else:
        spawn('landmark', m, x, y, yaw, (scl, scl, scl), sink, 'XR2_Landmark_' + key_, block=blk)
# path soil decals (dress stage only): worn soil along the treads, broken and irregular (no continuous brown strip)
DECAL_ROUTES = {'A_front': (140, [300, 200]), 'A': (170, [430, 260]), 'B': (170, [400, 240]), 'connect': (190, [330, 200]), 'descent': (190, [330, 200]),
                'west_loop': (420, [260, 160]), 'spur_inlet': (300, [300, 180]), 'spur_bay': (300, [300, 180]), 'spur_west': (300, [300, 180])}
for nm, (step, size) in (DECAL_ROUTES.items() if V not in ('x1', 'x2', 'x3', 'x4', 'x5', 'x6') else []):
    pts = RINFO[nm]['pts']; cum_ = [0.0]
    for a, b in zip(pts, pts[1:]):
        cum_.append(cum_[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    s_ = rng.uniform(0, step * 0.5); k_ = 0
    while s_ < cum_[-1]:
        x, y = at(pts, s_, cum_); x2, y2 = at(pts, min(s_ + 40, cum_[-1]), cum_)
        if prot(x, y) > 0.9 and (nm not in ('west_loop',) or rng.random() < 0.8):
            yaw = math.degrees(math.atan2(y2 - y, x2 - x)) + rng.uniform(-10, 10)
            off = rng.uniform(-25, 25); nx_, ny_ = -(y2 - y), (x2 - x); nl = math.hypot(nx_, ny_) or 1
            sc_ = rng.uniform(0.85, 1.15)
            SPAWN.append({'kind': 'decal', 'mesh': '/Game/Modular_Rural_Cabin/Materials/Decals/Forest_Ground', 'label': 'XR2_Decal_%s_%03d' % (nm, k_),
                          'x': round(x + nx_ / nl * off, 1), 'y': round(y + ny_ / nl * off, 1), 'z': round(zf(x, y), 1), 'yaw': round(yaw, 1), 'pitch': 0.0, 'roll': 0.0,
                          'scale': [1, 1, 1], 'size': [round(size[0] * sc_), round(size[1] * sc_)], 'fx': x, 'fy': y, 'hx': 0, 'hy': 0, 'top_cm': 0, 'block': False, 'stage': 'dress',
                          'nrm': [round(-(zf(x + 60, y) - zf(x - 60, y)) / 120, 4), round(-(zf(x, y + 60) - zf(x, y - 60)) / 120, 4), 1.0]})
            k_ += 1
        s_ += step * rng.uniform(0.8, 1.2)
# dress-stage foliage (x8 review): the far-shore glade's back read as a bare slope at player height -> a fir/pine stand on the bank
# with a fern skirt at its foot (separate dress RNG so the build spawns above stay identical)
if V not in ('x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7'):
    drng = random.Random(77)
    DRESS = [('/Game/Fishermans_Cabin/Meshes/Foliage/Tree/SM_Fir_Tree_03', (-1650, 9350), 1.05), ('/Game/Fishermans_Cabin/Meshes/Foliage/Tree/SM_Fir_Tree_03', (-1150, 9550), 1.15),
             ('/Game/PineForestPack/Meshes/Trees/SM_PineTree01', (-700, 9450), 0.95), ('/Game/Fishermans_Cabin/Meshes/Foliage/Tree/SM_Fir_Tree_03', (-250, 9300), 1.0),
             ('/Game/PineForestPack/Meshes/Trees/SM_PineTree01', (-2100, 9500), 1.0), ('/Game/Fishermans_Cabin/Meshes/Foliage/Tree/SM_Fir_Tree_03', (300, 9500), 0.9)]
    for k_, (m, (x, y), sc_) in enumerate(DRESS):
        SPAWN.append({'kind': 'dress_tree', 'mesh': m, 'label': 'XR2_DressTree_%02d' % k_, 'x': x, 'y': y, 'z': round(zf(x, y) - 15, 1), 'yaw': drng.uniform(0, 360),
                      'pitch': 0.0, 'roll': 0.0, 'scale': [sc_, sc_, sc_], 'fx': x, 'fy': y, 'hx': 30.0, 'hy': 30.0, 'top_cm': 999, 'block': True, 'stage': 'dress'})
    for k_ in range(14):
        x, y = drng.uniform(-2300, 500), drng.uniform(9050, 9300)
        if math.hypot(x + 900, y - 8750) < 450: continue
        m = drng.choice(['/Game/PineForestPack/Meshes/Plants/SM_FernLong01', '/Game/Calysto/World/Vegetation/Meshes/SM_Young_Black_Spruce_02', '/Game/PineForestPack/Meshes/Plants/SM_FernLong01'])
        sc_ = drng.uniform(0.9, 1.3)
        SPAWN.append({'kind': 'dress_soft', 'mesh': m, 'label': 'XR2_DressSoft_%02d' % k_, 'x': round(x), 'y': round(y), 'z': round(zf(x, y) - 5, 1), 'yaw': drng.uniform(0, 360),
                      'pitch': 0.0, 'roll': 0.0, 'scale': [sc_, sc_, sc_], 'fx': x, 'fy': y, 'hx': 0, 'hy': 0, 'top_cm': 0, 'block': False, 'stage': 'dress'})
# wade limit: invisible pawn-only wall along the 45 cm water depth contour (no walking across the pond floor)
cs = []
for jj in range(j0 + 1, j1 - 1, 2):
    for ii in range(i0 + 1, i1 - 1, 2):
        z_ = Zf[jj, ii]
        if (z_ < WATER - 45) and min(Zf[jj - 2, ii], Zf[jj + 2, ii], Zf[jj, ii - 2], Zf[jj, ii + 2]) < WATER - 45 <= max(Zf[jj - 2, ii], Zf[jj + 2, ii], Zf[jj, ii - 2], Zf[jj, ii + 2]):
            cs.append((OX + ii * 100.0, OY + jj * 100.0))
WADE = []
for x, y in cs:
    if all(math.hypot(x - a, y - b) > 180 for a, b in WADE):
        WADE.append((x, y))
for k_, (x, y) in enumerate(WADE):
    SPAWN.append({'kind': 'wade_limit', 'mesh': '/Engine/BasicShapes/Cube', 'label': 'XR2_WadeLimit_%03d' % k_, 'x': x, 'y': y, 'z': WATER - 60, 'yaw': 0.0,
                  'pitch': 0.0, 'roll': 0.0, 'scale': [2.2, 2.2, 3.0], 'fx': x, 'fy': y, 'hx': 110.0, 'hy': 110.0, 'top_cm': 240, 'block': True,
                  'invisible': True, 'profile': 'InvisibleWall'})
stats['spawn'] = {k_: sum(1 for s_ in SPAWN if s_['kind'] == k_) for k_ in sorted(set(s_['kind'] for s_ in SPAWN))}

# ================================================================ 7. write
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
for name, info in RINFO.items():
    pts = info['pts']; cum_ = [0.0]
    for a, b in zip(pts, pts[1:]):
        cum_.append(cum_[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    prof = [zf(*at(pts, s, cum_)) for s in np.arange(0, cum_[-1] + 1, 100.0)]
    info['profile_m'] = [round(p / 100, 2) for p in prof]
    info['max_grade_deg'] = round(max(abs(math.degrees(math.atan((b - a) / 100.0))) for a, b in zip(prof, prof[1:])), 1)
    info['max_cross_slope_deg'] = round(max(slope_deg(*at(pts, s, cum_)) for s in np.arange(0, cum_[-1] + 1, 100.0)), 1)
stats.update({'delta_cm_min_max': [round(float(DELTA.min()), 1), round(float(DELTA.max()), 1)], 'changed_samples': int((np.abs(Zf - Z0) > 1.0).sum()),
              'comps_changed': len(out_comps), 'ring_len_m': round(cum[-1] / 100, 1)})
json.dump({'variant': V, 'file': 'height_%s.png' % V, 'samples': samp, 'routes': RINFO, 'ring': RING, 'ring_h': RING_H, 'landforms': LANDFORMS,
           'protect': PROTECT, 'stands': STANDS, 'windthrow': WINDTHROW, 'flats': FLATS, 'inner': INNER, 'open': {k_: [list(c), r] for k_, (c, r) in OPEN.items()}, 'climb_r6': CLIMB_R6, 'stats': stats},
          open(os.path.join(OUTD, 'plan_%s.json' % V), 'w'), indent=1, default=str)
json.dump(out_comps, open(os.path.join(OUTD, 'foliage_%s.json' % V), 'w'))
chg = {(c_['mesh'], tuple(c_['cull'])): c_['xf_after'] for c_ in out_comps}
json.dump([dict(r, xf=chg.get((r['mesh'], tuple(r['cull'])), r['xf'])) for r in F], open(os.path.join(OUTD, 'foliage_full_%s.json' % V), 'w'))
json.dump(SPAWN, open(os.path.join(OUTD, 'spawn_%s.json' % V), 'w'), indent=0)
COL = {'A': [0.1, 0.55, 0.95], 'A_front': [0.1, 0.55, 0.95], 'B': [0.95, 0.2, 0.6], 'connect': [0.95, 0.75, 0.1], 'descent': [0.95, 0.75, 0.1],
       'west_loop': [0.55, 0.55, 0.9], 'spur_inlet': [0.2, 0.75, 0.4], 'spur_bay': [0.2, 0.75, 0.4], 'spur_west': [0.2, 0.75, 0.4]}
ov = {'polys': [{'pts': RING + [RING[0]], 'rgb': [0.75, 0.1, 0.1], 'w': 2}] + [{'pts': l_[1], 'rgb': [0.75, 0.1, 0.1], 'w': 2} for l_ in INNER] +
               [{'pts': info['pts'], 'rgb': COL[n], 'w': 3 if info['class'] == 'main' else 2} for n, info in RINFO.items()],
      'discs': [{'xy': c, 'r': r, 'rgb': [1, 0.95, 0.4], 'a': 0.9, 'ring': 2.0} for c, r in OPEN.values()]}
for g in STANDS:
    rot = math.radians(g[3]); pts = []
    for a in np.linspace(0, 2 * math.pi, 40):
        u_, v_ = g[2][0] * math.cos(a), g[2][1] * math.sin(a); pts.append((g[1][0] + u_ * math.cos(rot) - v_ * math.sin(rot), g[1][1] + u_ * math.sin(rot) + v_ * math.cos(rot)))
    ov['polys'].append({'pts': pts, 'rgb': [0.1, 0.6, 0.2], 'w': 1})
json.dump(ov, open(os.path.join(OUTD, 'overlay_%s.json' % V), 'w'))
print('DESIGN', V, json.dumps(stats), {n: (i['len_m'], i['max_grade_deg'], i['max_cross_slope_deg']) for n, i in RINFO.items()})
