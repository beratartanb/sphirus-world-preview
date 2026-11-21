# w_ctcourse.py (write, gated; manifest lists /Game/Sphirus/Test/L_Sph_MoveTest): contact test course in the Sphirus movement test map.
# Lanes run along +x, start line x = -6000 (POS "-6000 <y> 92 0"); floor z = 0. All actors are basic cubes labelled MT_CT_*.
#   y -6000  wall (3 m high) at x -5100            y -6500  waist-high block 105 cm at x -5100     y -7000  knee-high block 60 cm at x -5100
#   y -7500  wall beside the lane (gap 6 cm on the right), x -5600 .. -4200                        y -8000  wall at x -4500 (sprint lane)
#   y -8500  wall turned 45 deg at x -5100 (glancing impact)                                       y -9000  low step 30 cm at x -5100 (below step height)
import unreal as u
eas = u.get_editor_subsystem(u.EditorActorSubsystem); w = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
assert w.get_outermost().get_name() == '/Game/Sphirus/Test/L_Sph_MoveTest', w.get_outermost().get_name()
cube = u.load_asset('/Engine/BasicShapes/Cube'); have = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
SPEC = [('MT_CT_Wall', (-5085, -6000, 150), (0.3, 6, 3), 0), ('MT_CT_Waist', (-5060, -6500, 52.5), (0.8, 3, 1.05), 0), ('MT_CT_Knee', (-5070, -7000, 30), (0.6, 3, 0.6), 0),
        ('MT_CT_Side', (-4900, -7500 + 30 + 6 + 15, 150), (14, 0.3, 3), 0), ('MT_CT_WallSprint', (-4485, -8000, 150), (0.3, 6, 3), 0),
        ('MT_CT_Wall45', (-5000, -8500, 150), (0.3, 8, 3), 45), ('MT_CT_Step', (-5070, -9000, 15), (0.6, 3, 0.3), 0)]
for lab, loc, sc, yaw in SPEC:
    a = have.get(lab) or eas.spawn_actor_from_class(u.StaticMeshActor, u.Vector(*loc), u.Rotator(0, 0, yaw))
    a.set_actor_label(lab); a.static_mesh_component.set_static_mesh(cube); a.set_actor_location(u.Vector(*loc), False, False)
    a.set_actor_rotation(u.Rotator(roll=0, pitch=0, yaw=yaw), False); a.set_actor_scale3d(u.Vector(*sc))
    print('CTCOURSE', lab, loc, sc, yaw)
print('SAVE map', u.EditorLoadingAndSavingUtils.save_packages([w.get_outermost()], False))
print('DIRTY', [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
