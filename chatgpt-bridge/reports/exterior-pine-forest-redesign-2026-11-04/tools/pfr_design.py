"""pfr_design.py (offline, Blender Python + numpy): the Pine Forest redesign of the first gameplay area.
usage: pfr_design.py <variant>   -> Saved/Codex/PineForestRedesign_20261104/design/<variant>/{plan,foliage,newfol,spawn,mats,look}_<v>.json + preview

Base (proven, unsaved until now): XR2 x9 terrain + circulation (world ring, routes A/B, stands, wade limit) and the XR4 i5 slice identity
(bedrock ledge, glade terrace, hero masses). This design converts that world to the Pine Forest Pack identity:
  1 canopy family: every Fishermans fir -> PFP mid pine of the same height band; black spruce young -> PFP juveniles / broadleaf saplings
    (35 % kept as dark accents); hero PineTree04 at the frame edges of the key views (foliage instances, never actors)
  2 midstory: Fishermans bushes -> PFP bush family (height matched)
  3 floor: red-purple broadleaf litter -> needle clumps; moss-leaf carpet pockets (glade terrace, rock feet, saddle, shaded route bands,
    inlet floor); needle litter, cones, fallen branches, mushrooms at their causes; PFP ground patches on flat tread edges only
  4 rocks: PFP cliff family for the ledge (replaces the Environment_Set blocks), moss-topped PineGroundRock boulder groups at the shore,
    the shelf foot and route bends; one project-owned cliff MI (cooler, mossier) on every ring / ledge / outcrop block
  5 house front (refuge moment): two framing hero pines 6 m off the facade, flat stepping stones on the front footpath, quiet needle floor,
    moss on the shaded west side, foundation-corner ferns only
  6 glade: XR4 terrace kept, stone arc pulled inside the terrace (r 4.2 m), moss carpet instead of bare soil
  7 water: owned pond MI values of the XR5 material trial (dark tea water, micro ripple)
  8 light: PF morning look derived from the pack's showcase recipe, applied on the existing owners (measured against XR5 FINAL v2)
Landscape paint layers (PFP material) come from paint_masks.py <variant>."""
import sys, os, json, math, random, zlib, struct, collections
import numpy as np
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, 'Tools/ExteriorWorld_XR2_20261031'); sys.path.insert(0, 'Tools/PineForestRedesign_20261104')
import xr2_layout as LY, pfr_palette as PL
V = sys.argv[1] if len(sys.argv) > 1 else 'p1'
OUT = 'Saved/Codex/PineForestRedesign_20261104/design/%s' % V; os.makedirs(OUT, exist_ok=True)
X2 = 'Saved/Codex/ExteriorWorld_XR2_20261031/design'; D3 = 'Saved/Codex/ExteriorIdentity_XR3_20261031/design'
OX, OY, N = -50040.0, -50225.0, 1017; WATER = -100.0
rng = random.Random(11041)
FT_DIR = '/Game/GraceRanger/Environment/Exterior20260921/Foliage/'; MAT_DIR = '/Game/GraceRanger/Environment/Exterior20260921/Materials/'
P = {'PF': '/Game/PineForestPack/Meshes/', 'C': '/Game/Calysto/World/Vegetation/Meshes/', 'E': '/Game/Environment_Set/Environment/Rocks/Models/'}

# ================================================================ terrain (x9 = x8 + XR4 ledge berm + glade terrace)
H = np.fromfile(X2 + '/height_x9.u16', dtype='<u2').reshape(N, N); Z = (H.astype(np.float64) - 32768.0) * 100.0 / 128.0
plan9 = json.load(open(X2 + '/plan_x9.json'))


def zf(x, y):
    fx, fy = (x - OX) / 100.0, (y - OY) / 100.0; ix, iy = int(math.floor(fx)), int(math.floor(fy)); ax, ay = fx - ix, fy - iy
    return Z[iy, ix] * (1 - ax) * (1 - ay) + Z[iy, ix + 1] * ax * (1 - ay) + Z[iy + 1, ix] * (1 - ax) * ay + Z[iy + 1, ix + 1] * ax * ay


def slope_deg(x, y):
    gx = (zf(x + 100, y) - zf(x - 100, y)) / 200; gy = (zf(x, y + 100) - zf(x, y - 100)) / 200; return math.degrees(math.atan(math.hypot(gx, gy)))


def normal(x, y):
    gx = (zf(x + 60, y) - zf(x - 60, y)) / 120; gy = (zf(x, y + 60) - zf(x, y - 60)) / 120; n = np.array([-gx, -gy, 1.0]); return n / np.linalg.norm(n)


def pitch_roll_for(x, y, yaw):
    """pitch / roll (deg) that lay a flat mesh on the local ground for a given yaw (Unreal: pitch about Y, roll about X of the rotated frame)"""
    n = normal(x, y); c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    fwd = np.array([c, s, 0.0]); right = np.array([-s, c, 0.0])
    return round(-math.degrees(math.asin(max(-1, min(1, float(np.dot(n, fwd)))))), 2), round(math.degrees(math.asin(max(-1, min(1, float(np.dot(n, right)))))), 2)


def ring_inside(x, y):
    poly = plan9['ring']; c = False
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / ((by - ay) or 1e-9) + ax: c = not c
    return c


def dpoly(x, y, pts):
    b = 1e9
    for a, c in zip(pts, pts[1:]):
        vx, vy = c[0] - a[0], c[1] - a[1]; t = max(0, min(1, ((x - a[0]) * vx + (y - a[1]) * vy) / (vx * vx + vy * vy))); b = min(b, math.hypot(a[0] + t * vx - x, a[1] + t * vy - y))
    return b


MAIN = [LY.ROUTE_A, LY.ROUTE_B, LY.CONNECT, LY.DESCENT]; SPURS = [LY.SPUR_INLET, LY.SPUR_BAY, LY.SPUR_WEST]; FAINT = [LY.WEST_LOOP]


def rdist(x, y):
    return min(dpoly(x, y, p) for p in MAIN + SPURS)


def rdist_all(x, y):
    return min(rdist(x, y), dpoly(x, y, LY.WEST_LOOP))


HOUSE = (-350, 1870, -350, 1490)      # protected house box (+3.5 m)


def in_house(x, y, pad=0):
    return HOUSE[0] - pad < x < HOUSE[1] + pad and HOUSE[2] - pad < y < HOUSE[3] + pad


