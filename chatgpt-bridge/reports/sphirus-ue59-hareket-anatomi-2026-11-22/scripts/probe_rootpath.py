# probe_rootpath.py (read-only): root-motion path of transition clips. Every 0.1 s: root x,y (cm, clip frame: +y = forward for these packs
# is checked from the first step), root speed, heading of the root velocity (deg), root yaw; plus contact_l/r curve.
import unreal as u, math, builtins
AR=u.AssetRegistryHelpers.get_asset_registry(); L=u.AnimationLibrary; X=u.AnimPoseExtensions; o=[]
want=getattr(builtins,'RP_WANT',None) or ['M_Neutral_Run_Diamond_F_BR_Rfoot','M_Neutral_Run_Diamond_F_BL_Lfoot','M_Relaxed_Sprint_Turn_090_R_Lfoot','M_Relaxed_Run_Turn_L_090_Lfoot','M_Relaxed_Run_Stop_F_Rfoot','M_Relaxed_Run_Stop_B_Rfoot','M_Neutral_Walk_Pivot_F_B_Lfoot']
f=u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine','AnimSequence')],package_paths=['/Game'],recursive_paths=True)
opt=u.AnimPoseEvaluationOptions(); opt.set_editor_property('extract_root_motion',False)
for ad in AR.get_assets(f):
    n=str(ad.asset_name)
    if n not in want: continue
    s=u.load_asset(str(ad.package_name)); d=s.get_play_length(); o.append('## %s len %.2f %s'%(n,d,ad.package_name))
    def cur(c,t):
        try:
            ts,vs=L.get_float_keys(s,c); i=min(range(len(ts)),key=lambda k:abs(ts[k]-t)); return vs[i]
        except Exception: return -1
    pp=None; k=0; dt=0.05
    while k*dt<=min(d,2.2)+1e-6:
        t=k*dt; p=X.get_anim_pose_at_time(s,t,opt); T=X.get_bone_pose(p,'root',u.AnimPoseSpaces.WORLD); l=T.translation; y=T.rotation.rotator().yaw
        if pp is not None:
            vx=(l.x-pp.x)/dt; vy=(l.y-pp.y)/dt; sp=math.hypot(vx,vy)
            if k%2==0: o.append('  t %.2f root %7.1f %7.1f v %4.0f hdg %5.0f yaw %5.0f | c %3.0f %3.0f | spd curve %4.0f'%(t,l.x,l.y,sp,math.degrees(math.atan2(vy,vx)) if sp>3 else 0,y,cur('contact_l',t),cur('contact_r',t),cur('movedata_speed',t)))
        pp=l; k+=1
open(u.Paths.project_dir()+'Saved/UE59Work/r5/rootpath.txt','w').write('\n'.join(o)); print('ROOTPATH',len(o))
