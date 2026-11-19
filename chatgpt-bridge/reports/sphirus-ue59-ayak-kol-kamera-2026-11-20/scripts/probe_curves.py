# probe_curves.py (read-only): float curve names on stop / walk / transition clips used in game; sample Distance-like curves.
import unreal as u
B = '/Game/Characters/UEFN_Mannequin/Animations/'
names = ['Walk/M_Relaxed_Walk_Stop_F_Rfoot', 'Walk/M_Relaxed_Walk_Stop_F_Lfoot', 'Run/M_Relaxed_Run_Stop_F_Rfoot', 'Run/M_Neutral_Run_Stop_F_Rfoot', 'Run/M_Neutral_Run_Stop_F_Lfoot', 'Walk/M_Neutral_Transition_Run_to_Walk_Lfoot', 'Walk/M_Relaxed_Transition_Run_to_Walk_Lfoot']
o = []
ar = u.EditorAssetLibrary.list_assets(B, recursive=True)
for n in names:
    leaf = n.split('/')[-1]; p = [x.split('.')[0] for x in ar if x.split('.')[-1] == leaf]
    if not p: o.append('MISSING ' + n); continue
    s = u.load_asset(p[0]); cn = [str(c) for c in u.AnimationLibrary.get_animation_curve_names(s, u.RawCurveTrackTypes.RCT_FLOAT)]
    o.append('== %s %s len %.2f curves: %s' % (leaf, p[0], s.get_play_length(), ', '.join(cn)))
    for c in cn:
        if any(k in c.lower() for k in ('dist', 'contact', 'speed', 'root')):
            ts, vs = u.AnimationLibrary.get_float_keys(s, c)
            step = max(1, len(vs) // 25)
            o.append('   %s n=%d : %s' % (c, len(vs), ' '.join('%.0f@%.2f' % (vs[i], ts[i]) for i in range(0, len(vs), step))))
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/curves.txt', 'w').write('\n'.join(o)); print('CV', len(o))
