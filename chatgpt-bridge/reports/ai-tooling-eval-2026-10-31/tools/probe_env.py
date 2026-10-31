"""probe_env.py (measure job, read-only): rear-trail pilot segment facts on the AUTHORED trail line.

Trail = TRAIL polyline of Tools/AAAPolishRear20260923/design_terrain.py (the line the 2026-09-23 terrain carve and the 2026-09-24
structural pass used). Segment = arc [s0, s0 + 16.5 m], s0 = projection of the v4 start (2960, -1730).
Writes <OUT>/env_probe.json with:
  segment      resampled centreline every 0.5 m (x, y, landscape z), arc length
  profile      grade (deg) over 1 m and 2 m windows, cross-slope at +-0.75 m
  instances    every foliage/ISM instance within 14 m of the segment: component path + index (stable id for a later move), mesh,
               location, yaw, scale, approx height / crown radius from mesh bounds x scale, arc position s and signed lateral offset
               (+ = left of travel direction), and the component's collision state and response to the Camera / Visibility / Pawn channels
  lookback     from eye height (ground + 165 cm) at segment points, to house targets (roof top and upper corners of the house content
               bounds): blocked by TERRAIN ONLY (landscape height sampled every 25 cm along the sight line) and first blocking hit with the
               Visibility trace (static meshes; foliage has no collision so it is NOT seen by traces)
Nothing is selected, edited or saved.
"""
import unreal as u, json, os, math

OUT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\pilot'
os.makedirs(OUT, exist_ok=True)
TRAIL = [(1950, 2110), (2300, 1850), (2560, 1300), (2520, 750), (2580, 250), (2790, -250), (3010, -760), (2930, -1260),
         (3110, -1800), (3080, -2300), (2780, -2800), (2350, -3340)]
START, SEG_LEN, STEP, BAND = (2960.0, -1730.0), 1650.0, 50.0, 1400.0
world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
A = u.get_editor_subsystem(u.EditorActorSubsystem)
actors = A.get_all_level_actors()
land = [a for a in actors if a.get_class().get_name() == 'Landscape']


IFA = [a for a in actors if a.get_class().get_name() == 'InstancedFoliageActor']


def ground(x, y):  # LANDSCAPE height only: foliage ignored, any other first hit (house, rocks) is ignored and the trace repeated
    ign = list(IFA)
    for _ in range(10):
        h = u.SystemLibrary.line_trace_single(world, u.Vector(x, y, 6000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, ign,
                                              u.DrawDebugTrace.NONE, True)
        t = h.to_tuple() if h else None
        if not t or not t[0] or t[9] is None:
            return None
        if t[9].get_class().get_name() == 'Landscape':
            return t[4].z
        ign.append(t[9])
    return None


# --- arc-length parametrisation of TRAIL
seg = [0.0]
for a, b in zip(TRAIL, TRAIL[1:]):
    seg.append(seg[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))


def at(s):
    for i in range(len(TRAIL) - 1):
        if s <= seg[i + 1] or i == len(TRAIL) - 2:
            t = (s - seg[i]) / max(seg[i + 1] - seg[i], 1e-6)
            a, b = TRAIL[i], TRAIL[i + 1]
            tx, ty = (b[0] - a[0]) / (seg[i + 1] - seg[i]), (b[1] - a[1]) / (seg[i + 1] - seg[i])
            return a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]), tx, ty


def project(x, y):
    best = (1e18, 0, 0)
    for i in range(len(TRAIL) - 1):
        a, b = TRAIL[i], TRAIL[i + 1]; dx, dy = b[0] - a[0], b[1] - a[1]; L2 = dx * dx + dy * dy
        t = max(0.0, min(1.0, ((x - a[0]) * dx + (y - a[1]) * dy) / L2))
        px, py = a[0] + t * dx, a[1] + t * dy; d2 = (x - px) ** 2 + (y - py) ** 2
        if d2 < best[0]:
            L = math.sqrt(L2); side = (dx * (y - a[1]) - dy * (x - a[0])) / L   # >0 = left of travel (UE: x fwd, y right -> sign checked below)
            best = (d2, seg[i] + t * L, side)
    return best[1], math.sqrt(best[0]), best[2]


s0 = project(*START)[0]
s1 = s0 + SEG_LEN
cl = []
s = s0
while s <= s1 + 1e-6:
    x, y, tx, ty = at(s)
    cl.append({'s': round(s - s0, 1), 'x': round(x, 1), 'y': round(y, 1), 'z': ground(x, y), 'tx': round(tx, 4), 'ty': round(ty, 4)})
    s += STEP
prof = []
for i, p in enumerate(cl):
    row = {'s': p['s']}
    for w, k in ((2, 'grade_1m_deg'), (4, 'grade_2m_deg')):
        if i + w < len(cl) and p['z'] is not None and cl[i + w]['z'] is not None:
            row[k] = round(math.degrees(math.atan2(cl[i + w]['z'] - p['z'], w * STEP)), 1)
    # cross slope: right normal in UE (x forward, y right, z up) for tangent (tx, ty) is (-ty, tx)
    zl, zr = ground(p['x'] + p['ty'] * 75, p['y'] - p['tx'] * 75), ground(p['x'] - p['ty'] * 75, p['y'] + p['tx'] * 75)
    if zl is not None and zr is not None:
        row['cross_slope_deg'] = round(math.degrees(math.atan2(zl - zr, 150)), 1)
    prof.append(row)

