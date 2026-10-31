"""vmp_spec.py <area_probe.json> <out trial_spec.json> : Environment Visual Master Pass trial layout (offline, deterministic).
Authored rear trail (design_terrain.py TRAIL), arc 16.0-60.5 m (~44 m). lat > 0 = right of travel = uphill bank (area_probe: R300 +0.7..+2.1 m).
Only EXISTING project assets. Placement is in the trail frame; z is resolved on the landscape by vmp_build.py (dz < 0 = sunk).
Zones (arc cm):
  Z0 1600-2100 house side    : tread decals only (house/yard untouched)
  Z1 2100-3300 rear threshold: tread; large rock on the uphill side at the bend (gate with the existing fence/woodpile on the left);
                               ground-patch roots at the tread edges; leaf decal on the bend's outer edge
  Z2 3300-4300 climb         : root steps across the tread where the grade is steepest; mossy roots along the bank toe; soil/litter
                               transition decals on the left
  Z3 4300-5100 compression   : rocky cut bank on the right (rock group + embankment), fern groups at the bank toe (large-medium-small),
                               fallen trunk on the downhill left as a frame / leading line
  Z4 5100-6000 release       : natural opening kept; downhill anchor rock, stump on the uphill edge, soil/leaf transitions, small fern
                               groups and litter at the edges
Obstacles (collision trees/rocks, house actors) are avoided by sliding an item outward in 40 cm steps (max 6)."""
import sys, json, math, random

area = json.load(open(sys.argv[1])); OUT = sys.argv[2]
rnd = random.Random(1031)
TRAIL = [(1950, 2110), (2300, 1850), (2560, 1300), (2520, 750), (2580, 250), (2790, -250), (3010, -760), (2930, -1260),
         (3110, -1800), (3080, -2300), (2780, -2800), (2350, -3340)]
seg = [0.0]
for a, b in zip(TRAIL, TRAIL[1:]):
    seg.append(seg[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))


def frame(s):
    for i in range(len(TRAIL) - 1):
        if s <= seg[i + 1] or i == len(TRAIL) - 2:
            L = seg[i + 1] - seg[i]; t = (s - seg[i]) / L; a, b = TRAIL[i], TRAIL[i + 1]
            tx, ty = (b[0] - a[0]) / L, (b[1] - a[1]) / L
            return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])), math.degrees(math.atan2(ty, tx)), (-ty, tx)


OBST = [(o['xy'][0], o['xy'][1], o['r']) for o in area['obstacles'] if o.get('r', 0) < 2000]
P = {'dirt1': '/Game/Modular_Rural_Cabin/Materials/Decals/Dirt_Track_1.Dirt_Track_1', 'dirt2': '/Game/Modular_Rural_Cabin/Materials/Decals/Dirt_Track_2.Dirt_Track_2',
     'ground': '/Game/Modular_Rural_Cabin/Materials/Decals/Forest_Ground.Forest_Ground', 'leaves': '/Game/Modular_Rural_Cabin/Materials/Decals/Scattered_Leaves.Scattered_Leaves',
     'rock3': '/Game/PineForestPack/Meshes/Cliffs/SM_PineGroundRock03.SM_PineGroundRock03', 'rock5': '/Game/PineForestPack/Meshes/Cliffs/SM_PineGroundRock05.SM_PineGroundRock05',
     'rock1': '/Game/PineForestPack/Meshes/Cliffs/SM_PineGroundRock01.SM_PineGroundRock01', 'stone1': '/Game/PineForestPack/Meshes/Rocks/SM_PineStone01.SM_PineStone01',
     'stone2': '/Game/PineForestPack/Meshes/Rocks/SM_PineStone02.SM_PineStone02', 'emb': '/Game/PineForestPack/Meshes/Cliffs/SM_ForestEmbankment01.SM_ForestEmbankment01',
     'trunk1': '/Game/PineForestPack/Meshes/TerrainPatches/SM_PineDeadTrunk01.SM_PineDeadTrunk01', 'stump2': '/Game/PineForestPack/Meshes/TerrainPatches/SM_TreeStump02.SM_TreeStump02',
     'root4': '/Game/OakForestEnv/Meshes/ScanAssets/SM_Root_4.SM_Root_4',
     'mossroots': '/Game/Fab/Megascans/3D/Mossy_Forest_Roots_wgxjfhr/High/wgxjfhr_tier_1/StaticMeshes/wgxjfhr_tier_1.wgxjfhr_tier_1',
     'patchroot': '/Game/Fab/Megascans/3D/Nordic_Forest_Ground_Patch_Root_tkwqbbofa/High/tkwqbbofa_tier_1/StaticMeshes/tkwqbbofa_tier_1.tkwqbbofa_tier_1',
     'branch': '/Game/PineForestPack/Meshes/DeadLeaves/SM_DeadBranch01.SM_DeadBranch01', 'stones': '/Game/PineForestPack/Meshes/Rocks/SM_SmallStones01.SM_SmallStones01',
     'fernL': '/Game/PineForestPack/Meshes/Plants/SM_FernLong01.SM_FernLong01', 'fernW': '/Game/PineForestPack/Meshes/Plants/SM_FernWild01.SM_FernWild01',
     'fern2': '/Game/PineForestPack/Meshes/Plants/SM_Fern02.SM_Fern02', 'fernWide': '/Game/PineForestPack/Meshes/Plants/SM_FernWide_01.SM_FernWide_01',
     'fern3': '/Game/PineForestPack/Meshes/Plants/SM_Fern03.SM_Fern03'}
