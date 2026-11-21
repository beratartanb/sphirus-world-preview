# w_ctcourse2.py (write, gated; manifest lists /Game/Sphirus/Test/L_Sph_MoveTest): ramp + stairs lanes of the Sphirus movement test map.
#   y -9500  ramp 15 deg, rising toward +x, low end at x ~ -5390 (starts 610 cm after the start line), 8 m long, 3 m wide
#   y -4000  stairs: 8 steps, rise 18 cm / run 30 cm, first riser at x -5215, then a 4 m platform at 144 cm
import unreal as u
eas = u.get_editor_subsystem(u.EditorActorSubsystem); w = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
assert w.get_outermost().get_name() == '/Game/Sphirus/Test/L_Sph_MoveTest', w.get_outermost().get_name()
cube = u.load_asset('/Engine/BasicShapes/Cube'); have = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
SPEC = [('MT_CT_Ramp', (-5000, -9500, 100), (8, 3, 0.2), 15.0)]
for i in range(8):
    SPEC.append(('MT_CT_Stair%d' % i, (-5200 + i * 30, -4000, (i + 1) * 9.0), (0.3, 3, (i + 1) * 0.18), 0.0))
SPEC.append(('MT_CT_StairTop', (-5200 + 8 * 30 + 185, -4000, 72), (4, 3, 1.44), 0.0))
for lab, loc, sc, pitch in SPEC:
    a = have.get(lab) or eas.spawn_actor_from_class(u.StaticMeshActor, u.Vector(*loc), u.Rotator(0, 0, 0))
    a.set_actor_label(lab); a.static_mesh_component.set_static_mesh(cube); a.set_actor_location(u.Vector(*loc), False, False)
    a.set_actor_rotation(u.Rotator(roll=0, pitch=pitch, yaw=0), False); a.set_actor_scale3d(u.Vector(*sc))
    print('CTCOURSE2', lab, loc, sc, pitch)
print('SAVE map', u.EditorLoadingAndSavingUtils.save_packages([w.get_outermost()], False))
print('DIRTY', [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
