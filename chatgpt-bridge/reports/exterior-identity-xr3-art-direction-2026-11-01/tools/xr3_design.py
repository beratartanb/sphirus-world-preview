"""xr3_design.py (offline, Blender Python + numpy): the identity pass design on top of the applied XR2 x8 world -> design/id_<var>.json.
usage: xr3_design.py <variant>
Four layers, all inside the vertical-slice polygon (route A: house -> landing -> rock shelf -> inlet -> far-shore glade):
  1. ONE CLIMATE: project-owned material instances re-tuned in memory (landscape layer colour offsets, owned fern / pine / rock MIs)
     and dynamic material instances on the XR2 structural rocks / deadwood (cool grey mineral family, grey-green moss, no neon, no orange).
  2. PLACE IDENTITY: per-place support masses with a cause (sedge in wet pockets, moss on the shaded side of rocks, litter under
     the dense stand, bog laurel on the open glade), standing dead trees inside the stands, a dark spruce stand at the inlet.
  3. LIVED-IN TRACES: landing (lamp post, rope, sticks), glade (the too-regular stone row = the quiet uncanny), house front (wheelbarrow).
  4. QUIET GROUND: grass carpets thinned in deep shade (removal is a design act).
Everything is reversible: foliage lists per component (restore = recon snapshot), XR3_* actors, material backups."""
import sys, os, json, math, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ExteriorWorld_XR2_20261031'))
import xr3_places as PL, xr2_layout as LY

V = sys.argv[1] if len(sys.argv) > 1 else 'i1'
R = 'Saved/Codex/ExteriorRedesign_20261031/recon'; X2 = 'Saved/Codex/ExteriorWorld_XR2_20261031/design'; D = 'Saved/Codex/ExteriorIdentity_XR3_20261031'
OX, OY, N = -50040.0, -50225.0, 1017; WATER = -100.0
Z = (np.fromfile(X2 + '/height_x8.u16', dtype='<u2').reshape(N, N).astype(np.float64) - 32768.0) * 100.0 / 128.0
F = json.load(open(X2 + '/foliage_full_x8.json')); X2SP = json.load(open(X2 + '/spawn_x8.json'))
LIB = json.load(open(D + '/recon/library.json'))['meshes']
rng = random.Random(3031)


def zf(x, y):
    fx, fy = (x - OX) / 100.0, (y - OY) / 100.0; ix, iy = int(math.floor(fx)), int(math.floor(fy)); ax, ay = fx - ix, fy - iy
    return Z[iy, ix] * (1 - ax) * (1 - ay) + Z[iy, ix + 1] * ax * (1 - ay) + Z[iy + 1, ix] * (1 - ax) * ay + Z[iy + 1, ix + 1] * ax * ay


def slope(x, y):
    return math.degrees(math.atan(math.hypot(zf(x + 100, y) - zf(x - 100, y), zf(x, y + 100) - zf(x, y - 100)) / 200))


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


ROUTE = LY.ROUTE_A; SL = PL.SLICE
big = [t for r in F for t in r['xf'] if any(r['mesh'].split('/')[-1].startswith(b) for b in ('SM_PineTree', 'SM_Fir_Tree', 'SM_Oak'))]
rocks = [s for s in X2SP if s['kind'] in ('ring_rock', 'r6_outcrop', 'inner_rock') and inside(s['x'], s['y'], SL)]


def canopy(x, y, r=700):
    return sum(1 for t in big if abs(t[0] - x) < r and abs(t[1] - y) < r and math.hypot(t[0] - x, t[1] - y) < r)


