# w_ctcorr7.py (write, gated; manifest lists /Game/Sphirus/Test/L_Sph_MoveTest) - round 7: TIGHT-SPACE IMPACT lane of the movement test map.
#   y -10500 corridor: two side walls 96 cm apart (inner faces y -10548 / -10452), 6 m long from x -5700, end wall face at x -5100.
#   Knee-high block MT_CT_CorrKnee (front face x -5530, full corridor width): a trip / stagger between the side walls.
#   Floor slab MT_CT_CorrFloor (top z 0) from x -7050 to -4450: the map ground ends before this y.
#   Running into the end wall happens with the side walls 14 cm beyond the capsule on each side: the reaction (stagger steps, bracing hand,
#   arm swing) has to stay inside the corridor.
import unreal as u
eas = u.get_editor_subsystem(u.EditorActorSubsystem); w = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
assert w.get_outermost().get_name() == '/Game/Sphirus/Test/L_Sph_MoveTest', w.get_outermost().get_name()
cube = u.load_asset('/Engine/BasicShapes/Cube'); have = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
SPEC = [('MT_CT_CorrFloor', (-5750, -10500, -5), (26.0, 3.0, 0.1)), ('MT_CT_CorrL', (-5400, -10558, 125), (6.0, 0.2, 2.5)), ('MT_CT_CorrR', (-5400, -10442, 125), (6.0, 0.2, 2.5)), ('MT_CT_CorrEnd', (-5085, -10500, 125), (0.3, 1.4, 2.5)), ('MT_CT_CorrKnee', (-5500, -10500, 30), (0.6, 0.96, 0.6))]
for lab, loc, sc in SPEC:
    a = have.get(lab) or eas.spawn_actor_from_class(u.StaticMeshActor, u.Vector(*loc), u.Rotator(0, 0, 0))
    a.set_actor_label(lab); a.static_mesh_component.set_static_mesh(cube); a.set_actor_location(u.Vector(*loc), False, False); a.set_actor_scale3d(u.Vector(*sc))
    print('CTCORR7', lab, loc, sc)
print('SAVE map', u.EditorLoadingAndSavingUtils.save_packages([w.get_outermost()], False))
print('DIRTY', [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
