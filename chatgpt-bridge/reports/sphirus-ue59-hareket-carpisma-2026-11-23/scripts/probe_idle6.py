# probe_idle6.py (read-only): idle loop + idle break clips: length, hand height range over the pelvis, elbow flexion range, wrist (hand vs
# forearm) angle range, largest hand speed (cm/s), and how far the pelvis shifts sideways - picks calm / fidget-free breaks.
import unreal as u, math
ar=u.AssetRegistryHelpers.get_asset_registry(); X=u.AnimPoseExtensions; o=[]; opt=u.AnimPoseEvaluationOptions(); W=u.AnimPoseSpaces.WORLD
def ang(a,b,c):
    p=[a.x-b.x,a.y-b.y,a.z-b.z]; q=[c.x-b.x,c.y-b.y,c.z-b.z]; d=sum(p[i]*q[i] for i in range(3)); n=math.sqrt(sum(x*x for x in p)*sum(x*x for x in q)) or 1; return math.degrees(math.acos(max(-1,min(1,d/n))))
for a in ar.get_assets_by_path('/Game/Characters/UEFN_Mannequin/Animations',recursive=True):
    n=str(a.asset_name)
    if 'Stand_Idle' not in n or 'Relaxed' not in n or str(a.asset_class_path.asset_name) != 'AnimSequence': continue
    s=u.load_asset(str(a.package_name)); d=s.get_play_length(); hz=[];el=[];wr=[];sp=0;px=[];prev=None
    for k in range(int(d*15)+1):
        p=X.get_anim_pose_at_time(s,k/15.0,opt); g=lambda b:X.get_bone_pose(p,b,W).translation; pl=g('pelvis')
        for sd in 'lr':
            h=g('hand_'+sd); e=g('lowerarm_'+sd); up=g('upperarm_'+sd); m=g('middle_01_'+sd); hz.append(h.z-pl.z); el.append(180-ang(up,e,h)); wr.append(180-ang(e,h,m))
        hr=g('hand_r'); px.append(pl.x)
        if prev: sp=max(sp,math.dist((hr.x,hr.y,hr.z),prev)*15)
        prev=(hr.x,hr.y,hr.z)
    o.append('%-34s len %5.2f | hand z over pelvis %5.1f..%5.1f | elbow flex %4.0f..%4.0f | wrist bend %4.0f..%4.0f | hand speed max %4.0f | pelvis side shift %4.1f'%(n,d,min(hz),max(hz),min(el),max(el),min(wr),max(wr),sp,max(px)-min(px)))
open(u.Paths.project_dir()+'Saved/UE59Work/r6/idle6.txt','w',encoding='utf8').write('\n'.join(sorted(o))); print('IDLE6',len(o))