# ------------------------------------------------------------------ 1. one climate: material briefs
MATS = {
    '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_Integration_Valley': {
        'vector': {'Forest Color Offset': [0.20, 0.235, 0.185, 1.0], 'Grass Color Offset': [0.40, 0.47, 0.37, 1.0], 'Cliff Color Offset': [0.45, 0.50, 0.53, 1.0],
                   'Sand Color Offset': [0.17, 0.155, 0.13, 1.0]},
        'scalar': {'Macro Variation Contrast': 0.28}},
    '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_PR_FernLong01': {'scalar': {'Saturation': 0.46, 'Brightness': 0.40}},
    '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_PR_FernWild01': {'scalar': {'Saturation': 0.46, 'Brightness': 0.40}},
    '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_PR_PineTree01_FO': {'scalar': {'Saturation': 0.56}, 'vector': {'Albedo_Tint': [0.56, 0.60, 0.55, 1.0]}},
    '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_PR_PineTree03_FO': {'scalar': {'Saturation': 0.56}, 'vector': {'Albedo_Tint': [0.56, 0.60, 0.55, 1.0]}},
    '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_PR_PineTree05_FO': {'scalar': {'Saturation': 0.56}, 'vector': {'Albedo_Tint': [0.56, 0.60, 0.55, 1.0]}},
    '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_RefugeGroundRock03': {'scalar': {'Albedo_Brightness': 0.40}, 'vector': {'Color_Tint': [0.60, 0.65, 0.70, 1.0], 'Moss_ColorTint': [0.20, 0.27, 0.15, 1.0]}},
    '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_Refuge_Pine_Juvenile_FO': {'scalar': {'Saturation': 0.5}, 'vector': {'Albedo_Tint': [0.52, 0.58, 0.52, 1.0]}},
    '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_RefugeFirLeaves': {'vector': {'Color Multiply': [0.40, 0.53, 0.46, 1.0]}, 'scalar': {'Saturation': 0.62}},
}
ROCK_MID = {'scalar': {'Albedo_Brightness': 0.55, 'Moss_Opacity': 0.72, 'WorldBlendMax': 0.55, 'Moss_FuzzyEdgeBrightness': 0.6, 'Moss_FuzzyPower': 1.4, 'Moss_Roughness': 3.0, 'Blend_Normal': 1.0},
            'vector': {'Color_Tint': [0.60, 0.66, 0.72, 1.0], 'Moss_ColorTint': [0.21, 0.29, 0.16, 1.0]}}
WOOD_MID = {'scalar': {'Albedo_Brightness': 0.5, 'Moss_Opacity': 0.6, 'WorldBlendMax': 0.45, 'Saturation': 0.9},
            'vector': {'Color_Tint': [0.62, 0.60, 0.56, 1.0], 'Moss_ColorTint': [0.21, 0.29, 0.16, 1.0]}}
RETINT = [{'prefix': p, 'mid': ROCK_MID} for p in ('XR2_RingRock_', 'XR2_Outcrop_', 'XR2_W1_Rock_', 'XR2_W0_Bank_', 'XR2_Landmark_glade_seat', 'XR2_Landmark_saddle_seat')] + \
         [{'prefix': p, 'mid': WOOD_MID} for p in ('XR2_Windthrow_', 'XR2_Log_', 'XR2_RingDeadfall_', 'XR2_W0_Deadfall_', 'XR2_W1_Deadfall_')]

# ------------------------------------------------------------------ 2+3. place identity and traces (XR3 actors)
SPAWN = []; stats = {}
P = {'Calysto': '/Game/Calysto/World/Vegetation/Meshes/', 'PF': '/Game/PineForestPack/Meshes/', 'FC': '/Game/Fishermans_Cabin/Meshes/'}


def ext(mesh):
    return LIB[mesh]['ext'], LIB[mesh]['org']


def spawn(kind, mesh, x, y, yaw, sc, sink, label, soft=False, z=None, mid=None, pitch=0.0, roll=0.0):
    (ex, ey, ez), (ox, oy, oz) = ext(mesh)
    gz = zf(x, y) if z is None else z
    pz = gz - (oz - ez) * sc - sink * 2 * ez * sc
    rec = {'kind': kind, 'mesh': mesh, 'label': label, 'x': round(x, 1), 'y': round(y, 1), 'z': round(pz, 1), 'yaw': round(yaw, 1), 'pitch': pitch, 'roll': roll,
           'scale': [sc, sc, sc], 'soft': soft, 'camera_ignore': True}
    if mid: rec['mid'] = mid
    SPAWN.append(rec); return rec


def free_of_route(x, y, m=300):
    return dpoly(x, y, ROUTE) > m and dpoly(x, y, LY.CONNECT) > m and dpoly(x, y, LY.DESCENT) > m


# P1 landing: lived-in traces + wet pocket
if V == 'i1': spawn('trace', P['FC'] + 'Lamps/SM_Lamp_02', 420, 2740, 20, 1.0, 0.0, 'XR3_Trace_LampPost')
spawn('trace', P['FC'] + 'Ropes/SM_Rope_Tire_01', 300, 2860, 70, 1.0, 0.0, 'XR3_Trace_RopeTire', soft=True)
spawn('trace', P['FC'] + 'Sticks/SM_Sticks_02', 760, 2520, -30, 1.1, 0.0, 'XR3_Trace_Sticks', soft=True)
spawn('trace', P['FC'] + 'Wheelbarrow/SM_Wheelbarrow', 1280, 1560, 160, 1.0, 0.0, 'XR3_Trace_Wheelbarrow')
k = 0
for x, y in [(80, 3080), (160, 3180), (-40, 3140), (240, 3260), (-120, 3230), (420, 3300), (60, 3340), (300, 3400), (-200, 3330)]:   # landing west pocket: wet sedge
    if zf(x, y) > WATER - 20:
        spawn('sedge', P['Calysto'] + 'SM_Grass_Sedge_Clump_0%d' % rng.randint(1, 4), x, y, rng.uniform(0, 360), rng.uniform(1.0, 1.4), 0.05, 'XR3_Sedge_L%02d' % k, soft=True); k += 1
