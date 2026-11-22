# probe_starts6.py (read-only): start clips of every style - deepest pelvis drop (cm below the first frame), largest trunk pitch
# (pelvis->neck_01 against vertical, deg), time to reach 90 % of the end speed, in the first 1.2 s. Picks the least athletic source.
import unreal as u, math
AR=u.AssetRegistryHelpers.get_asset_registry(); X=u.AnimPoseExtensions; o=[]
f=u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine','AnimSequence')],package_paths=['/Game/Characters/UEFN_Mannequin','/Game/Sphirus/Player'],recursive_paths=True)
opt=u.AnimPoseEvaluationOptions(); opt.set_editor_property('extract_root_motion',True)
for ad in AR.get_assets(f):
    n=str(ad.asset_name)
    if not ('Start_F' in n and ('Lfoot' in n or 'Rfoot' in n or n.endswith('Start_F')) ) or 'Reface' in n or 'Crouch' in n: continue
    s=u.load_asset(str(ad.package_name)); d=min(s.get_play_length(),1.3); z0=None; dz=0; ln=0; t90=None; mdl=[]
    for k in range(int(d*30)+1):
        t=k/30.0; p=X.get_anim_pose_at_time(s,t,opt); pl=X.get_bone_pose(p,'pelvis',u.AnimPoseSpaces.WORLD).translation; nk=X.get_bone_pose(p,'neck_01',u.AnimPoseSpaces.WORLD).translation
        if z0 is None: z0=pl.z
        dz=max(dz,z0-pl.z); v=(nk.x-pl.x,nk.y-pl.y,nk.z-pl.z); ln=max(ln,math.degrees(math.atan2(math.hypot(v[0],v[1]),v[2])))
        try: mdl.append(X.get_curve_weight(p,'movedata_speed'))
        except Exception: mdl.append(0)
    end=mdl[-1] if mdl else 0
    for k,m in enumerate(mdl):
        if end>1 and m>=0.9*end: t90=k/30.0; break
    o.append('%-44s len %.2f | pelvis drop %5.1f cm | max trunk pitch %5.1f deg | speed at 1.3 s %3.0f, 90%% at %s s | %s'%(n,s.get_play_length(),dz,ln,end,('%.2f'%t90) if t90 is not None else '-',str(ad.package_path).split('/')[-1]))
open(u.Paths.project_dir()+'Saved/UE59Work/r6/starts6.txt','w',encoding='utf8').write('\n'.join(sorted(o))); print('STARTS6',len(o))
