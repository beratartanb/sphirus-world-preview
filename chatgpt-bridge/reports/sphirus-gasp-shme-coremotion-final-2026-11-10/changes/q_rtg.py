# q_rtg.py (read-only): retarget chains of the UEFN->MH retargeter and both IK rigs; MH chains used by RTG_Sph_Core_to_MH2.
import unreal as u
for ikp in ['/Game/Characters/UEFN_Mannequin/Rigs/IK_UEFN_Mannequin','/Game/MetaHumans/Common/Common/Rigs/IK_Metahuman_Retarget','/MetaHumanCharacter/Animation/Retargeting/IK_MH_IKRig']:
    ik=u.load_asset(ikp); c=u.IKRigController.get_controller(ik)
    try:
        ch=c.get_retarget_chains(); print('IK',ikp.split('/')[-1],'root',c.get_retarget_root())
        for x in ch: print('   CHAIN',x.get_editor_property('chain_name'),x.get_editor_property('start_bone').get_editor_property('bone_name'),'->',x.get_editor_property('end_bone').get_editor_property('bone_name'),'goal',x.get_editor_property('ik_goal_name'))
    except Exception as e: print('IK ERR',ikp,str(e)[:200])
rc=u.IKRetargeterController.get_controller(u.load_asset('/Game/Sphirus/Player/GASP/Rig/RTG_Sph_UEFN_to_MH'))
print('RC methods',[m for m in dir(rc) if not m.startswith('_')])
