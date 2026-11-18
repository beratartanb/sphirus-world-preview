# probe_stopclips.py (read-only): root-motion speed profile of the stop clips in the stop databases + AC_Sph_Motion brake defaults.
import unreal as u, math
o = []
R = '/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/'
mc = u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())
for n in ('PhysBrake', 'BrakeDecelLow', 'BrakeDecelHigh', 'BrakeEffortK', 'BrakeDecel', 'BrakeFriction'):
    try: o.append('MOT %s = %s' % (n, mc.get_editor_property(n)))
    except Exception as e: o.append('MOT %s ? %s' % (n, str(e)[:60]))
ar = u.AssetRegistryHelpers.get_asset_registry()
seen = set()
for p in ('Relaxed/PSD_Relaxed_Stand_Sprint_Stops', 'Relaxed/PSD_Relaxed_Stand_Run_Stops', 'Dense/PSD_Dense_Stand_Run_Stops', 'Dense/PSD_Dense_Stand_Sprint_Stops', 'Dense/PSD_Dense_Stand_Walk_Stops'):
    deps = ar.get_dependencies(R.rsplit('/', 1)[0] + '/Databases/' + p if False else '/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/' + p, u.AssetRegistryDependencyOptions())
    for dp in deps or []:
        dp = str(dp)
        if 'Stop' not in dp or dp in seen: continue
        a = u.load_asset(dp)
        if not isinstance(a, u.AnimSequence): continue
        seen.add(dp)
        L = a.get_play_length(); n = int(L * 60)
        opt = u.AnimPoseEvaluationOptions(); 
        pts = []
        for i in range(n + 1):
            t = min(L, i / 60.0); pose = u.AnimPoseExtensions.get_anim_pose_at_time(a, t, opt)
            tr = u.AnimPoseExtensions.get_bone_pose(pose, 'root', u.AnimPoseSpaces.WORLD); pts.append((t, tr.translation.x, tr.translation.y))
        sp = [math.hypot(pts[i + 1][1] - pts[i][1], pts[i + 1][2] - pts[i][2]) * 60 for i in range(len(pts) - 1)]
        v0 = sp[0] if sp else 0; vmax = max(sp) if sp else 0
        tstop = next((pts[i][0] for i in range(len(sp)) if i > 2 and sp[i] < 5), L)
        dist = sum(sp[i] / 60 for i in range(len(sp)) if pts[i][0] < tstop)
        prof = ' '.join('%.0f' % sp[i] for i in range(0, len(sp), 6))
        o.append('CLIP %-42s %-28s len %.2f v0 %4.0f vmax %4.0f stop %.2fs dist %5.1f | %s' % (a.get_name(), p.split('/')[-1], L, v0, vmax, tstop, dist, prof))
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/stopclips.txt', 'w', encoding='utf8').write('\n'.join(o)); print('CLIPS', len(o))
