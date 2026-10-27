exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py',encoding='utf8').read(),'shm_build.py','exec'))
import shm_component_vars as CV; importlib.reload(CV)
bp=bp_asset('BP_SHM_HumanMotionComponent',u.ActorComponent.static_class())
resp=u.load_asset(D+'/BP_SHM_ResponseProfile').generated_class();anth=u.load_asset(D+'/BP_SHM_AnthropometryProfile').generated_class()
ensure_vars(bp,[('Response',resp,'SHM|Config'),('Anthro',anth,'SHM|Config'),('OwnerChar',u.Character.static_class(),'SHM|Refs'),
  ('Mesh',u.SkeletalMeshComponent.static_class(),'SHM|Refs'),('MoveComp',u.CharacterMovementComponent.static_class(),'SHM|Refs'),
  ('Capsule',u.CapsuleComponent.static_class(),'SHM|Refs')]+CV.VARS)
for n in ['Response','Anthro','TelemetryLabel']:B.set_variable_instance_editable(bp,n,True)
st,errs=compile_ok(bp)
set_defaults(bp,{'Response':u.load_asset(D+'/DA_SHM_Response_Default'),'Anthro':u.load_asset(D+'/DA_SHM_Anthropometry_Default'),'CamBoomScale':1.0,'CamShoulderScale':1.0,'CamAirFollowFraction':0.25,'CamAirMaxLag':45.0,'CamRecScale':1.0})   # V2.33 CamRecScale (device profile, written by BP_GR_Player)
save(bp);print(st,errs[:2],len(B.list_variables(bp)))
eg=graph(bp,'EventGraph')
for q in ['OwnerChar','MeshAl','CharacterMovementAl','CastToCharacter','GetCapsuleComponent','BreakHitResult','Append','ToString(Vector)','ToString(Integer)','ToString(Boolean)','GetPlayerCameraManager','GetCameraRotation','GetCameraLocation','Delta(Rotator)','NormalizeAxis','Normalize2D','GetScaledCapsuleHalfHeight','GetMaxAcceleration']:
    print(q,[getattr(x,'type_id',x) for x in B.find_node_types(eg,q)][:8])
for t in ['İşlevsellikler|Casting|CastToCharacter','Çarpışma|BreakHitResult','Dönüşüm|GetSocketLocation']:
    i=B.get_node_type_pins(eg,t);print(t,'IN',[p.name for p in i.input_pins],'OUT',[p.name for p in i.output_pins])
