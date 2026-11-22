# w_fallroot6.py (write, gated): root handling of the retargeted fall / get-up clips. Their root bone travels (fall +75 cm, get-up clip is
# authored 333 cm away from the origin); played in a slot the visible body left the capsule (c6b_log_run: pelvis 324 cm from the capsule).
# Root motion OFF (an enabled clip's montage root motion replaced the capsule velocity: the body stopped on the log, v6a_log_sprint)
# + root locked at zero (forced): the pose stays over the capsule, the capsule's travel is owned by the contact system.
import unreal as u
L=u.AnimationLibrary; X=u.AnimPoseExtensions; opt=u.AnimPoseEvaluationOptions(); opt.set_editor_property('extract_root_motion',False)
for n in ('SphF_am_Stand_Trans_ProneCrawl','SphF_am_ProneCrawl_Trans_Stand','SphF_am_InjuredBelly_DropToFloor','SphF_am_InjuredBelly_DropToFloor_GetUp'):
    a=u.load_asset('/Game/Sphirus/Player/Anim/Fall/'+n)
    L.set_root_motion_enabled(a,False); L.set_root_motion_lock_type(a,u.RootMotionRootLock.ZERO); L.set_is_root_motion_lock_forced(a,True)
    print('FALLROOT',n,L.is_root_motion_enabled(a),L.get_root_motion_lock_type(a),L.is_root_motion_lock_forced(a),u.EditorAssetLibrary.save_loaded_asset(a,False))
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()][:8])
