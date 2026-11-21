# hk_pose.py (prelude, read-only): hk_gait fields + full pose of the visible body ('Manny') and of the driver mesh in component
# space per frame -> row['hook']['pv'] / ['pd'] (bone: [x,y,z], 0.1 cm) and hand/forearm/upperarm/head quats of the visible body ['pq'].
import builtins, unreal as _u
_BN=('pelvis','spine_01','spine_03','spine_05','neck_01','neck_02','head','clavicle_l','clavicle_r','upperarm_l','upperarm_r','lowerarm_l','lowerarm_r','hand_l','hand_r','middle_01_l','middle_01_r','thigh_l','thigh_r','calf_l','calf_r','foot_l','foot_r','ball_l','ball_r')
_QN=('pelvis','spine_03','spine_05','head','upperarm_l','upperarm_r','lowerarm_l','lowerarm_r','hand_l','hand_r')
def _hk(pw, ai, st, w_):
    o={}
    for k in ('GR_TempoOn','GR_TempoAct','GR_BrakeHold','GR_HoldT','GR_Back','GR_GaitSel','GR_Gait','GR_Pace','GR_HomeContext','GR_Load2H','SphContextSpeedScale','GR_StopHold'):
        try:
            v=pw.get_editor_property(k); o[k]=round(float(v),3) if isinstance(v,float) else (bool(v) if isinstance(v,bool) else int(v))
        except Exception: o[k]=None
    try: o['cv']=[round(float(ai.get_curve_value(n)),2) for n in ('contact_l','contact_r','movedata_speed')]
    except Exception as e: o['cv']=None
    try:
        m=[c for c in pw.get_components_by_class(_u.ActorComponent) if c.get_name()=='SphMotion'][0]
        o['m']=[round(float(m.get_editor_property(n)),2) for n in ('StK','StT','BrakeDecel','BrakeLatchSpeed','StartT','TurnCap','RcW','RcK','RcA','RcExit','RevFricMul','TlG','TlPeak','DmT','DmK','DmDecel')]
    except Exception as e: o['m']=None
    try:
        k={c.get_name():c for c in pw.get_components_by_class(_u.SkeletalMeshComponent)}; vis=k.get('Manny'); C=_u.RelativeTransformSpace.RTS_COMPONENT
        pv={}; pd={}; pq={}
        for b in _BN:
            t=vis.get_socket_transform(b,C).translation; pv[b]=[round(t.x,1),round(t.y,1),round(t.z,1)]
            t=pw.mesh.get_socket_transform(b,C).translation; pd[b]=[round(t.x,1),round(t.y,1),round(t.z,1)]
        for b in _QN:
            q=vis.get_socket_transform(b,C).rotation; pq[b]=[round(q.x,4),round(q.y,4),round(q.z,4),round(q.w,4)]
        o['pv']=pv; o['pd']=pd; o['pq']=pq
    except Exception as e: o['perr']=repr(e)[:120]
    try: o['nf']=round(float(ai.get_curve_value('SphNoFootIK')),3)
    except Exception as e: o['nf']=None
    try:
        m_=[c for c in pw.get_components_by_class(_u.ActorComponent) if c.get_name()=='SphMotion'][0]; o['eff']=[round(float(m_.get_editor_property(n)),3) for n in ('E','EUse','Fat','Demand')]
    except Exception as e: o['eff']=None
    try: o['ps']=[round(float(pw.get_editor_property(n)),2) for n in ('PS_C3','PS_C5','PS_CN','PS_CH','PS_CHR','PS_CYL','PS_CYR','PS_CPL','PS_CPR','PS_PAL','PS_PAR','PS_A1','PS_A2','PS_A3','PS_A4','PS_DAL','PS_DAR','PS_Eff','PS_Bent','PS_LP','PS_LR','PS_AccF','PS_AccR')]
    except Exception as e: o['pserr']=repr(e)[:80]
    try:
        o['sm']=[bool(ai.get_editor_property('UseExperimentalStateMachine')),str(ai.get_editor_property('StateMachineState')).split('.')[-1].split(':')[0],round(float(ai.get_editor_property('Search Cost')),2)]
        b=ai.get_editor_property('BlendStackInputs'); o['bs']=b.export_text()[:400]
    except Exception as e: o['smerr']=repr(e)[:120]
    try:
        C_=_u.RelativeTransformSpace.RTS_COMPONENT; W_=_u.RelativeTransformSpace.RTS_WORLD
        o['rt']=[round(pw.mesh.get_socket_transform('root',C_).rotation.rotator().yaw,1),round(pw.mesh.get_socket_transform('root',W_).rotation.rotator().yaw,1),round(pw.mesh.get_socket_transform('pelvis',W_).rotation.rotator().yaw,1),round(pw.mesh.get_world_rotation().yaw,1)]+[round(x,1) for x in pw.mesh.get_socket_transform('root',C_).translation.to_tuple()]
        for k_ in ('OffsetRootBoneEnabled','TargetRotationDelta'):
            try: o[k_]=round(float(ai.get_editor_property(k_)),2)
            except Exception: pass
    except Exception as e: o['rterr']=repr(e)[:120]
    return o
builtins.VID_TICKHOOK=_hk