# ================================================================ base foliage state = x9 lists + i5 edits
F9 = json.load(open(X2 + '/foliage_full_x9.json')); I5 = json.load(open(D3 + '/id_i5.json'))
i5f = {(c['mesh'], tuple(c['cull'])): c['xf_after'] for c in I5['foliage']}
base = {}
for rec in F9:
    key = (rec['mesh'], tuple(rec['cull'])); base[key] = [list(t) for t in i5f.get(key, rec['xf'])]
short = lambda m: m.split('/')[-1]
stats = collections.OrderedDict(); out_fol = {}; newfol = collections.defaultdict(list)


def add_new(ft, x, y, z, yaw, sc, pitch=0.0, roll=0.0):
    newfol[ft].append([round(x, 1), round(y, 1), round(z, 1), round(pitch, 2), round(yaw, 2), round(roll, 2), round(sc, 3), round(sc, 3), round(sc, 3)])


def pick(table):
    mesh, lo, hi = rng.choice(table); return mesh, rng.uniform(lo, hi)


FT_OF_MESH = {v[0]: k for k, v in PL.NEW_TYPES.items()}
# big-tree register (for spacing / cone / needle causes): existing pines + converted firs + heroes
BIG = []
for key, xf in base.items():
    n = short(key[0])
    if n.startswith('SM_PineTree') or n.startswith('SM_Oak'):
        for t in xf: BIG.append((t[0], t[1], t[6] * PL.PAL[n]['h'] if n in PL.PAL else 2500, n))

# ---- 1. fir -> pine family (same positions, height band kept, pine pivot at the base)
# p2: in the house-front zone (porch -> landing -> front footpath) the low-branched mid pines blocked the house views (p1 P0_house_back):
# there the firs become TALL pines (crown far above eye height) or are dropped when they stand within 4 m of the footpath / stations
FRONT = (-800, 2400, 1450, 3050)
front_lines = [LY.ROUTE_A[:4], LY.CONNECT, LY.DESCENT, [(1050, 2350), (760, 600)], [(850, 1950), (620, 2620)]]
def in_front(x, y): return FRONT[0] < x < FRONT[1] and FRONT[2] < y < FRONT[3]
def near_front_lines(x, y, d): return any(dpoly(x, y, l) < d for l in front_lines)
conv = collections.Counter(); dropped_front = 0
for key, xf in list(base.items()):
    n = short(key[0])
    if n in PL.FIR_SWAP:
        for t in xf:
            x, y = t[0], t[1]
            if in_front(x, y):
                if near_front_lines(x, y, 420) or rdist(x, y) < 420: dropped_front += 1; continue
                mesh, sc = rng.choice([('SM_PineTree01', 0.85, 1.0), ('SM_PineTree03', 0.8, 0.95)])[0], rng.uniform(0.82, 0.98)
                ft = 'FT_EX_PF_TallFront'
            else:
                mesh, sc = pick(PL.FIR_SWAP[n]); ft = FT_OF_MESH.get(mesh)
                if ft is None and mesh == 'SM_PineTree05': ft = 'FT_EX_PF_PineTree05'
            add_new(ft, x, y, zf(x, y) - 8.0, rng.uniform(0, 360), sc); conv[mesh] += 1
            BIG.append((x, y, sc * PL.PAL[mesh]['h'], mesh))
        base[key] = []; stats['fir_removed_' + n] = len(xf)
stats['fir_converted'] = dict(conv); stats['front_firs_dropped'] = dropped_front
# ---- young: black spruce -> 35 % kept, rest PFP juveniles / saplings
conv = collections.Counter()
for key, xf in list(base.items()):
    n = short(key[0])
    if n in PL.YOUNG_SWAP:
        keep = []
        for t in xf:
            if in_front(t[0], t[1]) and (near_front_lines(t[0], t[1], 650) or rdist(t[0], t[1]) < 450): continue   # p2: clear the house-front sightlines (young pines at eye height filled P0_house_back)
            if rng.random() < PL.YOUNG_KEEP_FRACTION and n != 'Pine_08':
                keep.append(t); continue
            mesh, sc = pick(PL.YOUNG_SWAP[n]); ft = FT_OF_MESH.get(mesh, 'FT_EX_PF_Juvenile')
            add_new(ft, t[0], t[1], zf(t[0], t[1]) - 4.0, rng.uniform(0, 360), sc); conv[mesh] += 1
        base[key] = keep; stats['young_' + n] = (len(xf), len(keep))
stats['young_converted'] = dict(conv)
# ---- 2. bushes
conv = collections.Counter()
for key, xf in list(base.items()):
    n = short(key[0])
    if n in PL.BUSH_SWAP:
        for t in xf:
            mesh, sc = pick(PL.BUSH_SWAP[n]); add_new(FT_OF_MESH[mesh], t[0], t[1], zf(t[0], t[1]) - 6.0, rng.uniform(0, 360), sc); conv[mesh] += 1
        base[key] = []; stats['bush_' + n] = len(xf)
stats['bush_converted'] = dict(conv)
# ---- 3. litter: broadleaf only within 12 m of an oak
oaks = [(t[0], t[1]) for key, xf in base.items() if short(key[0]).startswith('SM_Oak') for t in xf]
conv = collections.Counter()
for key, xf in list(base.items()):
    n = short(key[0])
    if n in PL.LITTER_SWAP:
        keep = []
        for t in xf:
            if any(math.hypot(t[0] - ox, t[1] - oy) < 1200 for ox, oy in oaks):
                keep.append(t); continue
            mesh, sc = pick(PL.LITTER_SWAP[n]); ft = FT_OF_MESH.get(mesh)
            if ft is None:   # DeadBranch01 exists as an owned type: route to the existing component
                base[(P['PF'] + 'DeadLeaves/SM_DeadBranch01', (2200, 4200))].append([t[0], t[1], round(zf(t[0], t[1]) + 1, 1), 0.0, rng.uniform(0, 360), 0.0, sc, sc, sc]); continue
            pr = pitch_roll_for(t[0], t[1], t[4]); add_new(ft, t[0], t[1], zf(t[0], t[1]) + 1.0, t[4], sc, pr[0], pr[1]); conv[mesh] += 1
        base[key] = keep; stats['litter_' + n] = (len(xf), len(keep))
