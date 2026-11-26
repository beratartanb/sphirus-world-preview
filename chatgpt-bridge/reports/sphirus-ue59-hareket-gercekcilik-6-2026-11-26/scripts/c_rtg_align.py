# c_rtg_align.py (control/write, in memory): target retarget pose of RTG_Sph_UEFN_to_MH - backup of every bone rotation offset to
# Saved/UE59Work/b11/rtg_target_pose_orig.json (first run only), then builtins.RTG_ALIGN = list of bones auto-aligned to the source
# (chain to chain) or 'RESTORE' to write the backup back.
import unreal as u, builtins, json, os
P = u.Paths.project_dir() + 'Saved/UE59Work/b11/rtg_target_pose_orig.json'; T = u.RetargetSourceOrTarget.TARGET
r = u.load_asset('/Game/Sphirus/Player/GASP/Rig/RTG_Sph_UEFN_to_MH'); c = u.IKRetargeterController.get_controller(r)
offs = c.get_retarget_pose_bone_rotation_offsets(c.get_current_retarget_pose_name(T), T)
if not os.path.exists(P):
    json.dump({str(k): [v.x, v.y, v.z, v.w] for k, v in offs.items()}, open(P, 'w')); print('RTGAL backup', len(offs))
mode = getattr(builtins, 'RTG_ALIGN', None)
if mode == 'RESTORE':
    for k, q in json.load(open(P)).items(): c.set_rotation_offset_for_retarget_pose_bone(k, u.Quat(*q), T)
    print('RTGAL restored')
elif mode:
    meth = getattr(builtins, 'RTG_METHOD', 'CHAIN_TO_CHAIN')
    c.auto_align_bones(mode, getattr(u.RetargetAutoAlignMethod, meth), T)
for b in ('clavicle_l', 'upperarm_l', 'lowerarm_l', 'hand_l'):
    q = c.get_rotation_offset_for_retarget_pose_bone(b, T); print('RTGAL', b, [round(q.x, 4), round(q.y, 4), round(q.z, 4), round(q.w, 4)])
