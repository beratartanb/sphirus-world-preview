import unreal as u
o=[]; ar=u.AssetRegistryHelpers.get_asset_registry()
s=u.load_asset('/Game/MC_Sample/Animations/ProneCrawl/am_Stand_Trans_ProneCrawl'); sk=s.get_skeleton(); o.append('SRC SKEL '+sk.get_path_name())
uef=u.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SK_UEFN_Mannequin'); pa=u.load_asset('/Game/MC_Core_Motion/Animations/Kneel/am_KneelB_Idle_01').get_skeleton(); o.append('PAUL SKEL '+pa.get_path_name())
def bones(k):
    try: return [str(x) for x in k.get_reference_pose().get_bone_names()]
    except Exception as e: return ['ERR '+repr(e)[:80]]
b1=bones(sk); b2=bones(uef); b3=bones(pa)
o.append('n src %d uefn %d paul %d'%(len(b1),len(b2),len(b3))); o.append('src not in paul: '+' '.join([b for b in b1 if b not in b3][:40])); o.append('paul not in src: '+' '.join([b for b in b3 if b not in b1][:40]))
o.append('src first: '+' '.join(b1[:30]))
for ad in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine','SkeletalMesh')):
    p=str(ad.package_name)
    if '/MC_Sample/' in p or '/MC_Core_Motion/' in p: o.append('MESH '+p+' skel '+str(ad.get_tag_value('Skeleton')))
r=u.load_asset('/Game/Sphirus/Player/GASP/CM/Rig/RTG_Sph_CM_to_UEFN'); c=u.IKRetargeterController.get_controller(r)
for k in (u.RetargetSourceOrTarget.SOURCE,u.RetargetSourceOrTarget.TARGET):
    try: o.append('RTG %s rig %s mesh %s'%(k,c.get_ik_rig(k).get_path_name(),c.get_preview_mesh(k).get_path_name() if c.get_preview_mesh(k) else None))
    except Exception as e: o.append('rtg err '+repr(e)[:120])
o.append('BATCH '+str(u.IKRetargetBatchOperation.duplicate_and_retarget.__doc__)[:900])
for p in ('/Game/MC_Sample/Animations/ProneCrawl/am_Stand_Trans_ProneCrawl','/Game/MC_Sample/Animations/ProneCrawl/am_ProneCrawl_Trans_Stand','/Game/MC_Sample/Animations/Injured/am_InjuredBelly_DropToFloor','/Game/MC_Sample/Animations/Injured/am_InjuredBelly_DropToFloor_GetUp'):
    a=u.load_asset(p); o.append('%s len %.2f rm %s'%(p.split('/')[-1],a.get_play_length(),a.get_editor_property('enable_root_motion')))
open(u.Paths.project_dir()+'Saved/UE59Work/r6/rtg_probe.txt','w',encoding='utf8').write('\n'.join(o)); print('RTGPROBE',len(o))
