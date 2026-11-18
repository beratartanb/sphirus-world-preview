import unreal as u
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
s = [a for a in u.GameplayStatics.get_all_actors_of_class(W, u.DirectionalLight)][0].get_components_by_class(u.DirectionalLightComponent)[0]
s.set_editor_property('light_source_soft_angle', 0.0); s.set_editor_property('light_source_angle', 0.53); print('SUNSOFT', s.get_editor_property('light_source_soft_angle'))
