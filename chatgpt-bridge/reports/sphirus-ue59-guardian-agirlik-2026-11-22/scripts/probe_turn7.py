# probe_turn7.py (control, read-only): world-space foot + root trajectory and contact curves of run 180 / 90 turn clips (does the planted foot stay put in the clip?)
import unreal as u, math
X=u.AnimPoseExtensions; W=u.AnimPoseSpaces.WORLD; o=[]
opt=u.AnimPoseEvaluationOptions(); opt.set_editor_property('extract_root_motion',False)
B='/Game/Characters/UEFN_Mannequin/Animations/'
ar=u.AssetRegistryHelpers.get_asset_registry()
for n in ('M_Relaxed_Run_Turn_R_180_Lfoot','M_Relaxed_Run_Turn_L_090_Rfoot','M_Relaxed_Run_Turn_L_180_Rfoot'):
    f=[x for x in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine','AnimSequence')) if str(x.asset_name)==n]
    if not f: o.append('NOTFOUND '+n); continue
    a=f[0].get_asset(); d=a.get_play_length(); o.append('%s %s len %.2f rm %s'%(n,f[0].package_name,d,u.AnimationLibrary.is_root_motion_enabled(a)))
    for k in range(int(d*30)+1):
        t=min(k/30.0,d); ps=X.get_anim_pose_at_time(a,t,opt); r=X.get_bone_pose(ps,'root',W); bl=X.get_bone_pose(ps,'ball_l',W).translation; br=X.get_bone_pose(ps,'ball_r',W).translation; pl=X.get_bone_pose(ps,'pelvis',W).translation
        try: c=(X.get_curve_weight(ps,'contact_l'),X.get_curve_weight(ps,'contact_r'))
        except Exception: c=(-1,-1)
        o.append(' t %.2f root(%.0f,%.0f) yaw %.0f | pel(%.0f,%.0f) | bl(%.0f,%.0f,%.0f) br(%.0f,%.0f,%.0f) | c %.2f/%.2f'%(t,r.translation.x,r.translation.y,r.rotation.rotator().yaw,pl.x,pl.y,bl.x,bl.y,bl.z,br.x,br.y,br.z,c[0],c[1]))
open(u.Paths.project_dir()+'Saved/UE59Work/r7/turn7.txt','w').write('\n'.join(o)); print('TURN7',len(o))
