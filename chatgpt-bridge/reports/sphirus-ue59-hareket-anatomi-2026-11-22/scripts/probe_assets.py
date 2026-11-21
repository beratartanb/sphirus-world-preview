# probe_assets.py (read-only): animation / physics assets usable for stagger, hit reaction, fall, get-up, brace, jump, carry
import unreal as u, re
AR=u.AssetRegistryHelpers.get_asset_registry(); o=[]
pat=re.compile(r'(stagger|stumbl|hit_?react|hitreact|knock|fall|getup|get_up|standup|trip|brace|push|lean|wall|bump|flinch|land|recover|slip|collapse|kneel|prone|supine|ragdoll)',re.I)
f=u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine','AnimSequence'),u.TopLevelAssetPath('/Script/Engine','AnimMontage')],package_paths=['/Game'],recursive_paths=True)
by={}
for ad in AR.get_assets(f):
    n=str(ad.asset_name)
    if pat.search(n): by.setdefault(str(ad.package_path),[]).append(n)
for p,l in sorted(by.items()): o.append('%s (%d): %s'%(p,len(l),', '.join(sorted(l))[:700]))
f2=u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine','PhysicsAsset')],package_paths=['/Game'],recursive_paths=True)
o.append('PHYSICS ASSETS: '+', '.join(sorted(str(a.package_name) for a in AR.get_assets(f2)))[:1500])
m=u.load_asset('/Game/Sphirus/CharacterLab/Sph_20261108/Built/MHC_Sph8/Body/SKM_MHC_Sph8_BodyMesh'); pa=m.get_editor_property('physics_asset'); o.append('BODY physics asset: %s'%(pa.get_path_name() if pa else None))
d=u.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin'); pa=d.get_editor_property('physics_asset'); o.append('DRIVER physics asset: %s'%(pa.get_path_name() if pa else None))
tot={}
for ad in AR.get_assets(f):
    tot[str(ad.package_path).split('/')[2] if str(ad.package_path).count('/')>1 else '?']=tot.get(str(ad.package_path).split('/')[2] if str(ad.package_path).count('/')>1 else '?',0)+1
o.append('ANIM COUNTS by top folder: '+str(tot))
open(u.Paths.project_dir()+'Saved/UE59Work/r5/assets.txt','w',encoding='utf8').write('\n'.join(o)); print('ASSETS',len(o))
