# probe_startpel8.py (control, read-only): pelvis / head height and root speed over time of the start-chain clips (source layer)
import unreal as u
X=u.AnimPoseExtensions; W=u.AnimPoseSpaces.WORLD; o=[]; opt=u.AnimPoseEvaluationOptions(); opt.set_editor_property('extract_root_motion',False)
ar=u.AssetRegistryHelpers.get_asset_registry(); AL={str(x.asset_name):x for x in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine','AnimSequence'))}
for n in ('M_Relaxed_Stand_Idle_Loop','M_Neutral_Walk_Start_F_Rfoot','M_Relaxed_Transition_Walk_to_Run_Rfoot','M_Neutral_Run_Start_F_Rfoot','M_Neutral_Run_Start_F_Lfoot','M_Relaxed_Run_Start_F_Rfoot','M_Neutral_Run_Loop_F','M_Neutral_Walk_Loop_F','M_Neutral_Tr_Run_to_Walk_Lfoot','M_Relaxed_Transition_Run_to_Walk_Lfoot','M_Neutral_Transition_Run_to_Walk_Lfoot'):
    if n not in AL: o.append('NOTFOUND '+n); continue
    a=AL[n].get_asset(); d=a.get_play_length(); row=[]; pr=None
    for k in range(0,int(d*10)+1):
        t=min(k/10.0,d); ps=X.get_anim_pose_at_time(a,t,opt); r=X.get_bone_pose(ps,'root',W).translation; p=X.get_bone_pose(ps,'pelvis',W).translation; h=X.get_bone_pose(ps,'head',W).translation
        sp=0 if pr is None else ((r.x-pr.x)**2+(r.y-pr.y)**2)**0.5/0.1; pr=r
        row.append('%.1f:p%.0f h%.0f v%.0f'%(t,p.z,h.z,sp))
        if k>=22: break
    o.append('%s len %.2f | %s'%(n,d,' '.join(row)))
open(u.Paths.project_dir()+'Saved/UE59Work/r8/startpel8.txt','w').write('\n'.join(o)); print('SP8',len(o))
