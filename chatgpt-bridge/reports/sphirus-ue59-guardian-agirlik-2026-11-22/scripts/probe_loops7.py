# probe_loops7.py (read-only): RAW locomotion loop clips: pelvis / head vertical p2p, pelvis / head lateral p2p (relative to the root, which
# moves straight), cadence (contact changes per second from contact_l/r), stride (root travel per full cycle), root speed, skeleton.
import unreal as u, math
AR=u.AssetRegistryHelpers.get_asset_registry(); X=u.AnimPoseExtensions; W=u.AnimPoseSpaces.WORLD; o=[]
opt=u.AnimPoseEvaluationOptions(); opt.set_editor_property('extract_root_motion',False)
KEYS=('Walk_Loop_F','Walk_Fwd','Jog_Fwd','Run_Loop_F','Sprint_Loop_F','Walk_Loop_B','Jog_Bwd','Run_Loop_B','Loco_Walk','Loco_Jog','Loco_Run')
f=u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine','AnimSequence')],package_paths=['/Game'],recursive_paths=True)
seen=set()
for ad in AR.get_assets(f):
    n=str(ad.asset_name); pk=str(ad.package_name)
    if not any(k in n for k in KEYS) or 'Start' in n or 'Stop' in n or 'Pivot' in n or 'Turn' in n or 'Lean' in n or 'Crouch' in n: continue
    if any(x in pk for x in ('/QA/','/Codex','/CharacterLab/','Backup','_BAK')): continue
    if n in seen: continue
    seen.add(n)
    try:
        s=u.load_asset(pk); d=s.get_play_length()
        if d<0.4 or d>12: continue
        sk=s.get_skeleton().get_name(); N=int(d*60); pz=[];hz=[];plat=[];hlat=[];cl=[];r0=None;r1=None
        for k in range(N+1):
            t=min(k/60.0,d); p=X.get_anim_pose_at_time(s,t,opt); g=lambda b:X.get_bone_pose(p,b,W).translation
            rt=g('root'); pl=g('pelvis'); hd=g('head')
            if r0 is None: r0=rt
            r1=rt; pz.append(pl.z-rt.z); hz.append(hd.z-rt.z); plat.append(pl.x-rt.x); hlat.append(hd.x-rt.x)
            try: cl.append(X.get_curve_weight(p,'contact_l'))
            except Exception: cl.append(-1)
        dist=math.hypot(r1.x-r0.x,r1.y-r0.y); sp=dist/d if d>0 else 0
        ch=sum(1 for i in range(1,len(cl)) if (cl[i]>0.5)!=(cl[i-1]>0.5)) if min(cl)>=0 else -1
        pp=lambda v:max(v)-min(v)
        o.append('%-44s %-22s len %5.2f speed %4.0f | pelvis z p2p %5.1f head z p2p %5.1f | pelvis lat %5.1f head lat %5.1f | contact changes/s %4.1f | %s'%(n,sk[:22],d,sp,pp(pz),pp(hz),pp(plat),pp(hlat),ch/d if ch>=0 else -1,pk.rsplit('/',1)[0][-34:]))
    except Exception as e: o.append(n+' ERR '+repr(e)[:80])
open(u.Paths.project_dir()+'Saved/UE59Work/r7/loops7.txt','w',encoding='utf8').write('\n'.join(sorted(o))); print('LOOPS7',len(o))
