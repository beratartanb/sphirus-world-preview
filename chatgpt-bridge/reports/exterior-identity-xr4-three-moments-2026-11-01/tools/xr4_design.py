"""xr4_design.py (offline, Blender Python + numpy): XR4 "three atmospheric moments" on the route A slice.
Writes TWO variants that the existing appliers consume in order:
  XR2 format 'x9' (Saved/Codex/ExteriorWorld_XR2_20261031/design/{height,plan,foliage,foliage_full,spawn,overlay}_x9.*):
      x8 terrain + the XR4 terrain deltas (ledge berm, glade terrace), x8 foliage regrounded (counts unchanged), x8 spawns re-z'd.
  XR3 format 'i4' (Saved/Codex/ExteriorIdentity_XR3_20261031/design/id_i4.json):
      foliage removals / tilts (counts change), XR4 spawns, material briefs, retints, hidden XR2 rocks.
Diagnosis this answers (why the slice still reads as a forest-pack demo, beyond colour):
  1. no value hierarchy: no dominant dark mass near the camera, no single light focus  -> hero trunks (1 m+ diameter) at the frame
     edges, dense dark spruce on the ledge top, the ground under the ledge emptied to bare needle floor, ONE light release per moment
  2. no scale hierarchy: every trunk 30-50 cm, every plant the same size                 -> 4 hero pines x1.3, talus boulders of 3 sizes
  3. rocks are props: single boulders with gaps on a smooth slope                           -> ONE continuous bedrock ledge: 9 overlapping
     grey blocks with a common strike, buried 45 %, a soil berm behind, talus + moss + fern only at the foot
  4. even distribution and even detail everywhere = noise                                 -> the shelf and the glade terrace are quiet
     surfaces; ferns only where there is a cause (rock foot, wet pocket)
  5. the glade has no composition                                                          -> a shallow terrace with a raised rim, the hero
     oak moved into the arrival sightline, the stone arc as a gate, the ring trees leaning outward (the quiet uncanny)
  6. lighting is a flat midday-ish key                                                     -> two reversible looks (low south sun with
     damp directional fog; overcast low-key) tested against production at every station
"""
import sys, os, json, math, random, zlib, struct
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ExteriorWorld_XR2_20261031'))
import xr3_places as PL, xr2_layout as LY

X2 = 'Saved/Codex/ExteriorWorld_XR2_20261031/design'; D3 = 'Saved/Codex/ExteriorIdentity_XR3_20261031'; RC = 'Saved/Codex/ExteriorRedesign_20261031/recon'
OX, OY, N = -50040.0, -50225.0, 1017; WATER = -100.0
H8 = np.fromfile(X2 + '/height_x8.u16', dtype='<u2').reshape(N, N)
Z8 = (H8.astype(np.float64) - 32768.0) * 100.0 / 128.0
F8 = json.load(open(X2 + '/foliage_full_x8.json')); SP8 = json.load(open(X2 + '/spawn_x8.json')); PLAN8 = json.load(open(X2 + '/plan_x8.json'))
LIB = json.load(open(D3 + '/recon/library.json'))['meshes']
rng = random.Random(4041); V = sys.argv[1] if len(sys.argv) > 1 else 'i4'
ROUTE = LY.ROUTE_A; SL = PL.SLICE; GC = (-900.0, 8750.0)


def bil(Zg, x, y):
    fx, fy = (x - OX) / 100.0, (y - OY) / 100.0; ix, iy = int(math.floor(fx)), int(math.floor(fy)); ax, ay = fx - ix, fy - iy
    return Zg[iy, ix] * (1 - ax) * (1 - ay) + Zg[iy, ix + 1] * ax * (1 - ay) + Zg[iy + 1, ix] * (1 - ax) * ay + Zg[iy + 1, ix + 1] * ax * ay


def inside(x, y, poly):
    c = False
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / ((by - ay) or 1e-9) + ax: c = not c
    return c


def dpoly(x, y, pts):
    b = 1e9
    for a, c in zip(pts, pts[1:]):
        vx, vy = c[0] - a[0], c[1] - a[1]; t = max(0, min(1, ((x - a[0]) * vx + (y - a[1]) * vy) / (vx * vx + vy * vy))); b = min(b, math.hypot(a[0] + t * vx - x, a[1] + t * vy - y))
    return b


