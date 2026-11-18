import unreal as u, builtins
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
for a in u.GameplayStatics.get_all_actors_of_class(W, u.DirectionalLight):
    c = a.get_component_by_class(u.DirectionalLightComponent); builtins.SUN_I = c.get_editor_property('intensity'); c.set_intensity(0.0); print('SUN off, was', builtins.SUN_I, 'rot', a.get_actor_rotation())
