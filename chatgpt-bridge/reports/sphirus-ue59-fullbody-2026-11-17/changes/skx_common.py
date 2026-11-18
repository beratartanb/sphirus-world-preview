# skx_common.py (runtime only, PIE): body skin MID with given overrides; nothing is saved. Set builtins.SKX = {'S': {...}, 'V': {...}} before exec.
import unreal as u, builtins
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
P = u.GameplayStatics.get_player_pawn(W, 0)
C = [c for c in P.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Manny'][0]
B = u.load_asset('/Game/Sphirus/CharacterLab/Day_20261107/Skin/MI_Sph_Body_HomeB')
C.set_material(0, B); M = C.create_dynamic_material_instance(0, B)
X = getattr(builtins, 'SKX', {})
for k, v in X.get('S', {}).items(): M.set_scalar_parameter_value(k, v)
for k, v in X.get('V', {}).items(): M.set_vector_parameter_value(k, u.LinearColor(*v))
print('SKX', X)