items = []


def place(label, key, s, lat, kind='mesh', dz=0.0, dyaw=0.0, scale=1.0, size=None, avoid=0.0, pitch=0.0, roll=0.0, sort=None, depth=60.0):
    (x, y), yaw, n = frame(s); moved = 0
    px, py = x + n[0] * lat, y + n[1] * lat
    if avoid > 0:
        for k in range(6):
            hit = [o for o in OBST if math.hypot(px - o[0], py - o[1]) < o[2] + avoid]
            if not hit:
                break
            step = 40 if lat >= 0 else -40
            px, py = px + n[0] * step, py + n[1] * step; moved += 1
    it = {'label': label, 'asset': P[key], 'kind': kind, 'xy': [round(px, 1), round(py, 1)], 'yaw': round(yaw + dyaw, 1), 'dz': dz, 's_arc': s, 'lat': lat, 'avoid_steps': moved}
    if kind == 'mesh':
        it['scale'] = [scale, scale, scale] if isinstance(scale, (int, float)) else scale; it['pitch'] = pitch; it['roll'] = roll
    else:
        it['size'] = size; it['depth'] = depth
        if sort is not None:
            it['sort'] = sort
    items.append(it)


# --- tread: compacted soil decals, staggered, every ~2.6 m, interrupted (every 5th skipped), alternating sources
s, k = 1600.0, 0
while s < 6000:
    if k % 5 != 4:
        place('tread_%02d' % k, 'dirt1' if k % 2 else 'dirt2', s + rnd.uniform(-30, 30), rnd.uniform(-18, 18), kind='decal', dyaw=rnd.uniform(-8, 8),
              size=[330 + rnd.uniform(-30, 30), 150 + rnd.uniform(-20, 25)], sort=1, depth=90)
    s += 260; k += 1
# --- Z1 rear threshold (bend at vertex 6, arc 3197)
place('Z1_gate_rock', 'rock3', 3150, 330, dz=-55, dyaw=25, scale=1.0, avoid=150)
place('Z1_gate_stone', 'stone1', 3330, 210, dz=-25, dyaw=-40, scale=0.8, avoid=60)
place('Z1_patchroot_a', 'patchroot', 2950, 130, dz=-3, dyaw=30, scale=1.3)
place('Z1_patchroot_b', 'patchroot', 3420, -140, dz=-3, dyaw=-60, scale=1.2)
place('Z1_leaves_outer', 'leaves', 3200, -190, kind='decal', dyaw=15, size=[380, 260], sort=2)
place('Z1_fern_a1', 'fernL', 3050, 175, dz=-4, dyaw=40, avoid=40); place('Z1_fern_a2', 'fern2', 2990, 140, dz=-2, dyaw=100); place('Z1_fern_a3', 'fern3', 3110, 130, dz=-2)
# --- Z2 climb
for i, ss in enumerate((3620, 3960, 4240)):
    place('Z2_rootstep_%d' % i, 'root4', ss, rnd.uniform(-15, 15), dz=-9, dyaw=90 + rnd.uniform(-12, 12), scale=0.85)