def off_route(x, y, m=300):
    return dpoly(x, y, ROUTE) > m and dpoly(x, y, LY.CONNECT) > m and dpoly(x, y, LY.DESCENT) > m


ss = lambda a, b, v: np.clip((v - a) / (b - a), 0, 1) ** 2 * (3 - 2 * np.clip((v - a) / (b - a), 0, 1))

# ================================================================ terrain deltas (cm) on the x8 heightmap
LEDGE = [(3120, 3350), (3100, 3900), (3080, 4300), (3105, 4750), (3130, 5200), (3090, 5650), (3050, 6100)]        # strike of the bedrock ledge (= the XR2 ring there)
i0, i1 = int((-3500 - OX) / 100), int((4200 - OX) / 100) + 1; j0, j1 = int((1000 - OY) / 100), int((10200 - OY) / 100) + 1
xs = OX + np.arange(i0, i1) * 100.0; ys = OY + np.arange(j0, j1) * 100.0; X, Y = np.meshgrid(xs, ys)
Dl = np.zeros_like(X)


def seg_sd(x, y, pts):
    best = np.full(x.shape, 1e18); sgn = np.zeros(x.shape)
    for a, b in zip(pts, pts[1:]):
        vx, vy = b[0] - a[0], b[1] - a[1]; L2 = vx * vx + vy * vy
        t = np.clip(((x - a[0]) * vx + (y - a[1]) * vy) / L2, 0, 1); d = np.hypot(x - a[0] - vx * t, y - a[1] - vy * t)
        cr = vx * (y - a[1]) - vy * (x - a[0]); m = d < best; best = np.where(m, d, best); sgn = np.where(m, np.sign(cr), sgn)
    return best, sgn


d, sgn = seg_sd(X, Y, LEDGE)                      # strike runs south (+y): east (outside, x larger) has cr < 0
east = sgn < 0
# soil berm behind the ledge blocks: +110 cm from 60 cm to 250 cm east of the strike, fading by 600; a 25 cm toe apron inside
Dl += np.where(east, 110 * ss(0, 60, d) * (1 - ss(250, 600, d)), 25 * (1 - ss(0, 220, d))) * ss(0, .0, np.ones_like(d))
# glade terrace: rim +55 cm at r 560..760, interior blended flat (height of the centre), bank behind untouched
r = np.hypot(X - GC[0], Y - GC[1]); zc = bil(Z8, *GC)
Dl += 55 * ss(520, 600, r) * (1 - ss(700, 820, r))
flat_w = 0.75 * (1 - ss(380, 540, r)); Zr = Z8[j0:j1, i0:i1]
Dl += (zc - Zr) * flat_w
Z9 = Z8.copy(); Z9[j0:j1, i0:i1] = Zr + Dl
H9 = np.clip(np.round(Z9 * 128.0 / 100.0 + 32768.0), 0, 65535).astype('<u2')
H9 = np.where(np.abs(Z9 - Z8) < 0.5, H8, H9); Z9 = (H9.astype(np.float64) - 32768.0) * 100.0 / 128.0
zf = lambda x, y: bil(Z9, x, y)

