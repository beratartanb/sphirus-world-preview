"""apply_dress.py (in memory; saved by w_dress.py): VF2C workshop level art - the mask maker's working kit, placed by purpose.
West wall: a drying rack with two masks in progress hung on it. On the drawer chest beside it: the clay face form the masks are laid over,
the glue pot and the torn linen strips (the lay-up station). Side table: the brush jar next to the pigment bowls. Main bench: the paint board.
Every position is validated with a trace (surface owner + height) before the actor is spawned; a failed check skips that piece and says so.
Re-run replaces VF2C_* actors. Small props have no collision (they sit on furniture); the rack blocks like furniture."""
import unreal as u, builtins
EA = u.get_editor_subsystem(u.EditorActorSubsystem); assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
W_ = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); H = '/Game/Sphirus/Props/Handmade20261112/'
for a in EA.get_all_level_actors():
    if a.get_actor_label().startswith('VF2C_'): EA.destroy_actor(a)
IGN = [x for x in EA.get_all_level_actors() if x.get_class().get_name().startswith('BP_GR_DayStation')]
def tr(p0, p1):
    h = u.SystemLibrary.line_trace_single(W_, u.Vector(*p0), u.Vector(*p1), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, IGN, u.DrawDebugTrace.NONE, False)
    if not h: return None, None
    t = h.to_tuple(); return t[4], (t[9].get_actor_label() if t[9] else None)
def top(x, y, z0=330, dz=200):
    l, w = tr((x, y, z0), (x, y, z0 - dz)); return (l.z if l else None), w
def spawn(label, mesh, loc, rot=(0, 0, 0), scale=1.0, collide=False):
    sm = u.load_asset(H + mesh); assert sm, mesh
    a = EA.spawn_actor_from_class(u.StaticMeshActor, u.Vector(*loc), u.Rotator(pitch=rot[0], yaw=rot[1], roll=rot[2])); a.set_actor_label(label); a.set_folder_path('LIVED/VF2C_20261125/workshop')
    c = a.static_mesh_component; c.set_static_mesh(sm); a.set_actor_scale3d(u.Vector(scale, scale, scale)); c.set_mobility(u.ComponentMobility.STATIC)
    if not collide: c.set_collision_enabled(u.CollisionEnabled.NO_COLLISION)
    print('VF2D spawn', label, [round(v) for v in loc], 'level', a.get_outer().get_outer().get_name()); return a
n = 0
# ---- 1. drying rack on the west wall
fz, fw = top(60, 230, 260, 160); wall, ww = tr((120, 230, 230), (0, 230, 230)); free = [tr((40 + dx, 180, 200), (40 + dx, 282, 200))[1] for dx in (0, 20)]
print('VF2D rack checks: floor', fz, fw, '| west wall x', wall.x if wall else None, ww, '| span free', free)
if fz and wall and not any(free):
    rx = wall.x + 20.0; spawn('VF2C_Workshop_DryRack', 'SM_HM_MaskDryRack', (rx, 230, fz), (0, 90, 0), 1.0, True); n += 1
    ref = [a for a in EA.get_all_level_actors() if a.get_actor_label().startswith('LIV_hm_workshop_194')]
    r0 = ref[0].get_actor_rotation() if ref else u.Rotator(0, 0, 0); print('VF2D reference hung mask rotation', round(r0.pitch), round(r0.yaw), round(r0.roll))
    for lab, mesh, ly, lz in (('VF2C_Workshop_RackMask_A', 'SM_HM_MaskStage2_Rough', 230 - 10, 112 - 17), ('VF2C_Workshop_RackMask_B', 'SM_HM_MaskStage1_Blank', 230 + 30, 78 - 17)):
        spawn(lab, mesh, (rx + 9.0 + (0 if lz > 80 else 5.2), ly, fz + lz), (r0.pitch, r0.yaw + 90.0, r0.roll)); n += 1
else: print('VF2D rack SKIPPED')
# ---- 2. lay-up station on the drawer chest
for lab, mesh, x, y, yaw in (('VF2C_Workshop_MaskForm', 'SM_HM_MaskForm', 84, 356, 8), ('VF2C_Workshop_GluePot', 'SM_HM_GluePot', 126, 350, 40), ('VF2C_Workshop_LinenStrips', 'SM_HM_LinenStrips', 44, 360, 20)):
    z, w = top(x, y, 320, 150); print('VF2D station check', lab, z, w)
    if z and w and 'Drawers' in w: spawn(lab, mesh, (x, y, z + 0.2), (0, yaw, 0)); n += 1
    else: print('VF2D', lab, 'SKIPPED (no drawer top under it)')
# ---- 3. brush jar on the side table, paint board on the main bench. These tops carry no collision (traces pass through), so the height
# comes from the props already standing on them (side table props sit at z 240, bench props at z 248).
spawn('VF2C_Workshop_BrushJar', 'SM_HM_BrushJar', (372, 60, 240.2), (0, 25, 0)); n += 1
spawn('VF2C_Workshop_PaintBoard', 'SM_HM_PaintBoard', (415, 302, 248.3), (0, -18, 0)); n += 1
print('VF2D done, actors', n)
