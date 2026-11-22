# probe_rawfoot.py (read-only): RAW clip check of planted-foot travel. For each clip: every contact interval of the clip's own contact
# curve (< 10 for >= 0.08 s): largest horizontal travel of the ball bone in animation space (root motion included) = what the clip
# itself does while its curve says "planted". Tells a clip-authored settle step from an in-game slide.
import unreal as u, math, builtins
AR=u.AssetRegistryHelpers.get_asset_registry(); X=u.AnimPoseExtensions; o=[]
want=getattr(builtins,'RF_WANT',None) or ['M_Relaxed_Run_Stop_B_Rfoot','M_Relaxed_Run_Stop_B_Lfoot','M_Relaxed_Run_Stop_F_Lfoot','M_Relaxed_Run_Stop_F_Rfoot','M_Relaxed_Walk_Stop_F_Rfoot','M_Relaxed_Walk_Stop_F_Lfoot','M_Relaxed_Stand_Idle_Loop','M_Relaxed_Run_Turn_L_180_Rfoot','M_Relaxed_Run_Turn_R_180_Rfoot','M_Neutral_Walk_Pivot_F_B_Lfoot','M_Neutral_Walk_Pivot_F_B_Rfoot','M_Relaxed_Sprint_Turn_090_R_Lfoot','M_Neutral_Run_Start_F_Lfoot']
f=u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine','AnimSequence')],package_paths=['/Game'],recursive_paths=True)
opt=u.AnimPoseEvaluationOptions(); opt.set_editor_property('extract_root_motion',False)
for ad in AR.get_assets(f):
    n=str(ad.asset_name)
    if n not in want: continue
    s=u.load_asset(str(ad.package_name)); d=s.get_play_length(); dt=1/60.0; N=int(d/dt)
    S=[]
    for k in range(N+1):
        t=min(k*dt,d); p=X.get_anim_pose_at_time(s,t,opt)
        try: c=(X.get_curve_weight(p,'contact_l'),X.get_curve_weight(p,'contact_r'))
        except Exception as e: c=(-1,-1)
        bl=X.get_bone_pose(p,'ball_l',u.AnimPoseSpaces.WORLD).translation; br=X.get_bone_pose(p,'ball_r',u.AnimPoseSpaces.WORLD).translation
        S.append((t,c,(bl.x,bl.y,bl.z),(br.x,br.y,br.z)))
    line='%-36s len %.2f curve range L %.0f..%.0f R %.0f..%.0f |'%(n,d,min(x[1][0] for x in S),max(x[1][0] for x in S),min(x[1][1] for x in S),max(x[1][1] for x in S))
    for k in (0,1):
        i=0
        while i<len(S):
            if S[i][1][k]>0.5:
                j=i
                while j<len(S) and S[j][1][k]>0.5: j+=1
                if S[j-1][0]-S[i][0]>=0.08:
                    p0=S[i][2+k]; dd=max(math.hypot(S[q][2+k][0]-p0[0],S[q][2+k][1]-p0[1]) for q in range(i,j)); zz=max(S[q][2+k][2] for q in range(i,j))
                    line+=' %s %.2f-%.2f %.1fcm(z%.0f)'%('LR'[k],S[i][0],S[j-1][0],dd,zz)
                i=j
            else: i+=1
    o.append(line)
open(u.Paths.project_dir()+'Saved/UE59Work/r5/rawfoot.txt','w',encoding='utf8').write('\n'.join(sorted(o))); print('RAWFOOT',len(o))
