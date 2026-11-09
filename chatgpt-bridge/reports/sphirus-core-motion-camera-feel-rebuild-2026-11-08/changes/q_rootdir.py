# q_rootdir.py (measure): direction of the Core Motion clips' root motion in mesh space (does MCPaul walk along +X or +Y
# in its own space?) versus the driver mesh component rotation (-90 yaw, mannequin convention). A mismatch rotates the
# motion-matching query trajectory relative to the database trajectories.
import unreal as u, math
opt=u.AnimPoseEvaluationOptions(); opt.set_editor_property('evaluation_type',u.AnimDataEvalType.RAW); opt.set_editor_property('extract_root_motion',False)
C='/Game/Sphirus/Player/Anim/Core/'
for n in ('af_Loco_Walk_Fwd','af_Loco_Run_Fwd','af_Loco_Walk_FwdLeft','af_Stand_Idle_TurnR090'):
    a=u.load_asset(C+n); L=float(a.get_play_length()); rows=[]
    for t in (0.0,0.5,1.0,min(L-0.01,1.5)):
        pose=u.AnimPoseExtensions.get_anim_pose_at_time(a,t,opt); r=u.AnimPoseExtensions.get_bone_pose(pose,'root',u.AnimPoseSpaces.WORLD); p=u.AnimPoseExtensions.get_bone_pose(pose,'pelvis',u.AnimPoseSpaces.WORLD)
        fw=u.MathLibrary.get_forward_vector(p.rotation.rotator()); rows.append((t,round(r.translation.x),round(r.translation.y),round(r.rotation.rotator().yaw),'pelvisfwd',(round(fw.x,2),round(fw.y,2),round(fw.z,2))))
    print('ROOT',n,rows)
    print('  flags',n,'root_motion',a.get_editor_property('enable_root_motion'),'lock',a.get_editor_property('root_motion_root_lock'),'force_lock',a.get_editor_property('force_root_lock'))
sk=u.load_asset('/Game/MC_Core_Motion/Demo/Characters/MCPaul/Meshes/SKM_MCPaul'); print('MESH bounds',sk.get_bounds().box_extent if hasattr(sk,'get_bounds') else None)
bp=u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); cdo=u.get_default_object(bp.generated_class())
print('DRIVER rot',cdo.get_editor_property('mesh').get_editor_property('relative_rotation'))
for c in cdo.get_editor_property('mesh').get_editor_property('attach_children') if False else []: pass
print('Q_DONE')
