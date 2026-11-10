# q_gasp2.py (read-only): Sphirus player component tree + retarget assets.
import unreal as u
SD=u.SubobjectDataBlueprintFunctionLibrary
def tree(path):
    bp=u.load_asset(path); scs=u.get_engine_subsystem(u.SubobjectDataSubsystem)
    for d in scs.k2_gather_subobject_data_for_blueprint(bp):
        o=SD.get_object(SD.get_data(d))
        if not o: continue
        x=o.get_name()+' '+type(o).__name__
        if isinstance(o,u.SceneComponent):
            pa=o.get_attach_parent(); x+=' parent=%s'%(pa.get_name() if pa else None)
        if isinstance(o,u.SkeletalMeshComponent):
            m=o.get_editor_property('skeletal_mesh_asset'); ac=o.get_editor_property('anim_class')
            x+=' mesh=%s skel=%s anim=%s vis=%s hig=%s lpc=%s'%(m.get_path_name() if m else None, m.get_editor_property('skeleton').get_path_name() if m else None, ac.get_name() if ac else None, o.get_editor_property('visible'), o.get_editor_property('hidden_in_game'), o.get_editor_property('leader_pose_component').get_name() if o.get_editor_property('leader_pose_component') else None)
        print('SCS',x)
tree('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player')
for r in ['/Game/MetaHumans/Common/Common/Rigs/RTG_UEFN_to_Metahuman_nrw','/Game/Sphirus/Player/Rig/RTG_Sph_Core_to_MH2']:
    a=u.load_asset(r)
    for k in ('source_ik_rig_asset','target_ik_rig_asset','source_preview_mesh','target_preview_mesh'):
        try: v=a.get_editor_property(k); print('RTG',r.split('/')[-1],k,v.get_path_name() if v else None)
        except Exception as e: print('RTG',r.split('/')[-1],k,'ERR',str(e)[:60])
for r in ['/Game/MetaHumans/Common/Common/Rigs/IK_Metahuman_Retarget','/Game/Characters/UEFN_Mannequin/Rigs/IK_UEFN_Mannequin']:
    a=u.load_asset(r)
    try: m=a.get_preview_mesh(); print('IK',r.split('/')[-1],'preview',m.get_path_name() if m else None, 'skel', m.get_editor_property('skeleton').get_path_name() if m else None)
    except Exception as e: print('IK',r,'ERR',str(e)[:80])
