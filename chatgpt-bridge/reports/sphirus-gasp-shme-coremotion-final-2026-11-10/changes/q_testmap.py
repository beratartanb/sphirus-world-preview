import unreal as u, collections
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); print('WORLD',w.get_name())
acts=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
c=collections.Counter(type(a).__name__ for a in acts); print('ACTORS',dict(c))
for a in acts:
    if isinstance(a,(u.Light,u.SkyLight,u.StaticMeshActor)): print('  ',type(a).__name__,a.get_actor_label(),a.get_actor_location(),a.get_actor_scale3d())