stats['litter_converted'] = dict(conv)
# ---- acid-green wild fern: halve (keep those near rocks / water / logs by chance), rest removed
for key, xf in list(base.items()):
    if short(key[0]) == 'SM_FernWild01':
        keep = [t for t in xf if rng.random() < 0.5]; base[key] = keep; stats['fernwild'] = (len(xf), len(keep))
# ---- house front quiet zone: small plants within 9 m of the house only at the four corners (foundation ferns) and never on the footpath
CORNERS = [(-350, -350), (1870, -350), (-350, 1490), (1870, 1490)]
for key, xf in list(base.items()):
    n = short(key[0])
    if n.startswith(('SM_Grass', 'SM_GroundCover', 'SM_Fern', 'SM_DeadLeaves', 'wgxjfhr', 'tkwqbbofa')):
        keep = []
        for t in xf:
            if in_house(t[0], t[1], 900) and not in_house(t[0], t[1], -50):
                near_corner = any(math.hypot(t[0] - cx, t[1] - cy) < 320 for cx, cy in CORNERS)
                if not (near_corner and n.startswith('SM_Fern') and rng.random() < 0.7):
                    continue
            keep.append(t)
        if len(keep) != len(xf): stats['housefront_' + n] = (len(xf), len(keep))
        base[key] = keep
# ---- Nordic flat patch (tkwqbbofa) only on near-flat ground (floated on slopes: XR4/VMP lesson)
for key, xf in list(base.items()):
    if short(key[0]).startswith('tkwqbbofa'):
        keep = [t for t in xf if slope_deg(t[0], t[1]) < 9]; base[key] = keep; stats['nordic_patch'] = (len(xf), len(keep))

# ================================================================ 4. heroes, moss, floor, rocks, deadwood (new types)
HERO = [(-330, 2470, 1.25), (1980, 2640, 1.2), (2330, 3620, 1.3), (1780, 6420, 1.2), (-1700, 9320, 1.25), (1250, -6900, 1.2), (3100, 300, 1.15), (-2500, 1200, 1.2)]
for x, y, sc in HERO:
    if in_house(x, y, 500) or rdist(x, y) < 260: continue
    add_new('FT_EX_PF_PineTree04', x, y, zf(x, y) - 10.0, rng.uniform(0, 360), sc); BIG.append((x, y, sc * 3906, 'SM_PineTree04'))
stats['hero_pines'] = len(newfol['FT_EX_PF_PineTree04'])
LEDGE = [(3120, 3350), (3100, 3900), (3080, 4300), (3105, 4750), (3130, 5200), (3090, 5650), (3050, 6100)]
GC = (-900.0, 8750.0)
# moss pockets: (centre, radius cm, core density per m2, cause)
MOSS = [((GC[0], GC[1]), 640, 32.0, 'glade terrace'), ((1450, -6250), 440, 18.0, 'saddle'), ((-1950, -100), 340, 14.0, 'west clearing'), ((3650, 8000), 320, 24.0, 'inlet head'),
        ((2300, 7250), 280, 20.0, 'inlet mouth'), ((-650, 1250), 320, 18.0, 'house west shade'), ((620, 2620), 240, 8.0, 'landing edge'), ((2850, -1750), 260, 14.0, 'narrows'),
        ((1750, -4500), 320, 14.0, 'climb bench'), ((-3300, 3500), 340, 14.0, 'west shore pocket'), ((-2900, 6200), 320, 14.0, 'sw bank pocket'), ((-1500, 9250), 380, 22.0, 'glade oak foot'),
        ((300, 3150), 260, 16.0, 'landing rocks'), ((2470, 6850), 260, 16.0, 'inlet rocks'), ((1300, -5000), 260, 12.0, 'climb rocks')]
for k, (px, py) in enumerate([(3000, 3600), (2990, 4100), (3010, 4600), (3020, 5100), (2990, 5600)]):
    MOSS.append(((px, py), 250, 26.0, 'ledge foot %d' % k))
moss_n = 0
for (cx, cy), r, dens, why in MOSS:
    n_want = int(math.pi * (r / 100.0) ** 2 * dens)
    for _ in range(n_want):
        a = rng.uniform(0, 2 * math.pi); rr = r * math.sqrt(rng.random()); x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr
        if in_house(x, y, 60) or zf(x, y) < WATER + 8 or slope_deg(x, y) > 30: continue
        if rdist(x, y) < 110: continue                                       # not on the tread centre
        fade = 1 - (rr / r) ** 2
        if rng.random() > 0.35 + 0.65 * fade: continue
        mesh = rng.choice(['SM_MossLeaf_01', 'SM_MossLeaf_02', 'SM_MossLeaf_03', 'SM_MossLeaf_04', 'SM_MossLeaf_03', 'SM_MossLeaf_02', 'SM_MossClump01'])
        ft = FT_OF_MESH[mesh]; lo, hi = PL.NEW_TYPES[ft][6]; yaw = rng.uniform(0, 360); pr = pitch_roll_for(x, y, yaw)
        sc = rng.uniform(lo, hi) * 0.72        # p2: the p1 moss read as neon fern-like clumps at x2-3; finer leaves
        add_new(ft, x, y, zf(x, y) + 0.5, yaw, sc, pr[0], pr[1]); moss_n += 1
stats['moss_instances'] = moss_n
# p5: continuous moss-leaf carpet band along the main routes (the reference floor is a green carpet, not pockets): 1.5-6.5 m off the
# tread centre, density fading outward, finer scale; skips water, steep slopes, the house and the stone arc; capped
band_n = 0; BAND_CAP = 7000
for poly in MAIN:
    for a, c in zip(poly, poly[1:]):
        vx, vy = c[0] - a[0], c[1] - a[1]; L = math.hypot(vx, vy)
        if L < 1: continue
        ux, uy = vx / L, vy / L; nx, ny = -uy, ux
        for s in range(0, int(L), 50):
            for _ in range(24):   # p6: denser carpet (p5's 9 tries gave 2.4k leaves, barely visible)
                if band_n >= BAND_CAP: break
                d = rng.uniform(150, 750) * rng.choice((-1, 1)); fade = 1 - ((abs(d) - 150) / 600.0) ** 2
                if rng.random() > 0.25 + 0.75 * fade: continue
                x = a[0] + ux * s + nx * d + rng.uniform(-25, 25); y = a[1] + uy * s + ny * d + rng.uniform(-25, 25)
                if rdist(x, y) < 130 or in_house(x, y, 60) or zf(x, y) < WATER + 8 or slope_deg(x, y) > 30 or not ring_inside(x, y): continue
                mesh = rng.choice(['SM_MossLeaf_01', 'SM_MossLeaf_02', 'SM_MossLeaf_03', 'SM_MossLeaf_04', 'SM_MossLeaf_02', 'SM_MossClump01'])
                ft = FT_OF_MESH[mesh]; lo, hi = PL.NEW_TYPES[ft][6]; yaw = rng.uniform(0, 360); pr = pitch_roll_for(x, y, yaw)
                add_new(ft, x, y, zf(x, y) + 0.5, yaw, rng.uniform(lo, hi) * 0.68, pr[0], pr[1]); band_n += 1
