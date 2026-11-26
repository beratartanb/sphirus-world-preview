# w_save_p14.py (write, gated): pass 6 save - compile player + motion, B14 top/shorts wiring (c_b14g_wire), pass-6 defaults (c_p6_defaults),
# save BP_HybridA_Player, AC_Sph_Motion and RTG_Sph_UEFN_to_MH (arms FK-only + target arm retarget pose auto-aligned, set in memory by
# c_rtg_armfk.py / c_rtg_align.py; verified here before saving).
import unreal as u
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
D = u.Paths.project_dir()
for p in ('/Game/Sphirus/Player/Motion/AC_Sph_Motion', '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'): u.BlueprintEditorLibrary.compile_blueprint(u.load_asset(p))
exec(open(D + 'Tools/UE59_20261126/c_b14g_wire.py', encoding='utf8').read())
exec(open(D + 'Tools/UE59_20261126/c_p6_defaults.py', encoding='utf8').read())
r = u.load_asset('/Game/Sphirus/Player/GASP/Rig/RTG_Sph_UEFN_to_MH'); c = u.IKRetargeterController.get_controller(r)
i = [k for k in range(c.get_num_retarget_ops()) if c.get_op_name(k) == 'Run IK Rig'][0]
ch = [str(x.get_editor_property('target_chain_name')) for x in c.get_op_controller(i).get_settings().get_editor_property('chains') if x.get_editor_property('enable_ik')]  # IK-enabled chains
q = c.get_rotation_offset_for_retarget_pose_bone('upperarm_l', u.RetargetSourceOrTarget.TARGET)
print('SAVEP14 rtg ik chains', ch, 'upperarm_l', [round(q.x, 4), round(q.y, 4), round(q.z, 4), round(q.w, 4)])
assert 'LeftArm' not in ch and abs(q.y - (-0.0503)) < 0.01, 'RTG arm changes not in memory'
for p in ('/Game/Sphirus/Player/Motion/AC_Sph_Motion', '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player', '/Game/Sphirus/Player/GASP/Rig/RTG_Sph_UEFN_to_MH'):
    print('SAVEP14', p.split('/')[-1], u.EditorAssetLibrary.save_loaded_asset(u.load_asset(p), False))
print('DIRTY', [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