# ---------------------------------------------------------------- write the x9 XR2 variant
H9.tofile(X2 + '/height_x9.u16')
hi, lo = (H9 >> 8).astype(np.uint8), (H9 & 255).astype(np.uint8); rgb = np.dstack([hi, lo, np.zeros_like(hi)])
raw = b''.join(b'\x00' + rgb[k].tobytes() for k in range(N)); ch = lambda t, dd: struct.pack('>I', len(dd)) + t + dd + struct.pack('>I', zlib.crc32(t + dd) & 0xffffffff)
open(X2 + '/height_x9.png', 'wb').write(b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', N, N, 8, 2, 0, 0, 0)) + ch(b'IDAT', zlib.compress(raw, 6)) + ch(b'IEND', b''))
dj, di = np.nonzero(np.abs(Z9 - Z8) > 1.0); samp = []
for _ in range(60):
    q = rng.randrange(len(dj)); samp.append({'x': int(di[q]), 'y': int(dj[q]), 'height': int(H9[dj[q], di[q]])})
for (x, y) in ((0, 0), (500, 500), (1016, 1016), (508, 508)):
    samp.append({'x': x, 'y': y, 'height': int(H9[y, x])})
plan9 = dict(PLAN8); plan9.update({'variant': 'x9', 'file': 'height_x9.png', 'samples': samp, 'xr4': {'ledge': LEDGE, 'glade': GC, 'changed': int(len(dj))}})
json.dump(plan9, open(X2 + '/plan_x9.json', 'w'), indent=1, default=str)
# foliage: regrounded on z9 (counts unchanged) -> foliage_x9 (changed comps) + foliage_full_x9
F9 = []; chg = []; n_reg = 0
for rec in F8:
    xf = [list(t) for t in rec['xf']]; changed = False
    for t in xf:
        dz = zf(t[0], t[1]) - bil(Z8, t[0], t[1])
        if abs(dz) > 0.5:
            t[2] = round(t[2] + dz, 1); changed = True; n_reg += 1
    F9.append(dict(rec, xf=xf))
    if changed: chg.append({'mesh': rec['mesh'], 'cull': rec['cull'], 'n': len(xf), 'xf_after': xf})
json.dump(chg, open(X2 + '/foliage_x9.json', 'w')); json.dump(F9, open(X2 + '/foliage_full_x9.json', 'w'))
SP9 = []
for s in SP8:
    s = dict(s); dz = zf(s['fx'], s['fy']) - bil(Z8, s['fx'], s['fy'])
    if abs(dz) > 0.5: s['z'] = round(s['z'] + dz, 1)
    SP9.append(s)
json.dump(SP9, open(X2 + '/spawn_x9.json', 'w'), indent=0)
json.dump(json.load(open(X2 + '/overlay_x8.json')), open(X2 + '/overlay_x9.json', 'w'))

# ================================================================ i4: masses, ledge, glade, quiet ground
P = {'C': '/Game/Calysto/World/Vegetation/Meshes/', 'PF': '/Game/PineForestPack/Meshes/', 'FC': '/Game/Fishermans_Cabin/Meshes/', 'E': '/Game/Environment_Set/Environment/Rocks/Models/'}
SPAWN = []; HIDE = []; st = {}


def ext(m): return LIB[m]['ext'], LIB[m]['org']


def spawn(kind, mesh, x, y, yaw, sc, sink, label, soft=False, z=None, pitch=0.0, roll=0.0, mid=None):
    (ex, ey, ez), (ox, oy, oz) = ext(mesh); gz = zf(x, y) if z is None else z
    rec = {'kind': kind, 'mesh': mesh, 'label': label, 'x': round(x, 1), 'y': round(y, 1), 'z': round(gz - (oz - ez) * sc - sink * 2 * ez * sc, 1), 'yaw': round(yaw, 1),
           'pitch': round(pitch, 2), 'roll': round(roll, 2), 'scale': [sc, sc, sc], 'soft': soft, 'camera_ignore': True}
    if mid: rec['mid'] = mid
    SPAWN.append(rec); return rec


def strike(s):
    cum = [0.0]
    for a, b in zip(LEDGE, LEDGE[1:]): cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    for k in range(len(LEDGE) - 1):
        if s <= cum[k + 1] or k == len(LEDGE) - 2:
            L = cum[k + 1] - cum[k]; t = (s - cum[k]) / L; a, b = LEDGE[k], LEDGE[k + 1]
            return a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]), math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])), cum[-1]


# 1. hero trunks (refuge frame + transition entry) - the biggest pine x1.3 = ~1 m trunk, 50 m crown
HERO = [(200, 2200), (2150, 3000), (1750, 4150), (1800, 6400)] if V != 'i4' else [(300, 2350), (1500, 2680), (1950, 3900), (2250, 6700)]
if V == 'i4':
    for k, (x, y) in enumerate(HERO):
        spawn('hero', P['PF'] + 'Trees/SM_PineTree04', x, y, rng.uniform(0, 360), 1.3, 0.0, 'XR4_Hero_%d' % k)
