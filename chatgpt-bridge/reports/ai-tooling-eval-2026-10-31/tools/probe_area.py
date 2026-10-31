"""probe_area.py (measure, read-only): facts for laying out the VMP trial on the authored rear trail, arc 16.0-60.5 m.
- every 1 m: centreline xy + landscape z, and landscape z at +-1.5 / +-3 / +-6 m on the right normal (uphill side / bank height)
- obstacles within 10 m of the centreline: collision-enabled foliage instances (trees, rocks, trunks) with radius; static-mesh actors
  (house, props) with bounds radius
- local bounds (cm) of the candidate meshes and decal materials' existence
Output: <VMP>/area_probe.json"""
import unreal as u, json, os, math

VMP = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\vmp'
TRAIL = [(1950, 2110), (2300, 1850), (2560, 1300), (2520, 750), (2580, 250), (2790, -250), (3010, -760), (2930, -1260),
         (3110, -1800), (3080, -2300), (2780, -2800), (2350, -3340)]
S_A, S_B = 1600.0, 6047.0
MESHES = ['/Game/PineForestPack/Meshes/Cliffs/SM_ForestEmbankment01', '/Game/PineForestPack/Meshes/Cliffs/SM_PineGroundRock03', '/Game/PineForestPack/Meshes/Cliffs/SM_PineGroundRock05',
          '/Game/PineForestPack/Meshes/Cliffs/SM_PineGroundRock01', '/Game/PineForestPack/Meshes/Rocks/SM_PineStone02', '/Game/PineForestPack/Meshes/Rocks/SM_PineStone01',
          '/Game/PineForestPack/Meshes/TerrainPatches/SM_PineDeadTrunk03', '/Game/PineForestPack/Meshes/TerrainPatches/SM_PineDeadTrunk01', '/Game/PineForestPack/Meshes/TerrainPatches/SM_PineDeadTrunk02',
          '/Game/PineForestPack/Meshes/TerrainPatches/SM_TreeStump02', '/Game/OakForestEnv/Meshes/ScanAssets/SM_Root_4',
          '/Game/Fab/Megascans/3D/Mossy_Forest_Roots_wgxjfhr/High/wgxjfhr_tier_1/StaticMeshes/wgxjfhr_tier_1',
          '/Game/Fab/Megascans/3D/Nordic_Forest_Ground_Patch_Root_tkwqbbofa/High/tkwqbbofa_tier_1/StaticMeshes/tkwqbbofa_tier_1',
          '/Game/PineForestPack/Meshes/DeadLeaves/SM_DeadBranch01', '/Game/PineForestPack/Meshes/DeadLeaves/SM_DeadLeaves02', '/Game/PineForestPack/Meshes/Rocks/SM_SmallStones01',
          '/Game/PineForestPack/Meshes/Plants/SM_Fern02', '/Game/PineForestPack/Meshes/Plants/SM_FernWild01', '/Game/PineForestPack/Meshes/Plants/SM_FernLong01',
          '/Game/PineForestPack/Meshes/Plants/SM_FernWide_01', '/Game/PineForestPack/Meshes/Plants/SM_Fern03', '/Game/PineForestPack/Meshes/GroundCover/SM_GroundCover01',
          '/Game/PineForestPack/Meshes/GroundCover/SM_GroundCover03']
DECALS = ['/Game/Modular_Rural_Cabin/Materials/Decals/Dirt_Track_1', '/Game/Modular_Rural_Cabin/Materials/Decals/Dirt_Track_2', '/Game/Modular_Rural_Cabin/Materials/Decals/Forest_Ground',
          '/Game/Modular_Rural_Cabin/Materials/Decals/Scattered_Leaves', '/Game/Modular_Rural_Cabin/Materials/Decals/Dirt_Track_Gradient']
world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
actors = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
IFA = [a for a in actors if a.get_class().get_name() == 'InstancedFoliageActor']
seg = [0.0]
for a, b in zip(TRAIL, TRAIL[1:]):
    seg.append(seg[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))


def frame(s):
    for i in range(len(TRAIL) - 1):
        if s <= seg[i + 1] or i == len(TRAIL) - 2:
            L = seg[i + 1] - seg[i]; t = (s - seg[i]) / L; a, b = TRAIL[i], TRAIL[i + 1]
            tx, ty = (b[0] - a[0]) / L, (b[1] - a[1]) / L
            return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])), (tx, ty), (-ty, tx)


def ground(x, y):
    ign = list(IFA)
    for _ in range(12):
        t = u.SystemLibrary.line_trace_single(world, u.Vector(x, y, 6000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, ign, u.DrawDebugTrace.NONE, True).to_tuple()
        if not t[0] or t[9] is None:
            return None
        if t[9].get_class().get_name() == 'Landscape':
            return round(t[4].z, 1)
        ign.append(t[9])
    return None


rows = []
s = S_A
while s <= S_B + 1:
    (x, y), t, n = frame(s); r = {'s_arc': round(s), 'xy': [round(x, 1), round(y, 1)], 'tan': [round(t[0], 4), round(t[1], 4)], 'z': ground(x, y)}
    for d in (150, 300, 600):
        r['zR%d' % d] = ground(x + n[0] * d, y + n[1] * d); r['zL%d' % d] = ground(x - n[0] * d, y - n[1] * d)
    rows.append(r); s += 100
pts = [r['xy'] for r in rows]


def dmin(x, y):
    return min(math.hypot(x - p[0], y - p[1]) for p in pts)


obst = []
for a in IFA:
    for c in a.get_components_by_class(u.InstancedStaticMeshComponent):
        m = c.get_editor_property('static_mesh')
        if not m or not str(c.get_collision_enabled()).split('.')[-1].startswith('QUERY'):
            continue
        b = m.get_bounds(); rr = max(b.box_extent.x, b.box_extent.y)
        for i in range(c.get_instance_count()):
            tr = c.get_instance_transform(i, True); L = tr.translation
            if dmin(L.x, L.y) <= 1000:
                obst.append({'mesh': m.get_name(), 'xy': [round(L.x), round(L.y)], 'r': round(rr * max(tr.scale3d.x, tr.scale3d.y))})
for a in actors:
    if a.get_class().get_name() in ('StaticMeshActor',) and not a.get_actor_label().startswith('VMP_'):
        o, e = a.get_actor_bounds(False)
        if dmin(o.x, o.y) <= 1000 + max(e.x, e.y):
            obst.append({'actor': a.get_actor_label(), 'xy': [round(o.x), round(o.y)], 'r': round(max(e.x, e.y)), 'level': a.get_level().get_outer().get_name()})
bounds = {}
for p in MESHES:
    m = u.load_asset(p)
    if m:
        b = m.get_bounds(); bounds[p] = {'origin': [round(b.origin.x), round(b.origin.y), round(b.origin.z)], 'extent': [round(b.box_extent.x), round(b.box_extent.y), round(b.box_extent.z)]}
    else:
        bounds[p] = None
dec = {p: (u.load_asset(p) is not None) for p in DECALS}
json.dump({'rows': rows, 'obstacles': obst, 'mesh_bounds': bounds, 'decals': dec}, open(os.path.join(VMP, 'area_probe.json'), 'w'), indent=1)
print('AREA_PROBE rows %d obstacles %d meshes %d decals %s' % (len(rows), len(obst), sum(1 for v in bounds.values() if v), dec))
for p, b in bounds.items():
    print('  ', p.rsplit('/', 1)[-1], b)
