# plant_set.py (PIE prelude, runtime only): builtins.PLANT = {field: value} applied to the live ABP_Sph_GASP PlantSettings_Default
import unreal as u, builtins
W_ = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(); P_ = u.GameplayStatics.get_player_controller(W_, 0).get_controlled_pawn()
AI_ = [c for c in P_.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'CharacterMesh0'][0].get_anim_instance()
ps = AI_.get_editor_property('PlantSettings_Default')
for k, v in (getattr(builtins, 'PLANT', None) or {}).items(): ps.set_editor_property(k, v)
AI_.set_editor_property('PlantSettings_Default', ps, u.PropertyAccessChangeNotifyMode.NEVER)
print('PLANTSET', AI_.get_editor_property('PlantSettings_Default').export_text()[:200])
