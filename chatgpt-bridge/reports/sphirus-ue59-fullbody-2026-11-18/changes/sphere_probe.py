# sphere_probe.py (runtime, PIE, not saved): borrow 4 movable static-mesh components from props, turn them into neutral grey spheres
# (engine BasicShapeMaterial) and park them beside the player's lit shoulders. PIE world only; nothing is saved.
import unreal as u
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(); P = u.GameplayStatics.get_player_controller(W, 0).get_controlled_pawn()
m = [c for c in P.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Manny'][0]
mesh = u.load_asset('/Engine/BasicShapes/Sphere'); mat = u.load_asset('/Engine/BasicShapes/BasicShapeMaterial'); out = []
cand = []
for a in u.GameplayStatics.get_all_actors_of_class(W, u.Actor):
    if a == P: continue
    for c in a.get_components_by_class(u.StaticMeshComponent):
        try:
            if c.get_editor_property('mobility') == u.ComponentMobility.MOVABLE and not c.get_attach_parent(): cand.append((a, c))
        except Exception: pass
fw = P.get_actor_forward_vector(); i = 0
for b in ('upperarm_r', 'upperarm_l'):
    for dz in (0.0, 28.0):
        if i >= len(cand): break
        a, c = cand[i]; i += 1
        loc = m.get_socket_location(b) + fw * 24.0 + u.Vector(0, 0, dz)
        c.set_static_mesh(mesh); c.set_material(0, mat); c.set_collision_enabled(u.CollisionEnabled.NO_COLLISION)
        c.set_simulate_physics(False); a.set_actor_location(loc, False, True); a.set_actor_scale3d(u.Vector(0.14, 0.14, 0.14))
        out.append((a.get_name(), [round(v) for v in (loc.x, loc.y, loc.z)]))
print('SPHERES', len(cand), out)
