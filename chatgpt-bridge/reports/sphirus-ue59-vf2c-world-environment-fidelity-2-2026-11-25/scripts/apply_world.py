"""apply_world.py (in memory; saved by w_world.py): VF2C front-yard ground breakup.
Finding: the sunlit ground between the house and the pond reads as a tended lawn - one grass type at even density with a sharp edge to bare soil.
Colour alone (previous pass) did not change that. This pass breaks the surface up with forest litter that belongs under pines: needle
drifts, bark and twig debris, fallen branches, in CLUSTERS (as litter collects), through the project's existing foliage types
(/Game/GraceRanger/Environment/PineCover/FT_Emb_*). No grass is removed (editing foliage instances outside the foliage bookkeeping is unsafe),
nothing is placed on the footpath. Deterministic; re-running adds again, so it is applied once on a clean map."""
import unreal as u, math, random, json, builtins
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None
C = dict(clusters=11, per=10, seed=20261125); C.update(getattr(builtins, 'VF2W', None) or {})
D = '/Game/GraceRanger/Environment/PineCover/FT_Emb_'
FT = {n: u.load_asset(D + n) for n in ('Pile_PineNeedles', 'Pile_PineNeedles_02', 'Pile_PineNeedles_03', 'Pile_PineBark', 'Pile_PineDebris', 'Pile_PineBranch', 'BranchSmall_group')}
assert all(FT.values()), FT
AREA = (300.0, 1950.0, 1560.0, 2470.0)                                  # front yard only; the first try (y up to 2880) buried the shore and the boat in debris
KEEP_OUT = [((620.0, 2620.0), 420.0), ((1400.0, 2980.0), 380.0)]         # boat landing, shore rocks
PATH = [(850, 1750), (900, 2150), (1000, 2500), (1100, 2900)]           # stepping-stone footpath: keep 95 cm clear
def dseg(p, a, b):
    ax, ay = a; bx, by = b; t = max(0.0, min(1.0, ((p[0] - ax) * (bx - ax) + (p[1] - ay) * (by - ay)) / ((bx - ax) ** 2 + (by - ay) ** 2))); return math.hypot(p[0] - ax - t * (bx - ax), p[1] - ay - t * (by - ay))
rng = random.Random(C['seed']); T = {n: [] for n in FT}; tries = 0; centres = []
while len(centres) < C['clusters'] and tries < 400:
    tries += 1; c = (rng.uniform(AREA[0], AREA[2]), rng.uniform(AREA[1], AREA[3]))
    if min(dseg(c, a, b) for a, b in zip(PATH, PATH[1:])) < 170: continue
    if any(math.dist(c, q) < 190 for q in centres): continue
    if any(math.dist(c, k) < r_ + 120 for k, r_ in KEEP_OUT): continue
    centres.append(c)
placed = 0
for cx, cy in centres:
    kind = rng.choice(('needles', 'needles', 'debris', 'branch'))
    for i in range(C['per']):
        r = abs(rng.gauss(0, 62)); a = rng.uniform(0, 6.283); x = cx + r * math.cos(a) * 1.35; y = cy + r * math.sin(a)
        if min(dseg((x, y), p, q) for p, q in zip(PATH, PATH[1:])) < 95: continue
        if any(math.dist((x, y), k) < r_ for k, r_ in KEEP_OUT) or y > AREA[3] + 40: continue
        h = u.SystemLibrary.line_trace_single(W, u.Vector(x, y, 3000), u.Vector(x, y, -1500), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, [], u.DrawDebugTrace.NONE, True)
        if not h: continue
        t = h.to_tuple(); actor = t[9]
        if actor is None or actor.get_class().get_name() != 'Landscape': continue
        loc = t[4] if hasattr(t[4], 'x') else t[5]; nrm = t[7] if hasattr(t[7], 'x') else t[6]
        if nrm.z < .86: continue
        if kind == 'needles': n = rng.choices(('Pile_PineNeedles', 'Pile_PineNeedles_02', 'Pile_PineNeedles_03', 'Pile_PineBark'), (4, 4, 4, 1))[0]
        elif kind == 'debris': n = rng.choices(('Pile_PineDebris', 'Pile_PineBark', 'Pile_PineNeedles_02', 'BranchSmall_group'), (4, 3, 2, 1))[0]
        else: n = rng.choices(('Pile_PineBranch', 'BranchSmall_group', 'Pile_PineDebris'), (3, 3, 2))[0]
        q = u.MathLibrary.make_rot_from_zx(nrm, u.Vector(math.cos(rng.uniform(0, 6.28)), math.sin(rng.uniform(0, 6.28)), 0)); sc = rng.uniform(.75, 1.1) * (1.15 if r < 40 else 1.0)
        T[n].append(u.Transform(u.Vector(loc.x, loc.y, loc.z - 1.0), q, u.Vector(sc, sc, sc))); placed += 1
for n, tr in T.items():
    if tr: u.InstancedFoliageActor.add_instances(W, FT[n], tr)
print('VF2W scatter', json.dumps({'clusters': len(centres), 'placed': placed, 'by': {n: len(v) for n, v in T.items()}, 'centres': [(round(a), round(b)) for a, b in centres]}))
