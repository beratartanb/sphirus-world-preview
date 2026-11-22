# probe_rootmd6.py (read-only): raw clip root speed vs its movedata_speed curve and contact curves (builtins.RM_WANT = clip names)
import unreal as u, math, builtins
AR=u.AssetRegistryHelpers.get_asset_registry(); X=u.AnimPoseExtensions; o=[]; want=getattr(builtins,'RM_WANT',['M_Neutral_Run_Start_B_Lfoot'])
f=u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine','AnimSequence')],package_paths=['/Game/Characters/UEFN_Mannequin'],recursive_paths=True)
opt=u.AnimPoseEvaluationOptions(); opt.set_editor_property('extract_root_motion',False)
for ad in AR.get_assets(f):
    n=str(ad.asset_name)
    if n not in want: continue
    s=u.load_asset(str(ad.package_name)); d=s.get_play_length(); dt=1/30.0; N=int(min(d,getattr(builtins,'RM_TMAX',1.5))/dt); prev=None; row=[]
    for k in range(N+1):
        t=k*dt; p=X.get_anim_pose_at_time(s,t,opt); r=X.get_bone_pose(p,'root',u.AnimPoseSpaces.WORLD).translation
        cv=[X.get_curve_weight(p,c) for c in ('contact_l','contact_r','movedata_speed')]
        sp=math.hypot(r.x-prev[0],r.y-prev[1])/dt if prev else 0.0; prev=(r.x,r.y)
        row.append('%.2f:%0.f/%0.f%s%s'%(t,sp,cv[2],'L' if cv[0]>0.5 else '-','R' if cv[1]>0.5 else '-'))
    o.append('%s len %.2f rate %.2f | t:rootspeed/md(planted) %s'%(n,d,s.get_editor_property('rate_scale'),' '.join(row)))
open(u.Paths.project_dir()+'Saved/UE59Work/r6/rootmd6.txt','w',encoding='utf8').write('\n'.join(o)); print('ROOTMD6',len(o))
