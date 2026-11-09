# q_prof.py (measure): root speed / yaw-rate profiles per 0.1 s of the start, stop, pivot and loop clips of all gaits,
# to calibrate capsule acceleration / braking / turn timing against the source motion (SHME physical contract).
import unreal as u, math
C='/Game/Sphirus/Player/Anim/Core/'
N=['af_Loco_%s_%s'%(g,k) for g in ('Walk','Jog','Run') for k in ('Fwd','Fwd_Start','Fwd_Stop','Fwd_Pivot')]+['af_Loco_Walk_Start_TurnL180_Lfoot','af_Loco_Jog_Start_TurnL180_Lfoot','af_Loco_Run_Start_TurnL180_Lfoot','af_Loco_Walk_Start_TurnL090_Lfoot','af_Stand_Idle_TurnL180','af_Stand_Idle_TurnL090']
opt=u.AnimPoseEvaluationOptions(); opt.set_editor_property('evaluation_type',u.AnimDataEvalType.RAW); opt.set_editor_property('extract_root_motion',False)
def rootat(a,t):
    pose=u.AnimPoseExtensions.get_anim_pose_at_time(a,t,opt); return u.AnimPoseExtensions.get_bone_pose(pose,'root',u.AnimPoseSpaces.WORLD)
STEP=0.1
for n in N:
    a=u.load_asset(C+n)
    if not a: print('MISSING',n); continue
    L=float(a.get_play_length()); t=0.0; r0=rootat(a,0.0); rows=[]; yaw0=r0.rotation.rotator().yaw
    while t+STEP<=L+1e-4:
        r1=rootat(a,t+STEP); d=r1.translation-r0.translation; sp=math.hypot(d.x,d.y)/STEP
        y1=r1.rotation.rotator().yaw; dy=(y1-r0.rotation.rotator().yaw+540)%360-180; cum=(y1-yaw0+540)%360-180
        rows.append('%.1f:%d/%d/%d'%(t,sp,dy/STEP,cum)); t+=STEP; r0=r1
    print('PROF',n,'L=%.2f'%L,'t:speed/yawrate/cumyaw',' '.join(rows))
# any graph nodes writing friction / braking / acceleration each frame?
exec(open(u.Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
bp=u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); g=B.get_graph(bp,'EventGraph')
for x in B.find_nodes(g):
    t=str(info(pn(x)).type_id)
    if any(k in t for k in ('Friction','Braking','MaxAcceleration','RotationRate','OrientRotation')): print('GRAPHNODE',t[-70:])
sds=u.get_engine_subsystem(u.SubobjectDataSubsystem); SB=u.SubobjectDataBlueprintFunctionLibrary
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o=SB.get_object(SB.get_data(h))
    if o and isinstance(o,u.CharacterMovementComponent):
        c=SB.get_object_for_blueprint(SB.get_data(h),bp)
        print('CMC',{k:str(c.get_editor_property(k)) for k in ('ground_friction','braking_friction','use_separate_braking_friction','braking_friction_factor','braking_deceleration_walking','max_acceleration','max_walk_speed','rotation_rate','orient_rotation_to_movement','use_controller_desired_rotation','braking_sub_step_time','max_simulation_time_step')})
print('Q_DONE')
