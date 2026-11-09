# q_cam.py (measure): camera ownership chain of BP_HybridA_Player - spring arm / camera component defaults and every
# event-graph node that writes or reads the spring arm, camera, control rotation or view target, with literal pin values.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
bp=u.load_asset(PP); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem); SB=u.SubobjectDataBlueprintFunctionLibrary
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o=SB.get_object_for_blueprint(SB.get_data(h),bp)
    if not o: continue
    cn=o.get_class().get_name()
    if cn in ('SpringArmComponent','CineCameraComponent','CameraComponent','CharacterMovementComponent','CapsuleComponent'):
        keys={'SpringArmComponent':('target_arm_length','socket_offset','target_offset','use_pawn_control_rotation','inherit_pitch','inherit_yaw','inherit_roll','enable_camera_lag','camera_lag_speed','camera_lag_max_distance','enable_camera_rotation_lag','camera_rotation_lag_speed','do_collision_test','probe_size','probe_channel','relative_location','relative_rotation','use_camera_lag_substepping'),
              'CineCameraComponent':('relative_location','relative_rotation','field_of_view','current_aperture','constrain_aspect_ratio','use_pawn_control_rotation','auto_activate'),
              'CameraComponent':('relative_location','field_of_view','use_pawn_control_rotation','auto_activate'),
              'CharacterMovementComponent':('max_walk_speed','max_acceleration','braking_deceleration_walking','rotation_rate','orient_rotation_to_movement','use_controller_desired_rotation','ground_friction','braking_friction_factor','braking_friction','use_separate_braking_friction','max_walk_speed_crouched'),
              'CapsuleComponent':('capsule_half_height','capsule_radius')}[cn]
        print('COMP',cn,o.get_name(),{k:str(o.get_editor_property(k))[:70] for k in keys if hasattr(o,k) or True})
cdo=u.get_default_object(bp.generated_class()); print('PAWN',{k:str(cdo.get_editor_property(k)) for k in ('use_controller_rotation_yaw','use_controller_rotation_pitch')})
g=B.get_graph(bp,'EventGraph'); N=[pn(x) for x in B.find_nodes(g)]; tp=lambda p:str(info(p).type_id)
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
KEY=('SpringArm','Camera','TargetArmLength','SocketOffset','TargetOffset','ControlRotation','ViewTarget','Cine','FieldOfView','Fov','Shoulder','Arm','Lag','LookInput','Cam')
for p in N:
    t=tp(p)
    if any(k in t for k in KEY):
        ins={str(x.name):pv(p,str(x.name)) for x in info(p).input_pins if str(x.name) not in ('execute','self')}
        lit={k:v for k,v in ins.items() if v not in (None,'','None','0.0','false','False') and not str(v).startswith('(')}
        print('NODE',t[-70:],lit)
# variables that look camera related
print('VARS',[str(v) for v in B.list_variables(bp) if any(k.lower() in str(v).lower() for k in ('cam','arm','shoulder','fov','look','aim','pitch','yaw','indoor','steady','gait'))])
print('Q_DONE')
