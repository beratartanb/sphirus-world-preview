# probe_r2w.py (read-only): arm carriage of run->walk transition clips vs walk loops. Per 0.1 s: hand height above spine_05 and
# forward hand offset (component space, cm), elbow angle, upper-arm abduction (angle of upperarm->lowerarm from the body's
# down axis in the frontal plane), root speed. Also lists the clips in the walk forward loop DB used in game.
import unreal as u, math
O = []
db = u.load_asset('/Game/Sphirus/Player/GASP/DB/PSD_Sph_N_Walk_F_Loops')
try:
    for i in range(u.PoseSearchDatabase.get_num_animation_assets(db) if hasattr(u.PoseSearchDatabase, 'get_num_animation_assets') else 0): pass
except Exception: pass
try:
    O.append('DB anims: ' + ', '.join(str(e.get_editor_property('animation_asset').get_name()) for e in db.get_editor_property('animation_assets')))
except Exception as e: O.append('DB list err %r' % e)
clips = ['/Game/Characters/UEFN_Mannequin/Animations/Walk/M_Neutral_Transition_Run_to_Walk_Lfoot', '/Game/Characters/UEFN_Mannequin/Animations/Walk/M_Neutral_Transition_Run_to_Walk_Rfoot',
         '/Game/Characters/UEFN_Mannequin/Animations/Walk/M_Relaxed_Transition_Run_to_Walk_Lfoot', '/Game/Characters/UEFN_Mannequin/Animations/Walk/M_Relaxed_Transition_Run_to_Walk_Rfoot']
for nm in ('M_Neutral_Walk_Loop_F', 'M_Relaxed_Walk_Loop_F', 'M_Neutral_Run_Loop_F'):
    r = u.EditorAssetLibrary.list_assets('/Game/Characters/UEFN_Mannequin/Animations', recursive=True)
    clips += [p.split('.')[0] for p in r if p.split('.')[-1] == nm][:1]
opt = u.AnimPoseEvaluationOptions()
def pos(p, b): t = u.AnimPoseExtensions.get_bone_pose(p, b, u.AnimPoseSpaces.WORLD); return t.translation
for c in clips:
    s = u.load_asset(c); L = s.get_play_length(); O.append('== %s len %.2f' % (c.split('/')[-1], L)); t = 0.0; prev = None
    while t <= L + 1e-4:
        p = u.AnimPoseExtensions.get_anim_pose_at_time(s, t, opt)
        sp = pos(p, 'spine_05'); rt = pos(p, 'root'); row = []
        for sd in ('l', 'r'):
            h = pos(p, 'hand_' + sd); ua = pos(p, 'upperarm_' + sd); la = pos(p, 'lowerarm_' + sd)
            e1 = ua - la; e2 = h - la
            ang = math.degrees(math.acos(max(-1, min(1, (e1.x*e2.x+e1.y*e2.y+e1.z*e2.z) / max(1e-3, e1.length()*e2.length())))))
            d = la - ua; abd = math.degrees(math.atan2(abs(d.x), -d.z))   # mannequin: x lateral, y forward, z up
            row.append('%s hz %5.1f fwd %5.1f elb %4.0f abd %4.0f' % (sd, h.z - sp.z, h.y - sp.y, ang, abd))
        sp_ = '' if prev is None else '%4.0f' % ((rt - prev).length() / 0.1)
        prev = rt
        O.append('  t %.1f root %s | %s' % (t, sp_, ' | '.join(row))); t += 0.1
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/r2w.txt', 'w').write('\n'.join(O)); print('R2W', len(O))
