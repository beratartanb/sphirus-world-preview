# w_ledge_root.py (write, gated): restores root motion on the retargeted AAMS ledge copies (SphL_*). The batch retarget (RTG_UE5_to_UEFN)
# moved the source root motion into the pelvis and left the root track at zero, so a mantle would snap the body back 1-2 m when it ends.
# Per frame: root_copy(t) = source root translation(t) * s, s = (copy pelvis travel) / (source pelvis travel) over the clip (skeleton
# size ratio); pelvis local translation(t) -= root_copy(t) (root rotation stays identity in these clips - checked: yaw drift printed).
import unreal as u, math
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
SRC = '/Game/AAMS/AAMS/Animations/'; DST = '/Game/Sphirus/Player/Anim/Ledge/SphL_'
CL = {'AS_Ledge_Braced_Mantle': 'Ledge/Braced/', 'AS_Ledge_Braced_FallToBracedIdle': 'Ledge/Braced/', 'AS_Ledge_Braced_StandToBracedIdle': 'Ledge/Braced/',
      'AS_Ledge_Braced_Jump_Down': 'Ledge/Braced/', 'AS_Ledge_Braced_StandDropToIdle': 'Ledge/Braced/', 'AS_Ledge_Braced_Jump_Up': 'Ledge/Braced/',
      'AS_Ledge_Braced_Left': 'Ledge/Braced/', 'AS_Ledge_Braced_Right': 'Ledge/Braced/', 'AS_Ledge_Braced_Jump_Back': 'Ledge/Braced/',
      'AS_Vault_MantleJumpUp_1m': 'Vault/', 'AS_Vault_FallToMantle': 'Vault/', 'AS_Vault_MantleStep': 'Vault/'}
L = u.AnimationLibrary
for n, sub in CL.items():
    s = u.load_asset(SRC + sub + n); c = u.load_asset(DST + n); nf = L.get_num_frames(c); nfs = L.get_num_frames(s)
    rs = [L.get_bone_pose_for_frame(s, 'root', min(f, nfs), False) for f in range(nf + 1)]
    if max(abs(r.translation.x) + abs(r.translation.y) + abs(r.translation.z) for r in rs) < 1.0: print('LROOT', n, 'no source root motion'); continue
    ps = [L.get_bone_pose_for_frame(s, 'pelvis', min(f, nfs), False) for f in (0, nfs)]; pc = [L.get_bone_pose_for_frame(c, 'pelvis', f, False) for f in range(nf + 1)]
    def comp(rt, pl): return u.Vector(rt.translation.x + pl.translation.x, rt.translation.y + pl.translation.y, rt.translation.z + pl.translation.z)
    srcd = (comp(rs[-1], ps[1]) - comp(rs[0], ps[0])).length(); cpd = (pc[-1].translation - pc[0].translation).length(); k = cpd / srcd if srcd > 1 else 1.0
    root = [u.Vector(r.translation.x * k, r.translation.y * k, r.translation.z * k) for r in rs]
    yaw = max(abs(r.rotation.rotator().yaw) for r in rs)
    ctl = c.get_editor_property('controller')
    ctl.set_bone_track_keys('root', root, [u.Quat() for _ in root], [u.Vector(1, 1, 1) for _ in root])
    ctl.set_bone_track_keys('pelvis', [p.translation - r for p, r in zip(pc, root)], [p.rotation for p in pc], [p.scale3d for p in pc])
    c.set_editor_property('enable_root_motion', True)
    e = L.get_bone_pose_for_frame(c, 'root', nf, False).translation
    print('LROOT', n, 'frames', nf, 'k %.3f' % k, 'root end (%.0f,%.0f,%.0f)' % (e.x, e.y, e.z), 'src yaw max %.1f' % yaw, 'saved', u.EditorAssetLibrary.save_loaded_asset(c, False))