# P2 rock shelf: moss on the shaded (north / water) side of each big rock, ferns already there; one standing dead tree in the stand
for i, s in enumerate(rocks):
    for j in range(2):
        a = math.radians(s['yaw'] + 90 + rng.uniform(-40, 40)); r_ = s['hy'] * 0.9 + rng.uniform(40, 140)
        x, y = s['x'] + math.cos(a) * r_, s['y'] + math.sin(a) * r_
        if zf(x, y) > WATER + 10 and free_of_route(x, y, 200):
            spawn('moss', P['PF'] + 'TerrainPatches/SM_GroundMossPatch0%d' % rng.randint(1, 3), x, y, rng.uniform(0, 360), rng.uniform(0.7, 1.0), 0.25, 'XR3_Moss_R%02d_%d' % (i, j), soft=True)
for x, y, yaw in [(3250, 4550, 20), (3050, 6050, 140)]:
    spawn('deadtree', P['Calysto'] + 'SM_Dead_Tree_02', x, y, yaw, 1.05, 0.03, 'XR3_DeadTree_%d' % int(y))
# inlet: dark spruce stand on wet ground + sedge in the inlet mouth
k = 0
for x, y in [(2500, 7250), (2750, 7420), (2300, 7500), (2650, 7700), (2950, 7150), (2450, 7900)]:
    if free_of_route(x, y, 350) and zf(x, y) > WATER + 10:
        spawn('spruce', P['Calysto'] + 'SM_Black_Spruce_0%d' % rng.choice([1, 3, 4, 5]), x, y, rng.uniform(0, 360), rng.uniform(0.9, 1.15), 0.02, 'XR3_Spruce_%02d' % k); k += 1
k = 0
for x, y in [(1950, 7100), (1800, 7250), (2100, 7250), (1700, 7400), (2000, 7400), (1850, 7550), (2200, 7050), (1600, 7600)]:
    if zf(x, y) > WATER - 20 and dpoly(x, y, ROUTE) > 180:
        spawn('sedge', P['Calysto'] + 'SM_Grass_Sedge_Clump_0%d' % rng.randint(1, 4), x, y, rng.uniform(0, 360), rng.uniform(1.0, 1.4), 0.05, 'XR3_Sedge_I%02d' % k, soft=True); k += 1
# P3 glade: bog laurel + bunchberry on the open ground, the too-regular stone row, a dead tree on the back
k = 0
for _ in range(40):
    x, y = rng.uniform(-1900, 200), rng.uniform(8350, 9150)
    if zf(x, y) > WATER + 15 and free_of_route(x, y, 170) and math.hypot(x + 1250, y - 9050) > 260 and canopy(x, y, 500) == 0:
        m = P['Calysto'] + (('SM_BogLaurelClump' if V == 'i1' else 'SM_MossPatch_01' if V == 'i2' else 'SM_Bunchberry_0%d' % rng.randint(1, 6)) if rng.random() < 0.5 else 'SM_Bunchberry_0%d' % rng.randint(1, 6))
        spawn('glade', m, x, y, rng.uniform(0, 360), rng.uniform(1.0, 1.5), 0.02, 'XR3_Glade_%02d' % k, soft=True); k += 1
for i in range(7):   # the stone row: 7 stones, 1.3 m apart, half buried, all the same size - older than the house, too regular for nature
    x, y = -1750 + i * 128, 8520 - i * 24
    spawn('uncanny', P['PF'] + 'Rocks/SM_PineStone02', x, y, 12.0 + i * 0.5, 0.9, 0.45, 'XR3_StoneRow_%d' % i)
