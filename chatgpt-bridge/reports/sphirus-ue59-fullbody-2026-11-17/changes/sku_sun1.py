import unreal as u, builtins
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
for a in u.GameplayStatics.get_all_actors_of_class(W, u.DirectionalLight):
    a.get_component_by_class(u.DirectionalLightComponent).set_intensity(builtins.SUN_I)
P = u.GameplayStatics.get_player_pawn(W, 0)
C = [c for c in P.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Manny'][0]
C.set_material(0, u.load_asset('/Engine/EngineMaterials/WorldGridMaterial')); print('SUN on, body plain material; cast', C.get_editor_property('cast_shadow'))
H = [c for c in P.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Henley'][0]
print('PP', [ (v.get_name(), v.get_editor_property('unbound'), v.get_editor_property('priority')) for v in u.GameplayStatics.get_all_actors_of_class(W, u.PostProcessVolume)])
