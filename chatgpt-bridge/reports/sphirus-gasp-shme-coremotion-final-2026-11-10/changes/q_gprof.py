# q_gprof.py (measure): root speed / yaw-rate profiles (0.1 s) of GASP Neutral stop, pivot, turn and start clips.
import unreal as u, math
D='/Game/Characters/UEFN_Mannequin/Animations/'
N=['Walk/M_Neutral_Walk_Stop_F_Lfoot','Run/M_Neutral_Run_Stop_F_Lfoot','Sprint/M_Neutral_Sprint_Stop_F_Lfoot','Walk/M_Neutral_Walk_Turn_L_180_Rfoot','Run/M_Neutral_Run_Turn_L_180_Rfoot','Sprint/M_Neutral_Sprint_Turn_R_180_Lfoot','Walk/M_Neutral_Walk_Pivot_F_B_Lfoot','Run/M_Neutral_Run_Pivot_F_B_Lfoot','Walk/M_Neutral_Walk_Start_F_Lfoot','Run/M_Neutral_Run_Start_F_Lfoot','Sprint/M_Neutral_Sprint_Start_F_Lfoot','Walk/M_Neutral_Walk_Loop_F','Run/M_Neutral_Run_Loop_F','Sprint/M_Neutral_Sprint_Loop_F','Run/M_Neutral_Run_Turn_L_090_Rfoot','Walk/M_Neutral_Walk_Turn_L_090_Rfoot']
opt=u.AnimPoseEvaluationOptions(); opt.set_editor_property('evaluation_type',u.AnimDataEvalType.RAW); opt.set_editor_property('extract_root_motion',False)
def rootat(a,t):
    pose=u.AnimPoseExtensions.get_anim_pose_at_time(a,t,opt); return u.AnimPoseExtensions.get_bone_pose(pose,'root',u.AnimPoseSpaces.WORLD)
for n in N:
    a=u.load_asset(D+n)
    if not a: print('MISSING',n); continue
    L=float(a.get_play_length()); t=0.0; r0=rootat(a,0.0); rows=[]; yaw0=r0.rotation.rotator().yaw
    while t+0.1<=L+1e-4:
        r1=rootat(a,t+0.1); d=r1.translation-r0.translation; sp=math.hypot(d.x,d.y)/0.1
        cum=(r1.rotation.rotator().yaw-yaw0+540)%360-180; rows.append('%.1f:%d/%d'%(t,sp,cum)); t+=0.1; r0=r1
    print('PROF',n.split('/')[-1],'L=%.2f'%L,' '.join(rows))