stats['moss_band_instances'] = band_n
# needle litter + cones + branches + mushrooms + ground patches: causes = big trees near the viewed band (<= 28 m from a route)
VIEW = lambda x, y: rdist_all(x, y) < 2800 and ring_inside(x, y) and zf(x, y) > WATER + 10 and not in_house(x, y, 40)
needles = cones = branches = shrooms = 0
for x, y, h, n in BIG:
    if not VIEW(x, y): continue
    big = h > 1800
    for _ in range(rng.randint(4, 9) if big else rng.randint(1, 3)):
        a = rng.uniform(0, 2 * math.pi); d = rng.uniform(120, 900 if big else 500); px, py = x + math.cos(a) * d, y + math.sin(a) * d
        if not VIEW(px, py) or rdist(px, py) < 90 or slope_deg(px, py) > 35: continue
        yaw = rng.uniform(0, 360); pr = pitch_roll_for(px, py, yaw); lo, hi = PL.NEW_TYPES['FT_EX_PF_Needle'][6]
        add_new('FT_EX_PF_Needle', px, py, zf(px, py) + 0.5, yaw, rng.uniform(lo, hi), pr[0], pr[1]); needles += 1
    if big and n.startswith('SM_PineTree'):
        for _ in range(rng.randint(2, 5)):
            a = rng.uniform(0, 2 * math.pi); d = rng.uniform(90, 420); px, py = x + math.cos(a) * d, y + math.sin(a) * d
            if not VIEW(px, py) or rdist(px, py) < 70: continue
            add_new('FT_EX_PF_Cone', px, py, zf(px, py) + 1.0, rng.uniform(0, 360), rng.uniform(0.85, 1.25)); cones += 1   # p2: p1 cones (x1.4-2.2) read as footballs
        if rng.random() < 0.35:
            a = rng.uniform(0, 2 * math.pi); d = rng.uniform(250, 700); px, py = x + math.cos(a) * d, y + math.sin(a) * d
            if VIEW(px, py) and rdist(px, py) > 200 and slope_deg(px, py) < 28:
                yaw = rng.uniform(0, 360); pr = pitch_roll_for(px, py, yaw); lo, hi = PL.NEW_TYPES['FT_EX_PF_FallenBranches01'][6]
                add_new('FT_EX_PF_FallenBranches01', px, py, zf(px, py) - 2.0, yaw, rng.uniform(lo, hi), pr[0], pr[1]); branches += 1
stats.update(needles=needles, cones=cones, fallen_branches=branches)
# dead-leaf litter clumps (needle floor cards) in the viewed band, denser under canopy, never on the tread centre
litter = 0; tries = 0
while litter < 950 and tries < 60000:   # p2: fewer, darker litter cards (the pale DeadLeaves04 mats read as paper on the climb)
    tries += 1; x, y = rng.uniform(-5200, 5000), rng.uniform(-7600, 9600)
    if not VIEW(x, y) or rdist(x, y) < 100 or slope_deg(x, y) > 32: continue
    mesh = rng.choice(['SM_DeadLeaves03', 'SM_DeadLeaves03', 'SM_DeadLeaves03', 'SM_DeadLeaves04']); ft = FT_OF_MESH[mesh]; lo, hi = PL.NEW_TYPES[ft][6]
    yaw = rng.uniform(0, 360); pr = pitch_roll_for(x, y, yaw); add_new(ft, x, y, zf(x, y) + 1.0, yaw, rng.uniform(lo, hi), pr[0], pr[1]); litter += 1
stats['litter_clumps'] = litter
# ground patches: flat tread shoulders (slope < 12), sunk; trail patches on main treads at bends; rocky ground at shore pockets / inlet
gp = tp = rg = 0
for route in MAIN:
    cum = [0.0]
    for a, b in zip(route, route[1:]): cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    s = rng.uniform(200, 500)
    while s < cum[-1]:
        for k in range(len(route) - 1):
            if s <= cum[k + 1]:
                L = cum[k + 1] - cum[k]; t = (s - cum[k]) / L; a, b = route[k], route[k + 1]
                x, y = a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]); th = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])); break
        side = rng.choice([-1, 1]); off = rng.uniform(150, 260)
        px, py = x + math.cos(math.radians(th + 90 * side)) * off, y + math.sin(math.radians(th + 90 * side)) * off
        if VIEW(px, py) and slope_deg(px, py) < 14 and not in_house(px, py, 200) and rng.random() < 0.6:
            yaw = th + rng.uniform(-25, 25); pr = pitch_roll_for(px, py, yaw); lo, hi = PL.NEW_TYPES['FT_EX_PF_GroundPatch'][6]
            add_new('FT_EX_PF_GroundPatch', px, py, zf(px, py) - 6.0, yaw, rng.uniform(lo, hi), pr[0], pr[1]); gp += 1
        # the tread itself: the pack's trail / ground patch plates (worn soil, roots, needles) laid along the route, overlapping, sunk 10 cm;
        # no painted path layer is reachable from Python in 5.8, so the pack's own patch method carries the tread language
        if slope_deg(x, y) < 17 and not in_house(x, y, 120):
            ft = rng.choice(['FT_EX_PF_TrailPatch01', 'FT_EX_PF_TrailPatch02', 'FT_EX_PF_GroundPatch01', 'FT_EX_PF_GroundPatch04', 'FT_EX_PF_TrailPatch02'])
            jx, jy = x + rng.uniform(-35, 35), y + rng.uniform(-35, 35)
            yaw = th + rng.uniform(-20, 20); pr = pitch_roll_for(jx, jy, yaw); lo, hi = PL.NEW_TYPES[ft][6]
            add_new(ft, jx, jy, zf(jx, jy) - 10.0, yaw, rng.uniform(lo, hi), pr[0], pr[1]); tp += 1
        s += rng.uniform(260, 340)
