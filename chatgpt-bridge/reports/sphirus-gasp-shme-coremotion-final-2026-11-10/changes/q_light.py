import unreal as u
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); print('WORLD',w.get_name())
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    if isinstance(a,(u.DirectionalLight,u.SkyLight)):
        c=a.get_component_by_class(u.LightComponentBase)
        print('LIGHT',w.get_name(),a.get_actor_label(),type(a).__name__,'int',c.get_editor_property('intensity'),'mob',c.get_editor_property('mobility'),'rot',a.get_actor_rotation())
    if isinstance(a,u.PostProcessVolume):
        s=a.get_editor_property('settings'); print('PPV',a.get_actor_label(),'unbound',a.get_editor_property('unbound'),'expMethod',s.get_editor_property('auto_exposure_method'),'bias',s.get_editor_property('auto_exposure_bias'),'override_bias',s.get_editor_property('override_auto_exposure_bias'))
