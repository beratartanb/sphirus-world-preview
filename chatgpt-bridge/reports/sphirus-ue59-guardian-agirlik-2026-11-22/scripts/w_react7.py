# w_react7.py (write, gated; manifest --new lists the created packages) - round 7. VISIBLE STAGGER source clips.
# Core Motion am_Stand_ReactBumpLight_{Front,FrontLeft,FrontRight,Back,BackLeft,BackRight} (SK_MCPaul_Skeleton, real recovery steps: front
# bump -> 90 cm back with one step, back bump -> 115 cm forward with two steps) retargeted to the driver skeleton with the existing
# RTG_Sph_CM_to_UEFN (its Root Motion op writes the travel into the root bone) into /Game/Sphirus/Player/Anim/React (vendor clips untouched).
# Then per copy: root motion ON (lock RefPose, not forced) so the montage carries the capsule with the steps (no foot slide), and
# contact_l / contact_r curves baked from the clip's own feet (raw convention 1 = planted: ball below 7 cm and moving < 35 cm/s, else 0) because GASP
# FootPlacement plants feet from these curves (a clip without them keeps both feet locked = the steps would be pinned).
import unreal as u, math
SRC = ['/Game/MC_Core_Motion/Animations/ReactBump/am_Stand_ReactBumpLight_' + d for d in ('Front', 'FrontLeft', 'FrontRight', 'Back', 'BackLeft', 'BackRight')]
DST = '/Game/Sphirus/Player/Anim/React'; o = []
rtg = u.load_asset('/Game/Sphirus/Player/GASP/CM/Rig/RTG_Sph_CM_to_UEFN'); sm = u.load_asset('/Game/MC_Core_Motion/Demo/Characters/MCHeath/Meshes/SKM_MCHeath')
tm = u.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin'); ar = u.AssetRegistryHelpers.get_asset_registry()
ads = [ar.get_asset_by_object_path(p + '.' + p.split('/')[-1]) for p in SRC]
if not all(u.EditorAssetLibrary.does_asset_exist(DST + '/SphR_' + p.split('/')[-1]) for p in SRC):
    res = u.IKRetargetBatchOperation.duplicate_and_retarget(ads, sm, tm, rtg, '', '', 'SphR_', '', DST, False, False, True)
    o.append('RETARGETED ' + ', '.join(str(x.package_name).split('/')[-1] for x in res))
X = u.AnimPoseExtensions; L = u.AnimationLibrary; W = u.AnimPoseSpaces.WORLD
opt = u.AnimPoseEvaluationOptions(); opt.set_editor_property('extract_root_motion', False)
for p in SRC:
    n = 'SphR_' + p.split('/')[-1]; a = u.load_asset(DST + '/' + n)
    if not a: o.append('MISSING ' + n); continue
    L.set_root_motion_enabled(a, True); L.set_root_motion_lock_type(a, u.RootMotionRootLock.REF_POSE); L.set_is_root_motion_lock_forced(a, False)
    d = a.get_play_length(); dt = 1.0 / 30; N = int(d / dt) + 1; T = []; C = {'contact_l': [], 'contact_r': []}; prev = None
    for k in range(N):
        t = min(k * dt, d); ps = X.get_anim_pose_at_time(a, t, opt); bl = X.get_bone_pose(ps, 'ball_l', W).translation; br = X.get_bone_pose(ps, 'ball_r', W).translation
        T.append(t)
        for key, b, pi in (('contact_l', bl, 0), ('contact_r', br, 1)):
            spd = 0.0 if prev is None else math.hypot(b.x - prev[pi].x, b.y - prev[pi].y) / dt
            C[key].append(1.0 if (b.z < 7.0 and spd < 35.0) else 0.0)   # raw clip convention: 1 = planted (RemapCurves turns it into the game's 0..100)
        prev = (bl, br)
    for key in C:
        if L.does_curve_exist(a, key, u.RawCurveTrackTypes.RCT_FLOAT): L.remove_curve(a, key, False)
        L.add_curve(a, key, u.RawCurveTrackTypes.RCT_FLOAT, False); L.add_float_curve_keys(a, key, T, C[key])
    rt0 = X.get_bone_pose(X.get_anim_pose_at_time(a, 0.0, opt), 'root', W).translation; rt1 = X.get_bone_pose(X.get_anim_pose_at_time(a, d, opt), 'root', W).translation
    o.append('%s len %.2f | root travel (%.0f, %.0f) | planted frames L %d R %d of %d | rm %s | SAVE %s' % (n, d, rt1.x - rt0.x, rt1.y - rt0.y, C['contact_l'].count(1.0), C['contact_r'].count(1.0), N,
             L.is_root_motion_enabled(a), u.EditorAssetLibrary.save_loaded_asset(a, False)))
for n in ('M_Neutral_Jump_F_Land_Stumble_Lfoot', 'M_Neutral_Jump_F_Land_Stumble_Rfoot'):
    a = u.load_asset('/Game/Characters/UEFN_Mannequin/Animations/Jump/' + n); d = a.get_play_length(); row = []
    for k in range(0, int(d * 10) + 1):
        t = min(k / 10.0, d); ps = X.get_anim_pose_at_time(a, t, opt); r = X.get_bone_pose(ps, 'root', W).translation; pl = X.get_bone_pose(ps, 'pelvis', W).translation
        try: c = (X.get_curve_weight(ps, 'contact_l'), X.get_curve_weight(ps, 'contact_r'))
        except Exception: c = (-1, -1)
        row.append('%.1f:r(%.0f,%.0f,%.0f)p%.0f c%.0f/%.0f' % (t, r.x, r.y, r.z, pl.z, c[0], c[1]))
    o.append(n + ' ' + ' '.join(row))
open(u.Paths.project_dir() + 'Saved/UE59Work/r7/react7_build.txt', 'w', encoding='utf8').write('\n'.join(o)); print('REACT7B', len(o))
print('DIRTY', [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()][:8])