# 2. bedrock ledge: 9 overlapping grey blocks along the strike, common strike, buried 45 %; talus + moss + fern at the foot
s = 120.0; k = 0; L_total = strike(0)[3]
while s < L_total - 80:
    px, py, tyaw, _ = strike(s); nx, ny = math.cos(math.radians(tyaw + 90)), math.sin(math.radians(tyaw + 90))   # +90 = east (outside)
    m = 'SM_Big_Rock_01' if k % 3 != 1 else 'SM_Big_Rock_02'; sc = rng.uniform(1.75, 2.05)
    spawn('ledge', P['E'] + m, px + nx * 70, py + ny * 70, tyaw + rng.uniform(-6, 6), round(sc, 2), 0.45, 'XR4_Ledge_%02d' % k, z=zf(px + nx * 140, py + ny * 140))
    if k % 2 == 0:
        tx, ty = px - nx * rng.uniform(170, 260), py - ny * rng.uniform(0, 60)
        if off_route(tx, ty, 240):
            spawn('talus', P['E'] + 'SM_Middle_Rock_0%d' % rng.randint(1, 3), tx, ty, rng.uniform(0, 360), rng.uniform(1.2, 1.7), 0.35, 'XR4_Talus_%02d' % k)
    if V == 'i4':
        mx, my = px - nx * rng.uniform(120, 200), py - ny * rng.uniform(-80, 80)
        spawn('moss', P['PF'] + 'TerrainPatches/SM_GroundMossPatch0%d' % rng.randint(1, 3), mx, my, rng.uniform(0, 360), rng.uniform(0.8, 1.1), 0.3, 'XR4_LedgeMoss_%02d' % k, soft=True)
    if k % 3 == 2:
        fx_, fy_ = px - nx * 150, py - ny * rng.uniform(-60, 60)
        spawn('fern', P['PF'] + 'Plants/SM_FernLong01', fx_, fy_, rng.uniform(0, 360), rng.uniform(1.1, 1.4), 0.05, 'XR4_LedgeFern_%02d' % k, soft=True)
    k += 1; s += rng.uniform(300, 340)
st['ledge_blocks'] = k
for sp in SP8:                                                   # the XR2 single boulders on this stretch are hidden (collision stays)
    if sp['kind'] in ('ring_rock', 'ring_deadfall') and inside(sp['x'], sp['y'], SL) and 3200 < sp['y'] < 6300:
        HIDE.append(sp['label'])
# 3. dark spruce on the ledge top (enclosure above the shelf) + the inlet stand
for k, (x, y) in enumerate([(3420, 3600), (3600, 4000), (3450, 4500), (3650, 4900), (3480, 5300), (3620, 5750), (3400, 6050), (2500, 7250), (2750, 7420), (2300, 7500), (2650, 7700)]):
    spawn('spruce', P['C'] + 'SM_Black_Spruce_0%d' % rng.choice([2, 4, 5, 1]), x, y, rng.uniform(0, 360), rng.uniform(0.95, 1.2), 0.02, 'XR4_Spruce_%02d' % k)
# 4. glade: the stone arc (gate, radius 4.8 m, 9 stones, identical size, radial yaw), the back dead tree; moss floor
for i in range(9):
    a = math.radians(-70 + i * 17.5); x, y = GC[0] + 480 * math.cos(a), GC[1] + 480 * math.sin(a)
    spawn('uncanny', P['PF'] + 'Rocks/SM_PineStone02', x, y, math.degrees(a), 1.05, 0.42, 'XR4_StoneArc_%d' % i)
spawn('deadtree', P['C'] + 'SM_Dead_Tree_01', -550, 9420, 200, 1.0, 0.03, 'XR4_DeadTree_glade')
spawn('deadtree', P['C'] + 'SM_Dead_Tree_02', 3250, 4550, 20, 1.05, 0.03, 'XR4_DeadTree_shelf')
k = 0
for _ in (range(80) if V == 'i4' else []):
    x, y = GC[0] + rng.uniform(-620, 620), GC[1] + rng.uniform(-620, 620)
    if math.hypot(x - GC[0], y - GC[1]) < 600 and off_route(x, y, 160):
        spawn('moss', P['PF'] + 'TerrainPatches/SM_GroundMossPatch0%d' % rng.randint(1, 3), x, y, rng.uniform(0, 360), rng.uniform(0.9, 1.3), 0.35, 'XR4_GladeMoss_%02d' % k, soft=True); k += 1
        if k >= 14: break
