# VF2B read-only probes: what is the white balcony floor, the white shapes on the upper hall wall, and does the fireplace take decals.
import unreal as u, math
W_ = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); EA = u.get_editor_subsystem(u.EditorActorSubsystem)
def tr(p0, p1, ign=[]):
    h = u.SystemLibrary.line_trace_single(W_, u.Vector(*p0), u.Vector(*p1), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, ign, u.DrawDebugTrace.NONE, False)
    if not h: return None
    t = h.to_tuple(); a = t[9]; c = t[10]
    mats = [m.get_path_name().split('.')[0] if m else None for m in c.get_materials()][:3] if c and hasattr(c, 'get_materials') else []
    sm = c.get_editor_property('static_mesh').get_name() if c and isinstance(c, u.StaticMeshComponent) and c.get_editor_property('static_mesh') else None
    return (a.get_actor_label() if a else None, str(a.get_folder_path()) if a else None, sm, mats, [round(v) for v in (t[4].x, t[4].y, t[4].z)], 'decals', c.get_editor_property('receives_decals') if c else None)
for nm, p in (('balcony_a', (540, 200, 600)), ('balcony_b', (450, 120, 600)), ('balcony_c', (620, 300, 600))):
    print('PH', nm, tr(p, (p[0], p[1], p[2] - 250)))
cam = (814, 570, 648)
for yaw, pitch in ((172, 6), (168, 4), (176, 8), (180, 2), (165, 10)):
    d = (math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)), math.sin(math.radians(yaw)) * math.cos(math.radians(pitch)), math.sin(math.radians(pitch)))
    print('PH wall', yaw, pitch, tr(cam, (cam[0] + d[0] * 900, cam[1] + d[1] * 900, cam[2] + d[2] * 900)))
for a in EA.get_all_level_actors():
    if a.get_actor_label() in ('Furniture_R3_StoneFireplace', 'Architecture_07_CHIMNEY_StoneChimney', 'GR_MaskBench') or a.get_actor_label().startswith('VF2H_'):
        for c in a.get_components_by_class(u.PrimitiveComponent): print('PH comp', a.get_actor_label(), c.get_name(), 'receives_decals', c.get_editor_property('receives_decals'))
        if isinstance(a, u.DecalActor): print('PH decal', a.get_actor_label(), a.get_actor_location(), a.get_actor_rotation(), a.decal.get_editor_property('decal_size'), a.decal.get_decal_material().get_name())