for (cx, cy) in ((330, 2980), (-1200, 2800), (2450, 6500), (3400, 7800), (-3600, 5200), (1200, 8200)):
    for _ in range(rng.randint(2, 3)):
        x, y = cx + rng.uniform(-280, 280), cy + rng.uniform(-280, 280)
        if zf(x, y) > WATER + 5 and slope_deg(x, y) < 14 and rdist(x, y) > 120:
            yaw = rng.uniform(0, 360); pr = pitch_roll_for(x, y, yaw); lo, hi = PL.NEW_TYPES['FT_EX_PF_RockyGround'][6]
            add_new('FT_EX_PF_RockyGround', x, y, zf(x, y) - 10.0, yaw, rng.uniform(lo, hi), pr[0], pr[1]); rg += 1
stats.update(ground_patches=gp, trail_patches=tp, rocky_ground=rg)
# boulder groups (moss-topped PFP ground rocks): shore, shelf foot, bends; 2-4 blocks, 30-45 % buried, never within 2.4 m of a tread
GROUPS = [(300, 3150, 3), (-1500, 2850, 2), (2470, 6850, 3), (-600, 9400, 2), (3550, 7700, 3), (-3700, 4600, 3), (2850, -2500, 3), (1300, -5000, 2), (-2350, -2500, 2), (4100, -1200, 2), (-3100, 7500, 2), (1850, 3400, 2)]
rocks = 0; GROUP_XY = []
for cx, cy, n in GROUPS:
    placed = []
    for i in range(n):
        for _ in range(12):
            x, y = cx + rng.uniform(-300, 300), cy + rng.uniform(-300, 300)
            if all(math.hypot(x - a, y - b) > 180 for a, b in placed): break
        if rdist(x, y) < 240 or in_house(x, y, 300) or zf(x, y) < WATER - 30: continue
        mesh = rng.choice(['SM_PineGroundRock02', 'SM_PineGroundRock04', 'SM_PineGroundRock06', 'SM_PineGroundRock02']); ft = FT_OF_MESH[mesh]
        sc = rng.uniform(0.7, 1.55) if i else rng.uniform(1.1, 1.6)      # p2: one parent block, smaller fragments (no equal-size rows)
        e, o = PL.ext(mesh); sink = rng.uniform(0.3, 0.5) * 2 * e[2] * sc
        add_new(ft, x, y, zf(x, y) - sink, rng.uniform(0, 360), sc, rng.uniform(-8, 8), rng.uniform(-8, 8)); rocks += 1; placed.append((x, y)); GROUP_XY.append((x, y, sc * e[0] * 2))
stats['boulders'] = rocks
# small logs + mushrooms at logs / stumps (viewed band, off the tread)
logs = 0; tries = 0
while logs < 26 and tries < 20000:
    tries += 1; x, y = rng.uniform(-5000, 4800), rng.uniform(-7400, 9500)
    if not VIEW(x, y) or rdist(x, y) < 260 or slope_deg(x, y) > 26: continue
    yaw = rng.uniform(0, 360); pr = pitch_roll_for(x, y, yaw); lo, hi = PL.NEW_TYPES['FT_EX_PF_DeadTrunk04'][6]
    add_new('FT_EX_PF_DeadTrunk04', x, y, zf(x, y) - 4.0, yaw, rng.uniform(lo, hi), pr[0], pr[1]); logs += 1
    for _ in range(rng.randint(2, 4)):
        a = rng.uniform(0, 2 * math.pi); d = rng.uniform(40, 130); px, py = x + math.cos(a) * d, y + math.sin(a) * d
        lo2, hi2 = PL.NEW_TYPES['FT_EX_PF_Mushroom01'][6]; add_new('FT_EX_PF_Mushroom01', px, py, zf(px, py) + 0.5, rng.uniform(0, 360), rng.uniform(lo2, hi2)); shrooms += 1
stats.update(small_logs=logs, mushrooms=shrooms)
# field cover (open pockets): WeedA + GroundCover02 in the ForestField pockets
fc = 0
for (cx, cy), r in (((GC[0], GC[1]), 700), ((1450, -6250), 500), ((-1950, -100), 380), ((3900, -1050), 320), ((-3300, 3500), 420), ((-2900, 6200), 400)):
    for _ in range(int(math.pi * (r / 100) ** 2 * 0.35)):
        a = rng.uniform(0, 2 * math.pi); rr = r * math.sqrt(rng.random()); x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr
        if rdist(x, y) < 120 or slope_deg(x, y) > 24 or zf(x, y) < WATER + 10: continue
        mesh = rng.choice(['SM_WeedA_01', 'SM_GroundCover02', 'SM_GroundCover02']); ft = FT_OF_MESH[mesh]; lo, hi = PL.NEW_TYPES[ft][6]
        yaw = rng.uniform(0, 360); pr = pitch_roll_for(x, y, yaw); add_new(ft, x, y, zf(x, y) + 0.5, yaw, rng.uniform(lo, hi), pr[0], pr[1]); fc += 1
stats['field_cover'] = fc
# rock-foot ferns (long fern 02) at the ledge and boulder groups (cause: shade + moisture at the rock foot)
rf = 0
for (px, py) in [(2990, 3500), (2980, 3950), (3000, 4450), (3010, 4900), (2990, 5400), (2970, 5900)]:
    for _ in range(rng.randint(2, 4)):
        x, y = px + rng.uniform(-150, 150), py + rng.uniform(-150, 150)
        if rdist(x, y) < 150 or zf(x, y) < WATER + 5: continue
        lo, hi = PL.NEW_TYPES['FT_EX_PF_FernLong02'][6]; add_new('FT_EX_PF_FernLong02', x, y, zf(x, y) - 2.0, rng.uniform(0, 360), rng.uniform(lo, hi)); rf += 1
