# q_gasp1.py (read-only): GASP CMC sandbox character as imported into Sphirus.
import unreal as u
for p in ['/Game/Blueprints/SandboxCharacter_CMC','/Game/Blueprints/SandboxCharacter_CMC_ABP','/Game/Blueprints/RetargetedCharacters/ABP_GenericRetarget','/Game/Blueprints/AC_VisualOverrideManager']:
    a=u.load_asset(p); print('ASSET',p,type(a).__name__ if a else None, 'status',a.get_editor_property('status') if a and hasattr(a,'status') else '')
bp=u.load_asset('/Game/Blueprints/SandboxCharacter_CMC'); C=u.load_object(None,'/Game/Blueprints/SandboxCharacter_CMC.SandboxCharacter_CMC_C'); cdo=u.get_default_object(C)
print('PARENT',C.get_super_class().get_name() if hasattr(C,'get_super_class') else '?')
for c in cdo.get_components_by_class(u.ActorComponent): 
    x=c.get_name()+' '+type(c).__name__
    if isinstance(c,u.SkeletalMeshComponent): x+=' mesh=%s anim=%s'%(c.get_editor_property('skeletal_mesh_asset').get_path_name() if c.get_editor_property('skeletal_mesh_asset') else None, c.get_editor_property('anim_class').get_name() if c.get_editor_property('anim_class') else None)
    print('COMP',x)
scs=u.get_engine_subsystem(u.SubobjectDataSubsystem) if hasattr(u,'SubobjectDataSubsystem') else None
h=scs.k2_gather_subobject_data_for_blueprint(bp) if scs else []
for d in h:
    o=u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(d))
    if o: 
        x=o.get_name()+' '+type(o).__name__
        if isinstance(o,u.SkeletalMeshComponent): x+=' mesh=%s anim=%s'%(o.get_editor_property('skeletal_mesh_asset').get_path_name() if o.get_editor_property('skeletal_mesh_asset') else None, o.get_editor_property('anim_class').get_name() if o.get_editor_property('anim_class') else None)
        print('SCS',x)
cm=cdo.get_editor_property('character_movement')
for k in ['max_walk_speed','max_acceleration','braking_deceleration_walking','ground_friction','braking_friction','use_separate_braking_friction','braking_friction_factor','rotation_rate','orient_rotation_to_movement','use_controller_desired_rotation']:
    try: print('CMC',k,cm.get_editor_property(k))
    except Exception as e: print('CMC',k,'ERR')
print('ROT ctrl yaw',cdo.get_editor_property('use_controller_rotation_yaw'))
try:
    for i in bp.get_editor_property('implemented_interfaces'): print('IFACE',i.get_editor_property('interface').get_name())
except Exception as e: print('IFACE ERR',e)
B=u.BlueprintTools if hasattr(u,'BlueprintTools') else None
try:
    for v in B.list_variables(bp): print('VAR',v)
except Exception as e: print('VARS ERR',str(e)[:80])
