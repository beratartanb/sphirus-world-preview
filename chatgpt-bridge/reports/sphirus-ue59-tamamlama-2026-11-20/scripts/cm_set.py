# cm_set.py (PIE prelude, runtime only): override entries of the live database maps. builtins.NORM_ADD / TEMPO_ADD = {key_db_name: value_db_path}
import unreal as u, builtins
W_=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(); P_=u.GameplayStatics.get_player_controller(W_,0).get_controlled_pawn()
M_=[c for c in P_.get_components_by_class(u.SkeletalMeshComponent) if c.get_name()=='CharacterMesh0'][0]; AI_=M_.get_anim_instance()
K_=[x.get_name() for x in AI_.get_editor_property('CM_Keys')]
def app(vals,add):
    vals=list(vals)
    for k,v in (add or {}).items():
        va=u.load_asset(v); assert va,v; vals[K_.index(k)]=va
    return vals
N_=app(P_.get_editor_property('GR_NormVals'),getattr(builtins,'NORM_ADD',None)); T_=app(P_.get_editor_property('GR_TempoVals'),getattr(builtins,'TEMPO_ADD',None))
P_.set_editor_property('GR_NormVals',N_,u.PropertyAccessChangeNotifyMode.NEVER); P_.set_editor_property('GR_TempoVals',T_,u.PropertyAccessChangeNotifyMode.NEVER)
AI_.set_editor_property('CM_Vals',N_,u.PropertyAccessChangeNotifyMode.NEVER)
print('CMSET',[(k,a.get_name(),b.get_name()) for k,a,b in zip(K_,N_,T_) if 'Stops' in k])