for (bx, by, bw) in GROUP_XY:        # p2: ferns at the boulder FOOT (outside the block footprint), never on top of the rock
    for _ in range(rng.randint(1, 2)):
        a = rng.uniform(0, 2 * math.pi); d = bw * 0.55 + rng.uniform(40, 110); x, y = bx + math.cos(a) * d, by + math.sin(a) * d
        if rdist(x, y) < 150 or zf(x, y) < WATER + 5 or in_house(x, y, 300): continue
        lo, hi = PL.NEW_TYPES['FT_EX_PF_FernLong02'][6]; add_new('FT_EX_PF_FernLong02', x, y, zf(x, y) - 2.0, rng.uniform(0, 360), rng.uniform(lo, hi)); rf += 1
stats['rock_foot_ferns'] = rf
# house front: 5 flat stepping stones on the front footpath (existing PineStone04 component), the hero pair is in HERO
for k, s in enumerate((0.12, 0.3, 0.48, 0.66, 0.84)):
    pts = LY.ROUTE_A[:4]; cum = [0.0]
    for a, b in zip(pts, pts[1:]): cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    sd = s * cum[-1]
    for i in range(len(pts) - 1):
        if sd <= cum[i + 1]:
            L = cum[i + 1] - cum[i]; t = (sd - cum[i]) / L; a, b = pts[i], pts[i + 1]; x, y = a[0] + t * (b[0] - a[0]) + rng.uniform(-18, 18), a[1] + t * (b[1] - a[1]) + rng.uniform(-18, 18); break
    base[(P['PF'] + 'Rocks/SM_PineStone04', (10000, 16000))].append([round(x, 1), round(y, 1), round(zf(x, y) - 48, 1), 0.0, rng.uniform(0, 360), 0.0, 0.55, 0.55, 0.3])
stats['stepping_stones'] = 5

# ================================================================ 5. actors: x9 structure + i5 identity, converted to the PF family
SP9 = json.load(open(X2 + '/spawn_x9.json')); SP5 = I5['spawn']
SPAWN = []; CLIFF_MI = MAT_DIR + 'MI_EX_PF_Cliff'
MB = {}
for s in SP9:
    k = s['kind']
    if k == 'decal': continue                                   # path decals replaced by the GroundPath landscape layer
    r = {'kind': k, 'mesh': s['mesh'], 'label': s['label'].replace('XR2_', 'PFR_'), 'x': s['x'], 'y': s['y'], 'z': s['z'], 'yaw': s['yaw'], 'pitch': s.get('pitch', 0.0), 'roll': s.get('roll', 0.0), 'scale': s['scale']}
    if s.get('invisible'):
        r.update(invisible=True, profile='InvisibleWall')
    elif k == 'dress_soft':
        r['soft'] = True
    elif k in ('ring_rock', 'inner_rock', 'r6_outcrop', 'inner_bank'):
        r['camera_ignore'] = False; r['material'] = CLIFF_MI         # big masses keep camera collision; cooler mossier owned cliff MI
    else:
        r['camera_ignore'] = True
    if k == 'dress_tree' and 'Fir_Tree' in s['mesh']:
        r['mesh'] = P['PF'] + 'Trees/SM_PineTree06'; r['scale'] = [1.15, 1.15, 1.15]
    SPAWN.append(r)
# i5: ledge blocks -> PFP cliff family on the same strike (8 blocks), talus -> PFP ground rocks, spruces kept (6) / pines (5), arc r 4.2 m, dead trees + traces kept
ledge_k = 0; CL = ['SM_PineCliff02', 'SM_CliffRock01', 'SM_PineCliff03', 'SM_CliffRock02', 'SM_CliffRockCurve01']
for s in SP5:
    k = s['kind']; r = dict(s); r['label'] = s['label'].replace('XR4_', 'PFR_').replace('XR3_', 'PFR_')
    if k == 'pine_swap': continue
    if k == 'ledge':
        m = CL[ledge_k % len(CL)]; e, o = PL.ext(m); r['mesh'] = PL.M[m]; sc = s['scale'][0] * 0.95
        r['scale'] = [round(sc, 3)] * 3; r['z'] = round(zf(s['x'] + 60, s['y']) - (o[2] - e[2]) * sc - 0.42 * 2 * e[2] * sc, 1); r['camera_ignore'] = False; r['material'] = CLIFF_MI; ledge_k += 1
    elif k == 'talus':
        m = rng.choice(['SM_PineGroundRock02', 'SM_PineGroundRock04']); e, o = PL.ext(m); sc = rng.uniform(1.0, 1.4)
        r.update(mesh=PL.M[m], scale=[round(sc, 3)] * 3, z=round(zf(s['x'], s['y']) - (o[2] - e[2]) * sc - 0.35 * 2 * e[2] * sc, 1), camera_ignore=True)
    elif k == 'spruce':
        if rng.random() < 0.45:
            m = 'SM_PineTree06'; e, o = PL.ext(m); sc = rng.uniform(0.95, 1.2); r.update(mesh=PL.M[m], scale=[round(sc, 3)] * 3, z=round(zf(s['x'], s['y']) - 8, 1))
    elif k == 'uncanny':
        a = math.radians(-70 + int(s['label'].split('_')[-1]) * 17.5); r['x'] = round(GC[0] + 420 * math.cos(a), 1); r['y'] = round(GC[1] + 420 * math.sin(a), 1)
        e, o = PL.ext('SM_PineStone02'); r['scale'] = [0.85, 0.85, 0.85]; r['z'] = round(zf(r['x'], r['y']) - (o[2] - e[2]) * 0.85 - 0.5 * 2 * e[2] * 0.85, 1)   # p2: lower, half sunk
    SPAWN.append(r)
HIDE = list(I5.get('hide', []))   # the 4 XR2 single boulders under the ledge stay hidden (collision kept)
HIDE = [h.replace('XR2_', 'PFR_') for h in HIDE]
stats['spawn'] = dict(collections.Counter(s['kind'] for s in SPAWN))