place('Z2_mossroots_a', 'mossroots', 3520, 175, dz=-12, dyaw=8, scale=0.9, avoid=60)
place('Z2_mossroots_b', 'mossroots', 4120, 185, dz=-12, dyaw=-6, scale=1.0, avoid=60)
place('Z2_ground_l1', 'ground', 3750, -200, kind='decal', dyaw=20, size=[420, 300], sort=0)
place('Z2_ground_l2', 'ground', 4180, -230, kind='decal', dyaw=-30, size=[380, 280], sort=0)
place('Z2_branch', 'branch', 3880, -120, dz=-1, dyaw=55)
# --- Z3 compression: rocky cut bank + fern toe + fallen trunk frame
place('Z3_bank_rock5', 'rock5', 4500, 300, dz=-50, dyaw=10, scale=1.1, avoid=120)
place('Z3_bank_emb', 'emb', 4700, 380, dz=-120, dyaw=0, scale=[1.0, 1.0, 1.1], avoid=150)
place('Z3_bank_rock1', 'rock1', 4920, 320, dz=-55, dyaw=-15, scale=0.9, avoid=120)
place('Z3_toe_stone_a', 'stone2', 4620, 165, dz=-14, dyaw=70, scale=0.9)
place('Z3_toe_stone_b', 'stone2', 4980, 175, dz=-16, dyaw=-20, scale=0.7)
for g, (ss, lat) in enumerate(((4560, 150), (4860, 160))):
    place('Z3_ferngrp%d_L' % g, 'fernL', ss, lat + 25, dz=-4, dyaw=rnd.uniform(0, 360), scale=1.15)
    place('Z3_ferngrp%d_W1' % g, 'fernW', ss + 70, lat + 10, dz=-3, dyaw=rnd.uniform(0, 360))
    place('Z3_ferngrp%d_W2' % g, 'fernW', ss - 60, lat + 40, dz=-3, dyaw=rnd.uniform(0, 360), scale=0.9)
    place('Z3_ferngrp%d_s1' % g, 'fern2', ss + 120, lat - 15, dz=-2, dyaw=rnd.uniform(0, 360))
    place('Z3_ferngrp%d_s2' % g, 'fern3', ss - 110, lat - 10, dz=-2, dyaw=rnd.uniform(0, 360))
place('Z3_fallen_trunk', 'trunk1', 4950, -280, dz=-14, dyaw=-25, avoid=80)
place('Z3_fern_left', 'fernWide', 4800, -170, dz=-3, dyaw=30)
place('Z3_leaves_left', 'leaves', 4870, -230, kind='decal', dyaw=-25, size=[420, 260], sort=2)
# --- Z4 release: opening with anchors and transitions
place('Z4_anchor_rock', 'rock1', 5620, -380, dz=-45, dyaw=35, scale=0.95, avoid=120)
place('Z4_stump', 'stump2', 5360, 270, dz=-12, dyaw=140, scale=0.85, avoid=80)
place('Z4_ground_a', 'ground', 5450, -260, kind='decal', dyaw=10, size=[520, 360], sort=0)
place('Z4_ground_b', 'ground', 5800, -300, kind='decal', dyaw=-40, size=[460, 320], sort=0)
place('Z4_leaves_r', 'leaves', 5520, 190, kind='decal', dyaw=60, size=[360, 240], sort=2)
place('Z4_fern_a1', 'fernW', 5280, -150, dz=-3, dyaw=10); place('Z4_fern_a2', 'fern2', 5220, -110, dz=-2, dyaw=200); place('Z4_fern_a3', 'fern3', 5340, -125, dz=-2)
place('Z4_fern_b1', 'fernL', 5790, 165, dz=-4, dyaw=80); place('Z4_fern_b2', 'fern2', 5860, 140, dz=-2, dyaw=10)
place('Z4_stones', 'stones', 5700, 115, dz=-6, dyaw=30, scale=0.7)
place('Z4_branch', 'branch', 5450, -125, dz=-1, dyaw=-20)
spec = {'trail_source': 'Tools/AAAPolishRear20260923/design_terrain.py TRAIL', 'arc_cm': [1600, 6047], 'items': items,
        'counts': {'decals': sum(1 for i in items if i['kind'] == 'decal'), 'meshes': sum(1 for i in items if i['kind'] == 'mesh')}}
json.dump(spec, open(OUT, 'w'), indent=1)
print('TRIAL_SPEC items %d %s avoid-moved %d' % (len(items), spec['counts'], sum(1 for i in items if i['avoid_steps'])))
