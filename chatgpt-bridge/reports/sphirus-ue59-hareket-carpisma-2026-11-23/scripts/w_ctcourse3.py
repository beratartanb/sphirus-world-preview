# w_ctcourse3.py (write, gated; manifest lists /Game/Sphirus/Test/L_Sph_MoveTest): round-6 contact lanes of the movement test map.
#   y -4700 log: 25 cm high, 20 cm deep at x -5100 (isolated low obstacle -> trip / forward fall, flat ground beyond)
#   y -5200 tight: knee block (front face x -5740) with a wall 40 cm behind the impact position (rear face x -5840) -> no room to retreat
#   y -3200 low passage: beam with its underside at 150 cm at x -5100 (head-height obstacle, chest-only class)
#   y -2700 pushable: 40 cm cube, simulating physics, mass 25 kg at x -5100
import unreal as u
eas = u.get_editor_subsystem(u.EditorActorSubsystem); w = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
assert w.get_outermost().get_name() == '/Game/Sphirus/Test/L_Sph_MoveTest', w.get_outermost().get_name()
cube = u.load_asset('/Engine/BasicShapes/Cube'); have = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
SPEC = [('MT_CT_Log', (-5090, -4700, 12.5), (0.2, 3, 0.25)), ('MT_CT_TightKnee', (-5710, -5200, 30), (0.6, 3, 0.6)), ('MT_CT_TightWall', (-5855, -5200, 150), (0.3, 3, 3)),
        ('MT_CT_Beam', (-5085, -3200, 175), (0.3, 3, 0.5)), ('MT_CT_Push', (-5080, -2700, 20), (0.4, 0.4, 0.4))]
for lab, loc, sc in SPEC:
    a = have.get(lab) or eas.spawn_actor_from_class(u.StaticMeshActor, u.Vector(*loc), u.Rotator(0, 0, 0))
    a.set_actor_label(lab); a.static_mesh_component.set_static_mesh(cube); a.set_actor_location(u.Vector(*loc), False, False); a.set_actor_scale3d(u.Vector(*sc))
    if lab == 'MT_CT_Push':
        a.set_mobility(u.ComponentMobility.MOVABLE); c = a.static_mesh_component; c.set_simulate_physics(True); c.set_mass_override_in_kg('None', 25.0, True); c.set_linear_damping(0.8); c.set_angular_damping(2.0)
    print('CTCOURSE3', lab, loc, sc)
print('SAVE map', u.EditorLoadingAndSavingUtils.save_packages([w.get_outermost()], False))
print('DIRTY', [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
