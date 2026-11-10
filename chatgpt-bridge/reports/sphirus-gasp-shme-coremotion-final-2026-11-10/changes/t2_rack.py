# t2_rack.py (control, test map only): add the review camera actor 'GR_CamRack' (used by vid.py VID_SIDE) to L_Sph_MoveTest.
import unreal as u
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); assert w.get_name()=='L_Sph_MoveTest',w.get_name()
EAS=u.get_editor_subsystem(u.EditorActorSubsystem)
if not [a for a in EAS.get_all_level_actors() if a.get_actor_label()=='GR_CamRack']:
    a=EAS.spawn_actor_from_class(u.CameraActor,u.Vector(0,0,300),u.Rotator(0,0,0)); a.set_actor_label('GR_CamRack'); print('ADDED',a.get_actor_label())
print('SAVE',u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level())
