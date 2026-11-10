# t1_testlight.py (write, test map only): L_Sph_MoveTest rendered black because its sun was 6 lux (house: 1450 lux,
# movable) while the player CineCamera exposure is set up for the house. Match the house sun / sky so the flat test
# stage can be used for full-body review videos. Production map untouched.
import unreal as u
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); assert w.get_name()=='L_Sph_MoveTest',w.get_name()
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    if a.get_actor_label()=='MT_Sun':
        a.modify(); c=a.get_component_by_class(u.LightComponentBase); c.set_editor_property('mobility',u.ComponentMobility.MOVABLE); c.set_editor_property('intensity',1450.0)
        a.set_actor_rotation(u.Rotator(pitch=-24.0,yaw=-60.0,roll=0.0),False); print('SUN',c.get_editor_property('intensity'),a.get_actor_rotation())
    if a.get_actor_label()=='MT_Sky':
        a.modify(); c=a.get_component_by_class(u.LightComponentBase); c.set_editor_property('mobility',u.ComponentMobility.MOVABLE); c.set_editor_property('intensity',0.8); print('SKY',c.get_editor_property('intensity'))
print('SAVE',u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level())
