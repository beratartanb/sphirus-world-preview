import unreal as u, re
AR=u.AssetRegistryHelpers.get_asset_registry(); o=[]
f=u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine','AnimSequence'),u.TopLevelAssetPath('/Script/Engine','AnimMontage')],package_paths=['/Game'],recursive_paths=True)
rx=re.compile(r'(ReactBump|Knockdown|DropToFloor|GetUp|ProneCrawl.*Stand|KneelB_Trans_Stand|A_CP2_Bump|Stumble|Trip|LandRecovery|ragdoll_poses|KneelB_Idle_01$|Stand_To_Kneel|Trans_KneelB)',re.I)
drv=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP').get_editor_property('target_skeleton')
o.append('DRIVER SKELETON '+drv.get_path_name())
for ad in AR.get_assets(f):
    n=str(ad.asset_name)
    if not rx.search(n): continue
    a=u.load_asset(str(ad.package_name)); sk=a.get_editor_property('skeleton') if hasattr(a,'get_editor_property') else None
    try: rm=a.get_editor_property('enable_root_motion')
    except Exception: rm='?'
    o.append('%s | %s | len %.2f | skel %s%s | rm %s'%(ad.package_name,ad.asset_class_path.asset_name,a.get_play_length(),sk.get_name() if sk else None,' SAME' if sk==drv else '',rm))
b=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'); T=u.BlueprintToolset
c=u.get_default_object(b.generated_class())
o.append('BODY VARS '+' '.join(x for x in dir(c) if re.match(r'^(ra|r_|reach|hand|ik)',x,re.I))[:1500])
open(u.Paths.project_dir()+'Saved/UE59Work/r5/react.txt','w',encoding='utf8').write('\n'.join(o)); print('REACT',len(o))