# ================================================================ 6. materials (project-owned only) + 7. look
TX = '/Game/PineForestPack/Textures/Landscape/'; TXO = '/Game/GraceRanger/Environment/Exterior20260921/Textures/'; VMA = '/Game/Sphirus/World/Chapter01/VisualMotionAcceptance/BackgroundMemory/'
# p2: the 12 vendor 4K scans pushed the texture streaming pool 77-323 MB over budget (red warning in every p1 walk frame). Only the two
# dominant sets are used, as project-owned copies capped at 2K (max_texture_size); Sand / Cliff keep the existing 2K VMA set.
NEWTEX = {TXO + 'T_EX_PF_PineGround01_D': {'source': TX + 'T_PineGround01_D', 'max_size': 2048}, TXO + 'T_EX_PF_PineGround01_N': {'source': TX + 'T_PineGround01_N', 'max_size': 2048},
          TXO + 'T_EX_PF_PineGround01_H': {'source': TX + 'T_PineGround01_H', 'max_size': 1024}, TXO + 'T_EX_PF_GroundForest01_D': {'source': TX + 'T_GroundForest01_D', 'max_size': 2048},
          TXO + 'T_EX_PF_GroundForest01_N': {'source': TX + 'T_GroundForest01_N', 'max_size': 2048}, TXO + 'T_EX_PF_GroundForest01_H': {'source': TX + 'T_GroundForest01_H', 'max_size': 1024}}
MATS = {
    # p5: the sun highlight on the pond read as a white patch from the house (P0_refuge_front_path): rougher, less specular, more ripple
    MAT_DIR + 'MI_EX_Pond': {'scalar': {'Roughness': 0.7, 'Specular': 0.06, 'Murkiness': 7.0, 'Calm Normal Amplitude': 0.08}, 'vector': {'Absorption': [0.24, 0.19, 0.13, 1.0]}},
    # the owned auto landscape instance re-skinned with the pack's ground scans (no painted layers are reachable from Python in 5.8):
    # Forest = needle floor under the canopy, Grass = forest soil with litter (replaces the lawn); matching height maps in the mask slots
    MAT_DIR + 'MI_EX_Integration_Valley': {
        'texture': {'Forest Color': TXO + 'T_EX_PF_PineGround01_D', 'Forest Normal': TXO + 'T_EX_PF_PineGround01_N', 'Forest Mask': TXO + 'T_EX_PF_PineGround01_H',
                    'Grass Color': TXO + 'T_EX_PF_GroundForest01_D', 'Grass Normal': TXO + 'T_EX_PF_GroundForest01_N', 'Grass Mask': TXO + 'T_EX_PF_GroundForest01_H',
                    # Sand / Cliff explicitly back on the project's 2K VMA set (p1 had put the 4K vendor scans there)
                    'Sand Color': VMA + 'T_VMA_BG_Sand_Color_2K', 'Sand Normal': VMA + 'T_VMA_BG_Sand_Normal_2K', 'Sand Mask': VMA + 'T_VMA_BG_Sand_Mask_2K',
                    'Cliff Color': VMA + 'T_VMA_BG_Cliff_Color_2K', 'Cliff Normal': VMA + 'T_VMA_BG_Cliff_Normal_2K', 'Cliff Mask': VMA + 'T_VMA_BG_Cliff_Mask_2K'},
        'scalar': {'Forest Tiling': 420.0, 'Grass Tiling': 440.0, 'Sand Tiling': 400.0, 'Cliff Tiling': 600.0, 'Macro Variation Contrast': 0.22, 'Forest Specular': 0.2},
        # p5: floor chroma toward the reference (0.26 -> 0.36 measured gap): a mossy-green cast on the two floor sets instead of the neutral brown
        'vector': {'Forest Color Offset': [0.52, 0.62, 0.42, 1.0], 'Grass Color Offset': [0.55, 0.68, 0.44, 1.0], 'Sand Color Offset': [0.5, 0.45, 0.38, 1.0], 'Cliff Color Offset': [0.5, 0.54, 0.53, 1.0]}},
}
LITTER_MI = {MAT_DIR + 'MI_EX_PF_DeadLeaves01': '/Game/PineForestPack/Materials/MaterialInstances/Foliage/MI_DeadLeaves01', MAT_DIR + 'MI_EX_PF_DeadLeaves02': '/Game/PineForestPack/Materials/MaterialInstances/Foliage/MI_DeadLeaves02'}
NEWMATS = {   # owned instances created from vendor instances (never modified vendor assets)
    # p3: the litter cards read as pale paper in direct sun (house front, climb) - darker, less saturated owned copies, assigned on the owned FTs
    MAT_DIR + 'MI_EX_PF_DeadLeaves01': {'parent_of': LITTER_MI[MAT_DIR + 'MI_EX_PF_DeadLeaves01'], 'scalar': {'Albedo_Brightness': 0.4, 'Roughness': 3.0}, 'vector': {'Color_Tint': [0.5, 0.4, 0.24, 1.0]}},
    MAT_DIR + 'MI_EX_PF_DeadLeaves02': {'parent_of': LITTER_MI[MAT_DIR + 'MI_EX_PF_DeadLeaves02'], 'scalar': {'Albedo_Brightness': 0.48, 'Roughness': 2.4}, 'vector': {'Color_Tint': [0.47, 0.38, 0.26, 1.0]}},
    CLIFF_MI: {'parent_of': '/Game/PineForestPack/Materials/MaterialInstances/Rocks/MI_CliffRock01', 'scalar': {'Albedo_Brightness': 0.8, 'Moss_Opacity': 0.9, 'Moss_FuzzyPower': 1.3, 'Moss_Roughness': 2.6}, 'vector': {'Color_Tint': [0.66, 0.7, 0.72, 1.0], 'Moss_ColorTint': [0.24, 0.33, 0.18, 1.0]}},
}
LOOK = {   # PF morning on the existing owners (XR5 FINAL v2 is the fallback); measured at the 24 stations before adoption
    # p4 (final): the p2/p3 haze muted everything (places mean 74 / sat 0.245 vs showcase 79 / 0.36; the restored XR5 light read crisper):
    # keep the PF sun direction / colour, bring the fog back to XR5's clarity, moderate god rays, full saturation, +0.15 EV
    # p6: the sun's specular highlight on the pond stayed a white patch after the water-material change -> the light's own specular scale
    'sun': {'rot': [-30.0, -60.0], 'intensity': 1500.0, 'temperature': 5300.0, 'light_source_angle': 1.4, 'volumetric_scattering_intensity': 1.5, 'specular_scale': 0.55},
    'sky': {'intensity': 1.3},
    'fog': {'fog_density': 0.013, 'fog_height_falloff': 0.2, 'start_distance': 200.0, 'fog_max_opacity': 0.6, 'volumetric_fog_extinction_scale': 1.2, 'volumetric_fog_albedo': [235, 226, 212], 'volumetric_fog_scattering_distribution': 0.5},
    'atmos': {'mie_scattering_scale': 0.035, 'mie_anisotropy': 0.4},
    'pp': {'white_temp': 6000.0, 'color_saturation': [1.06, 1.06, 1.06, 1.0], 'color_contrast': [1.06, 1.06, 1.06, 1.0], 'film_slope': 0.8, 'film_toe': 0.55, 'film_shoulder': 0.26, 'bloom_intensity': 0.35, 'vignette_intensity': 0.4, 'auto_exposure_bias': -0.45},
}

