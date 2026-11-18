import unreal as u
o = []
for p in ('/Game/Sphirus/Player/GASP/DB/PSD_Sph_N_Walk_F_Turns', '/Game/Sphirus/Player/GASP/DB/PSD_Sph_N_Walk_F_Pivots', '/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_Walk_F_Turns', '/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Dense/PSD_Dense_Stand_Walk_Pivots'):
    d = u.load_asset(p); o.append('## %s n %d' % (p.split('/')[-1], d.get_num_animation_assets()))
    o.append('   ' + ', '.join(sorted(d.get_animation_asset(i).get_name() for i in range(d.get_num_animation_assets()) if d.get_animation_asset(i))))
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/turndb.txt', 'w').write('\n'.join(o)); print('TURNDB', len(o))