spawn('deadtree', P['Calysto'] + 'SM_Dead_Tree_01', -600, 9400, 200, 1.0, 0.03, 'XR3_DeadTree_glade')
# canopy litter under the shelf stand (sheltered pockets, not a carpet)
k = 0
for _ in range(60):
    x, y = rng.uniform(2800, 3500), rng.uniform(3400, 6400)
    if zf(x, y) > WATER + 10 and free_of_route(x, y, 230) and canopy(x, y, 600) >= 2 and slope(x, y) < 30:
        spawn('litter', P['PF'] + 'TerrainPatches/SM_PineGroundPatch0%d' % rng.randint(1, 6), x, y, rng.uniform(0, 360), rng.uniform(0.8, 1.2), 0.3, 'XR3_Litter_%02d' % k, soft=True); k += 1
        if k >= 14: break
HIDE = []
if V != 'i1':
    # the warm olive CliffRock family is replaced inside the slice by the cool grey Environment_Set rocks (same place, same footprint
    # class); the XR2 actor keeps its collision and is hidden, so the circulation evidence of XR2 stays valid
    E_ = '/Game/Environment_Set/Environment/Rocks/Models/'
    for i, s_ in enumerate(rocks):
        HIDE.append(s_['label'])
        m = rng.choice(['SM_Big_Rock_01', 'SM_Big_Rock_02', 'SM_Big_Rock_01', 'SM_Big_Rock_03'])
        (ex, ey, ez), (ox, oy, oz) = ext(E_ + m); sc = max(s_['hx'] / max(ex, ey), s_['hy'] / min(ex, ey)) * 0.95; sc = max(1.1, min(2.4 if V == 'i2' else 1.7, sc))
        spawn('rock_swap', E_ + m, s_['x'], s_['y'], s_['yaw'] + rng.uniform(-10, 10), round(sc, 2), 0.22 if V == 'i2' else 0.38, 'XR3_RockSwap_%02d' % i, z=zf(s_['x'], s_['y']) - (30 if V == 'i2' else 90))
        # a second, smaller rock of the same family at its toe (a formation, not a single prop)
        a = math.radians(s_['yaw'] - 90 + rng.uniform(-30, 30)); x2, y2 = s_['x'] + math.cos(a) * (s_['hy'] + 150), s_['y'] + math.sin(a) * (s_['hy'] + 150)
        if free_of_route(x2, y2, 260) and zf(x2, y2) > WATER + 10:
            spawn('rock_swap', E_ + 'SM_Middle_Rock_0%d' % rng.randint(1, 3), x2, y2, rng.uniform(0, 360), rng.uniform(1.3, 1.9), 0.3, 'XR3_RockToe_%02d' % i)
    for x, y in [(3350, 3900), (3550, 4300), (3400, 5200), (3600, 5700)]:
        if free_of_route(x, y, 350):
            spawn('spruce', P['Calysto'] + 'SM_Black_Spruce_0%d' % rng.choice([2, 4, 5]), x, y, rng.uniform(0, 360), rng.uniform(1.0, 1.2), 0.02, 'XR3_Spruce_S%d' % int(y))
stats['spawn'] = {}
for s in SPAWN: stats['spawn'][s['kind']] = stats['spawn'].get(s['kind'], 0) + 1

# ------------------------------------------------------------------ 4. quiet ground: thin carpets in deep shade, swap the 3 firs
FOL = []
for r in F:
    n = r['mesh'].split('/')[-1]; keep = []; changed = False
    for t in r['xf']:
        x, y = t[0], t[1]
        if inside(x, y, SL):
            if n.startswith('SM_Fir_Tree'):
                changed = True; spawn('pine_swap', P['PF'] + 'Trees/SM_PineTree07', x, y, t[4], t[6], 0.0, 'XR3_PineSwap_%d' % len(SPAWN)); continue
            if n in ('SM_GrassSmall01', 'SM_GrassMedium01', 'SM_GroundCover01', 'SM_GroundCover03') and dpoly(x, y, ROUTE) > 350 and canopy(x, y, 700) >= 2 and rng.random() < 0.55:
                changed = True; continue
        keep.append(t)
    if changed:
        FOL.append({'mesh': r['mesh'], 'cull': r['cull'], 'xf_after': keep, 'n_before': len(r['xf'])})
stats['foliage'] = {f['mesh'].split('/')[-1]: (f['n_before'], len(f['xf_after'])) for f in FOL}
stats['hide'] = len(HIDE)
json.dump({'variant': V, 'slice': SL, 'mats': MATS, 'retint': RETINT, 'spawn': SPAWN, 'foliage': FOL, 'hide': HIDE, 'stats': stats}, open('%s/design/id_%s.json' % (D, V), 'w'), indent=0)
print('DESIGN', V, json.dumps(stats))
