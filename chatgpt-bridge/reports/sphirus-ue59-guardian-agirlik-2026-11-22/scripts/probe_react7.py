# probe_react7.py (read-only): stumble / push / hit / fall / floor / get-up clip inventory. Per clip: skeleton, length, root motion flag,
# pelvis height min / end, horizontal pelvis travel (start->end and direction: fwd = +Y of the clip's root at t0, side, back), number of
# foot plants (ball within 4 cm of the floor for >= 0.1 s, alternating feet), first stepping foot, hand lowest height (hands to floor).
import unreal as u, math
AR=u.AssetRegistryHelpers.get_asset_registry(); X=u.AnimPoseExtensions; W=u.AnimPoseSpaces.WORLD; o=[]
opt=u.AnimPoseEvaluationOptions(); opt.set_editor_property('extract_root_motion',True)
KEY=('stumble','trip','stagger','push','hit','react','knock','fall','floor','ground','lie','lying','prone','supine','getup','get_up','standup','stand_up','trans_stand','drunk','slip','injured','dodge','bump','death','die')
f=u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine','AnimSequence')],package_paths=['/Game'],recursive_paths=True); seen=set()
for ad in AR.get_assets(f):
    n=str(ad.asset_name); pk=str(ad.package_name); nl=n.lower()
    if not any(k in nl for k in KEY) or any(x in pk for x in ('/QA/','/Codex','/CharacterLab/','Backup','Facial','Face','_Mirror','NoRM')): continue
    if n in seen: continue
    seen.add(n)
    try:
        s=u.load_asset(pk); d=s.get_play_length()
        if d<0.3 or d>14: continue
        sk=s.get_skeleton().get_name(); N=int(d*20); P=[]
        for k in range(N+1):
            t=min(k/20.0,d); p=X.get_anim_pose_at_time(s,t,opt); g=lambda b:X.get_bone_pose(p,b,W).translation
            P.append((t,g('pelvis'),g('ball_l'),g('ball_r'),g('hand_l'),g('hand_r'),g('head')))
        pz=[q[1].z for q in P]; p0=P[0][1]; p1=P[-1][1]; dx=p1.x-p0.x; dy=p1.y-p0.y
        plants=[]; 
        for side,ix in (('L',2),('R',3)):
            on=False; st=0
            for q in P:
                lo=q[ix].z<6
                if lo and not on: on=True; st=q[0]
                if not lo and on:
                    on=False
                    if q[0]-st>=0.1: plants.append((st,side))
        plants.sort(); seq=''.join(x[1] for x in plants)
        hand=min(min(q[4].z,q[5].z) for q in P)
        o.append('%-46s %-20s len %5.2f rm %-5s | pelvis z %3.0f min %3.0f end %3.0f | travel fwd(Y) %5.0f side(X) %5.0f | plants %-10s | hands min z %3.0f | %s'%(n,sk[:20],d,str(s.get_editor_property('enable_root_motion')),pz[0],min(pz),pz[-1],dy,dx,seq[:10],hand,pk.rsplit('/',2)[-2][:22]))
    except Exception as e: o.append(n+' ERR '+repr(e)[:80])
open(u.Paths.project_dir()+'Saved/UE59Work/r7/react7.txt','w',encoding='utf8').write('\n'.join(sorted(o))); print('REACT7',len(o))
