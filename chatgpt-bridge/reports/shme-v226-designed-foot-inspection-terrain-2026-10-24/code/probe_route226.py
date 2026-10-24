"""probe_route226.py (read-only editor job): the REAL house-forest route geometry for the terrain pilot - ground height profiles along lines
from each exterior door outward (and across the veranda), sampled every 10 cm with a line trace in the EDITOR world; reports every height
jump > 4 cm within 20 cm (= a step edge: position, height, direction) and the slope statistics. Prints ROUTE226 {...}."""
import unreal as u, json, math
ELS = u.get_editor_subsystem(u.UnrealEditorSubsystem); w = ELS.get_editor_world()
acts = {a.get_actor_label(): a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()}
doors = {n: acts[n].get_actor_location() for n in ('VerandaDoor', 'RearKitchenDoor', 'BalconyDoor') if n in acts}
def ground(x, y, z0):
    hit = u.SystemLibrary.line_trace_single(w, u.Vector(x, y, z0 + 250), u.Vector(x, y, z0 - 400), u.TraceTypeQuery.TRACE_TYPE_QUERY1, False, [], u.DrawDebugTrace.NONE, True)
    return hit.to_tuple()[5].z if hit and hit.to_tuple()[0] else None
out = {'doors': {k: [round(v.x), round(v.y), round(v.z)] for k, v in doors.items()}, 'lines': {}}
LINES = []
for name, loc in doors.items():
    for yaw in (0, 90, 180, 270):
        LINES.append((name + '_%d' % yaw, loc.x, loc.y, loc.z, yaw, 1200))
for name, x0, y0, z0, yaw, length in LINES:
    c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)); prof = []; z = z0
    for k in range(0, length + 1, 10):
        g = ground(x0 + c * k, y0 + s * k, z)
        prof.append(g if g is not None else None)
        if g is not None: z = g
    valid = [(k * 10, g) for k, g in enumerate(prof) if g is not None]
    jumps = []
    for i in range(2, len(valid)):
        dz = valid[i][1] - valid[i - 2][1]
        if abs(dz) > 4.0: jumps.append([valid[i][0], round(dz, 1), round(valid[i][1], 1)])
    cov = len(valid) / max(len(prof), 1)
    slopes = [abs(valid[i][1] - valid[i - 1][1]) / max(valid[i][0] - valid[i - 1][0], 1) for i in range(1, len(valid))]
    out['lines'][name] = {'start': [round(x0), round(y0), round(z0)], 'yaw': yaw, 'coverage': round(cov, 2), 'relief': [round(min(g for _, g in valid), 1), round(max(g for _, g in valid), 1)] if valid else None,
                          'max_slope_deg': round(math.degrees(math.atan(max(slopes))), 1) if slopes else None, 'jumps': jumps[:12]}
print('ROUTE226 ' + json.dumps(out, default=str))