# --- instances near the segment
inst = []
xs, ys = [p['x'] for p in cl], [p['y'] for p in cl]
bb = (min(xs) - BAND, max(xs) + BAND, min(ys) - BAND, max(ys) + BAND)
cam_ch = u.CollisionChannel.ECC_CAMERA
for a in actors:
    for c in a.get_components_by_class(u.InstancedStaticMeshComponent):
        m = c.get_editor_property('static_mesh')
        if not m or c.get_instance_count() == 0:
            continue
        bnd = m.get_bounds(); ext = bnd.box_extent; org = bnd.origin
        try:
            coll = {'enabled': str(c.get_collision_enabled()).split('.')[-1], 'camera': str(c.get_collision_response_to_channel(cam_ch)).split('.')[-1],
                    'visibility': str(c.get_collision_response_to_channel(u.CollisionChannel.ECC_VISIBILITY)).split('.')[-1],
                    'pawn': str(c.get_collision_response_to_channel(u.CollisionChannel.ECC_PAWN)).split('.')[-1]}
        except Exception as ex:
            coll = {'err': str(ex)}
        for i in range(c.get_instance_count()):
            t = c.get_instance_transform(i, True); L = t.translation
            if not (bb[0] < L.x < bb[1] and bb[2] < L.y < bb[3]):
                continue
            sa, d, side = project(L.x, L.y)
            if sa < s0 - BAND or sa > s1 + BAND or d > BAND:
                continue
            sc = t.scale3d; r = t.rotation.rotator()
            inst.append({'comp': c.get_path_name(), 'idx': i, 'mesh': m.get_name(), 'x': round(L.x, 1), 'y': round(L.y, 1), 'z': round(L.z, 1),
                         'yaw': round(r.yaw, 1), 'scale': [round(sc.x, 3), round(sc.y, 3), round(sc.z, 3)],
                         'height_cm': round((org.z + ext.z) * sc.z, 1), 'crown_r_cm': round(max(ext.x, ext.y) * max(sc.x, sc.y), 1),
                         's': round(sa - s0, 1), 'lat_cm': round(side, 1), 'dist_cm': round(d, 1), 'collision': coll})

# --- lookback: house targets
hb = None
for a in actors:
    lvl = a.get_level().get_outer().get_name() if a.get_level() else ''
    if lvl == 'L_GR_CurrentHouseContent' and a.get_components_by_class(u.StaticMeshComponent):
        o, e = a.get_actor_bounds(True)
        lo, hi = (o.x - e.x, o.y - e.y, o.z - e.z), (o.x + e.x, o.y + e.y, o.z + e.z)
        hb = [lo, hi] if hb is None else [[min(hb[0][k], lo[k]) for k in range(3)], [max(hb[1][k], hi[k]) for k in range(3)]]
look = {'house_bounds': hb, 'rows': []}
if hb:
    cx, cy = (hb[0][0] + hb[1][0]) / 2, (hb[0][1] + hb[1][1]) / 2
    top = hb[1][2]; zu = hb[0][2] + 0.8 * (hb[1][2] - hb[0][2])
    targets = {'roof_centre': (cx, cy, top - 50), 'upper_c1': (hb[0][0], hb[0][1], zu), 'upper_c2': (hb[1][0], hb[0][1], zu),
               'upper_c3': (hb[0][0], hb[1][1], zu), 'upper_c4': (hb[1][0], hb[1][1], zu)}
    for p in cl[::4]:
        if p['z'] is None:
            continue
        eye = (p['x'], p['y'], p['z'] + 165)
        row = {'s': p['s'], 'eye': eye, 'targets': {}}
        for k, tg in targets.items():
            dist = math.dist(eye[:2], tg[:2]); n = max(2, int(dist / 25)); terr = False; first = None
            for j in range(1, n):
                f = j / n; x, y, z = eye[0] + f * (tg[0] - eye[0]), eye[1] + f * (tg[1] - eye[1]), eye[2] + f * (tg[2] - eye[2])
                gz = ground(x, y)
                if gz is not None and gz > z:
                    terr = True; first = round(f * dist / 100, 1); break
            h = u.SystemLibrary.line_trace_single(world, u.Vector(*eye), u.Vector(*tg), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, [], u.DrawDebugTrace.NONE, True)
            ht = h.to_tuple() if h else None
            blk = None
            if ht and ht[0] and ht[9] is not None:
                al = ht[9].get_level().get_outer().get_name() if ht[9].get_level() else ''
                blk = {'actor': ht[9].get_actor_label(), 'level': al, 'dist_m': round(ht[3] / 100, 1), 'is_house': al == 'L_GR_CurrentHouseContent'}
            row['targets'][k] = {'terrain_blocked': terr, 'terrain_block_at_m': first, 'first_hit': blk}
        look['rows'].append(row)
res = {'trail_source': 'Tools/AAAPolishRear20260923/design_terrain.py TRAIL', 's0_on_trail_cm': round(s0, 1), 'segment_len_cm': SEG_LEN,
       'centreline': cl, 'profile': prof, 'instances': inst, 'lookback': look}
json.dump(res, open(os.path.join(OUT, 'env_probe.json'), 'w'), indent=1, default=str)
g = [r.get('grade_2m_deg') for r in prof if r.get('grade_2m_deg') is not None]
print('ENV_PROBE s0 %.0f, %d centre pts, grade2m min %.1f max %.1f, instances %d, house bounds %s, lookback rows %d' % (
    s0, len(cl), min(g), max(g), len(inst), hb is not None, len(look['rows'])))
