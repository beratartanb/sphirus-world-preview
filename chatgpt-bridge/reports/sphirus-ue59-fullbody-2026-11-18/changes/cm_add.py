# cm_add.py (PIE prelude, runtime only): add / replace entries in the live ABP_Sph_GASP database remap (SphCM keys -> vals).
# builtins.CM_ADD = {relaxed_db_path: replacement_db_path}
import unreal as u, builtins
W_ = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(); P_ = u.GameplayStatics.get_player_controller(W_, 0).get_controlled_pawn()
M_ = [c for c in P_.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'CharacterMesh0'][0]; AI_ = M_.get_anim_instance()
ks = list(AI_.get_editor_property('CM_Keys')); vs = list(AI_.get_editor_property('CM_Vals'))
for k, v in (getattr(builtins, 'CM_ADD', None) or {}).items():
    ka = u.load_asset(k); va = u.load_asset(v); assert ka and va, (k, v)
    names = [x.get_path_name() for x in ks]
    if ka.get_path_name() in names: vs[names.index(ka.get_path_name())] = va
    else: ks.append(ka); vs.append(va)
AI_.set_editor_property('CM_Keys', ks, u.PropertyAccessChangeNotifyMode.NEVER); AI_.set_editor_property('CM_Vals', vs, u.PropertyAccessChangeNotifyMode.NEVER)
print('CMADD', len(ks), [x.get_name() for x in AI_.get_editor_property('CM_Vals')][-3:])