# ---- p2: house-front sightline sweep (porch -> landing -> footpath, house_back / front_path stations): no sapling, juvenile, young
# spruce or bush within 5 m of the camera lines, no broadleaf cover within 2.5 m of the tread (the p1 P0_house_back frame was a juvenile pine)
swept = collections.Counter()
for key, xf in list(base.items()):
    n = short(key[0])
    if n.startswith(('SM_Pine_Juvenile', 'SM_Young_Black', 'SM_Bush', 'SM_PineTreeLowSmall', 'SM_SonoSapling', 'SM_SonoTree')):
        keep = [t for t in xf if not (in_front(t[0], t[1]) and near_front_lines(t[0], t[1], 520))]; swept[n] += len(xf) - len(keep); base[key] = keep
for ft, xf in list(newfol.items()):
    if any(k in ft for k in ('Bush', 'Salix', 'Sapling', 'SonoTree', 'Juvenile', 'LowSmall')):
        keep = [t for t in xf if not (in_front(t[0], t[1]) and near_front_lines(t[0], t[1], 380))]; swept[ft] += len(xf) - len(keep); newfol[ft] = keep
stats['front_sweep'] = dict(swept)

# ================================================================ 7. write
json.dump({'variant': V, 'terrain': 'x9', 'file': X2 + '/height_x9.png', 'samples': plan9['samples'], 'stats': stats, 'hero': HERO, 'moss_pockets': [[c, r, d, w] for c, r, d, w in MOSS]}, open('%s/plan_%s.json' % (OUT, V), 'w'), indent=1, default=str)
fol = [{'mesh': k[0], 'cull': list(k[1]), 'xf_after': xf} for k, xf in base.items()]
json.dump(fol, open('%s/foliage_%s.json' % (OUT, V), 'w'))
nf = {}
for ft, xf in newfol.items():
    mesh, cull, col, sh, al, ry, sc = PL.NEW_TYPES[ft] if ft in PL.NEW_TYPES else (None,) * 7
    if mesh is None:
        extra = {'FT_EX_PF_Juvenile': ('SM_Pine_Juvenile_01', [9500, 14500], False, True, False, True, (0.8, 1.2)), 'FT_EX_PF_PineTree05': ('SM_PineTree05', [36000, 44000], True, True, False, True, (0.6, 0.8)),
                 'FT_EX_PF_TallFront': ('SM_PineTree03', [36000, 44000], True, True, False, True, (0.8, 1.0))}
        mesh, cull, col, sh, al, ry, sc = extra[ft]
    nf[ft] = {'mesh': PL.M[mesh], 'cull': cull, 'collision': col, 'cast_shadow': sh, 'align_to_normal': al, 'random_yaw': ry, 'scale': list(sc), 'xf': xf}
    if ft in getattr(PL, 'FT_MATS', {}): nf[ft]['materials'] = PL.FT_MATS[ft]
json.dump(nf, open('%s/newfol_%s.json' % (OUT, V), 'w'))
json.dump({'spawn': SPAWN, 'hide': HIDE}, open('%s/spawn_%s.json' % (OUT, V), 'w'), indent=0)
json.dump({'mats': MATS, 'newmats': NEWMATS, 'newtex': NEWTEX}, open('%s/mats_%s.json' % (OUT, V), 'w'), indent=1)
json.dump(LOOK, open('%s/look_%s.json' % (OUT, V), 'w'), indent=1)
tot_new = sum(len(v['xf']) for v in nf.values()); tot_old = sum(len(f['xf_after']) for f in fol)
print('DESIGN', V, 'existing comps', len(fol), 'instances', tot_old, '| new types', len(nf), 'instances', tot_new, '| actors', len(SPAWN))
print(json.dumps(stats, default=str)[:2500])
print('new type counts', {k: len(v['xf']) for k, v in sorted(nf.items(), key=lambda kv: -len(kv[1]['xf']))})
# preview map (top-down, 10 m grid): trees dark green, new pines green, moss light, rocks grey, paths orange
W = 1420 // 2; Hh = 2080 // 2; img = np.zeros((Hh, W, 3), np.uint8); img[:] = (28, 40, 26)
def px(x, y): return int((x + 7600) / 20), int((y + 9600) / 20)
for key, xf in base.items():
    n = short(key[0]); c = (70, 110, 60) if n.startswith('SM_PineTree') else (120, 90, 60) if n.startswith('SM_Oak') else None
    if c:
        for t in xf:
            i, j = px(t[0], t[1]);
            if 0 <= i < W and 0 <= j < Hh: img[j, i] = c
for ft, v in nf.items():
    c = (90, 170, 80) if 'Pine' in ft or 'Sono' in ft else (150, 190, 110) if 'Moss' in ft else (140, 140, 140) if 'Rock' in ft else None
    if c:
        for t in v['xf']:
            i, j = px(t[0], t[1])
            if 0 <= i < W and 0 <= j < Hh: img[j, i] = c
for route in MAIN + SPURS + FAINT:
    for a, b in zip(route, route[1:]):
        for t in np.linspace(0, 1, 80):
            i, j = px(a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
            if 0 <= i < W and 0 <= j < Hh: img[j, i] = (230, 150, 60)
for s in SPAWN:
    i, j = px(s['x'], s['y']);
    if 0 <= i < W and 0 <= j < Hh: img[j, i] = (200, 200, 220) if 'Rock' in s['kind'] or s['kind'] in ('ledge', 'r6_outcrop') else (160, 110, 70)
raw = b''.join(b'\x00' + img[r].tobytes() for r in range(Hh)); ch = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
open('%s/preview_%s.png' % (OUT, V), 'wb').write(b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', W, Hh, 8, 2, 0, 0, 0)) + ch(b'IDAT', zlib.compress(raw, 6)) + ch(b'IEND', b''))