# traces (kept from XR3)
spawn('trace', P['FC'] + 'Ropes/SM_Rope_Tire_01', 300, 2860, 70, 1.0, 0.0, 'XR4_Trace_RopeTire', soft=True)
spawn('trace', P['FC'] + 'Sticks/SM_Sticks_02', 760, 2520, -30, 1.1, 0.0, 'XR4_Trace_Sticks', soft=True)
spawn('trace', P['FC'] + 'Wheelbarrow/SM_Wheelbarrow', 1280, 1560, 160, 1.0, 0.0, 'XR4_Trace_Wheelbarrow')
st['spawn'] = {}
for s_ in SPAWN: st['spawn'][s_['kind']] = st['spawn'].get(s_['kind'], 0) + 1

# 5. foliage edits on the x9 lists: quiet shelf + quiet terrace, hero oak into the arrival sightline, ring trees leaning outward
FOL = []; st['foliage'] = {}
SHELF = lambda x, y: 3200 < y < 6500 and x < 3150 and dpoly(x, y, ROUTE) < 800
def lean(yaw, dx, dy, deg):
    c, s_ = math.cos(math.radians(-yaw)), math.sin(math.radians(-yaw)); lx, ly = dx * c - dy * s_, dx * s_ + dy * c
    return deg * lx, -deg * ly
for rec in F9:
    n = rec['mesh'].split('/')[-1]; keep = []; changed = False
    small = n.startswith(('SM_Grass', 'SM_GroundCover', 'SM_Fern', 'SM_DeadLeaves', 'wgxjfhr', 'tkwqbbofa', 'SM_Bush', 'SM_Young', 'SM_Pine_Juvenile', 'Pine_08'))
    big = n.startswith(('SM_PineTree', 'SM_Fir_Tree'))
    for t in rec['xf']:
        x, y = t[0], t[1]; r_ = math.hypot(x - GC[0], y - GC[1])
        if inside(x, y, SL):
            if n == 'SM_Oak_L_1' and r_ < 900:
                t = list(t); t[0], t[1] = -1450.0, 8480.0; t[2] = round(zf(-1450, 8480) + (t[2] - bil(Z8, x, y)), 1); keep.append(t); changed = True; continue
            if small and SHELF(x, y) and not (n.startswith('SM_Fern') and dpoly(x, y, LEDGE) < 260):
                if rng.random() < 0.88: changed = True; continue
            if small and r_ < 700:
                changed = True; continue
            if n.startswith('SM_Fir_Tree'):
                changed = True; spawn('pine_swap', P['PF'] + 'Trees/SM_PineTree07', x, y, t[4], t[6], 0.0, 'XR4_PineSwap_%d' % len(SPAWN)); continue
            if big and 650 < r_ < 1250:
                t = list(t); dx, dy = (x - GC[0]) / r_, (y - GC[1]) / r_; p, rl = lean(t[4], dx, dy, 7.0); t[3], t[5] = round(p, 2), round(rl, 2); changed = True
            if small and r_ < 1250 and rng.random() < 0.5:
                changed = True; continue
        keep.append(t)
    if V != 'i4' and n == 'SM_PineTree03' and rec['cull'][0] == 42000:
        for x, y in HERO:
            keep.append([float(x), float(y), round(zf(x, y) - 10.0, 1), 0.0, round(rng.uniform(0, 360), 2), 0.0, 1.4, 1.4, 1.4]); changed = True
    if changed:
        FOL.append({'mesh': rec['mesh'], 'cull': rec['cull'], 'xf_after': keep, 'n_before': len(rec['xf'])}); st['foliage'][n + ' ' + str(rec['cull'][0])] = (len(rec['xf']), len(keep))

# 6. materials: the XR3 i3 briefs + retints (one climate), unchanged
I3 = json.load(open(D3 + '/design/id_i3.json'))
json.dump({'variant': V, 'slice': SL, 'mats': I3['mats'], 'retint': I3['retint'], 'spawn': SPAWN, 'foliage': FOL, 'hide': HIDE, 'stats': st},
          open(D3 + '/design/id_%s.json' % V, 'w'), indent=0)
print('DESIGN x9/' + V, 'terrain changed', len(dj), 'regrounded', n_reg, 'ledge', st['ledge_blocks'], json.dumps(st['spawn']), 'hide', len(HIDE))
print('foliage', st['foliage'])
