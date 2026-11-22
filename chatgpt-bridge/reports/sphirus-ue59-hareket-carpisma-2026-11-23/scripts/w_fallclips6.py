# w_fallclips6.py (write, gated; manifest --new lists the created packages): retarget the MC_Sample fall / floor / get-up clips
# (skeleton SKM_MCUE5v2_Skeleton, a superset of the Core Motion MCPaul bone set) onto the driver skeleton SK_UEFN_Mannequin with the
# existing Core Motion -> UEFN retargeter (source IK rig is bone-name based), into /Game/Sphirus/Player/Anim/Fall. Vendor clips untouched.
# Then: root motion ON with the root locked at the reference pose (the body stays over the capsule; the capsule is driven by the
# contact system), curve SphNoFootIK = 1 (no foot placement while lying / kneeling on the floor), contact curves not needed.
import unreal as u, math
SRC = ['/Game/MC_Sample/Animations/ProneCrawl/am_Stand_Trans_ProneCrawl', '/Game/MC_Sample/Animations/ProneCrawl/am_ProneCrawl_Trans_Stand',
       '/Game/MC_Sample/Animations/Injured/am_InjuredBelly_DropToFloor', '/Game/MC_Sample/Animations/Injured/am_InjuredBelly_DropToFloor_GetUp']
DST = '/Game/Sphirus/Player/Anim/Fall'; o = []
rtg = u.load_asset('/Game/Sphirus/Player/GASP/CM/Rig/RTG_Sph_CM_to_UEFN'); sm = u.load_asset('/Game/MC_Sample/Demo/Characters/MCUE5v2/Meshes/SKM_MCUE5Fv2')
tm = u.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin'); ar = u.AssetRegistryHelpers.get_asset_registry()
ads = [ar.get_asset_by_object_path(p + '.' + p.split('/')[-1]) for p in SRC]
have = [p for p in SRC if u.EditorAssetLibrary.does_asset_exist(DST + '/SphF_' + p.split('/')[-1])]
if len(have) < len(SRC):
    res = u.IKRetargetBatchOperation.duplicate_and_retarget(ads, sm, tm, rtg, '', '', 'SphF_', '', DST, False, False, True)
    o.append('RETARGETED ' + ', '.join(str(x.package_name) for x in res))
X = u.AnimPoseExtensions; opt = u.AnimPoseEvaluationOptions(); opt.set_editor_property('extract_root_motion', False); L = u.AnimationLibrary
for p in SRC:
    n = 'SphF_' + p.split('/')[-1]; a = u.load_asset(DST + '/' + n)
    if not a: o.append('MISSING ' + n); continue
    d = a.get_play_length(); row = []
    for k in range(0, 9):
        t = d * k / 8.0; ps = X.get_anim_pose_at_time(a, t, opt); r = X.get_bone_pose(ps, 'root', u.AnimPoseSpaces.WORLD).translation; pl = X.get_bone_pose(ps, 'pelvis', u.AnimPoseSpaces.WORLD).translation; hd = X.get_bone_pose(ps, 'head', u.AnimPoseSpaces.WORLD).translation
        row.append('root(%.0f,%.0f) pel(%.0f,%.0f,%.0f) head(%.0f,%.0f,%.0f)' % (r.x, r.y, pl.x, pl.y, pl.z, hd.x, hd.y, hd.z))
    o.append('%s skel %s len %.2f | %s' % (n, a.get_skeleton().get_name(), d, ' | '.join(row)))
    if not L.does_curve_exist(a, 'SphNoFootIK', u.RawCurveTrackTypes.RCT_FLOAT):
        L.add_curve(a, 'SphNoFootIK', u.RawCurveTrackTypes.RCT_FLOAT, False); L.add_float_curve_keys(a, 'SphNoFootIK', [0.0, d], [1.0, 1.0])
    o.append('SAVE %s %s' % (n, u.EditorAssetLibrary.save_loaded_asset(a, False)))
open(u.Paths.project_dir() + 'Saved/UE59Work/r6/fallclips6.txt', 'w', encoding='utf8').write('\n'.join(o)); print('FALLCLIPS6', len(o))
print('DIRTY', [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()][:12])
