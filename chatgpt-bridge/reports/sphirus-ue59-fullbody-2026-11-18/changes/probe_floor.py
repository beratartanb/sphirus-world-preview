# probe_floor.py (read-only, PIE): what the capsule stands on. CMC current floor, capsule size, traces on visibility and pawn channels,
# sphere sweep with the capsule radius. -> appends to Saved/UE59Work/probe/floor.txt
import unreal as u, builtins
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(); pc = u.GameplayStatics.get_player_controller(W, 0); P = pc.get_controlled_pawn()
cm = P.get_movement_component(); cap = P.get_components_by_class(u.CapsuleComponent)[0]; L = P.get_actor_location()
r = cap.get_scaled_capsule_radius(); hh = cap.get_scaled_capsule_half_height(); o = ['== %s at %s r %.1f hh %.1f bottom %.1f' % (getattr(builtins, 'PF_TAG', ''), L, r, hh, L.z - hh)]
try:
    f = cm.get_editor_property('current_floor'); o.append('CMC floor %s' % str(f.export_text() if hasattr(f, 'export_text') else f)[:600])
except Exception as e: o.append('CMC floor ? %s' % e)
for n in ('max_step_height', 'walkable_floor_angle', 'perch_radius_threshold', 'perch_additional_height', 'use_flat_base_for_floor_checks'):
    try: o.append('CMC %s=%s' % (n, cm.get_editor_property(n)))
    except Exception: pass
def tr(ch, a, b):
    h = u.SystemLibrary.line_trace_single(W, a, b, ch, False, [P], u.DrawDebugTrace.NONE, True)
    if not h: return 'none'
    t = h.to_tuple(); return 'z %.1f nz %.3f %s.%s' % (t[5].z, t[7].z, t[9].get_name() if t[9] else None, t[10].get_name() if t[10] else None)
for nm, ch in (('vis', u.TraceTypeQuery.TRACE_TYPE_QUERY1), ('cam', u.TraceTypeQuery.TRACE_TYPE_QUERY2)):
    o.append('LINE %s centre %s' % (nm, tr(ch, L, u.Vector(L.x, L.y, L.z - hh - 200))))
try:
    h = u.SystemLibrary.sphere_trace_single(W, u.Vector(L.x, L.y, L.z - hh + r + 5), u.Vector(L.x, L.y, L.z - hh - 100), r - 0.5, u.TraceTypeQuery.TRACE_TYPE_QUERY1, False, [P], u.DrawDebugTrace.NONE, True)
    t = h.to_tuple() if h else None
    o.append('SWEEP vis r%.1f: %s' % (r, 'none' if not t else 'impact z %.1f at (%.1f,%.1f) nz %.3f %s.%s sphere-bottom %.1f' % (t[5].z, t[5].x - L.x, t[5].y - L.y, t[7].z, t[9].get_name() if t[9] else None, t[10].get_name() if t[10] else None, t[4].z - r + 0.5)))
except Exception as e: o.append('SWEEP ? %s' % e)
for c in P.get_components_by_class(u.SkeletalMeshComponent):
    o.append('MESH %s z %.1f rel %s' % (c.get_name(), c.get_world_location().z, c.get_editor_property('relative_location')))
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/floor.txt', 'a', encoding='utf8').write('\n'.join(o) + '\n'); print('FLOOR', len(o))
