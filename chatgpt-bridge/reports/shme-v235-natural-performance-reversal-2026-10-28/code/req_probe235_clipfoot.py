import unreal as u, sys, pathlib, json
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae
AL = u.AnimationLibrary
out = {}
for path in ['/Game/GraceRanger/SHME/Animations/V235/SHM235_JogRev_F_B_P16', '/Game/GraceRanger/SHME/Animations/V226/SHM226_JogRev_F_B_P14']:
    seq = u.load_asset(path); names = [str(n) for n in AL.get_animation_track_names(seq)]
    nk = ae.num_frames(seq); L = ae.read_local(seq, names, list(range(nk)))
    clip = ae.Clip(seq, ['root', 'pelvis', 'ball_l', 'ball_r', 'foot_l', 'foot_r'])
    rows = []
    for f in range(0, nk, 2):
        rt = L['root'][f][0]; bl = clip.comp('ball_l', f, L)[0]; br = clip.comp('ball_r', f, L)[0]
        rows.append([round(f / 30.0, 2), round(rt[1], 1), round(bl[1], 1), round(bl[2], 1), round(br[1], 1), round(br[2], 1)])
    out[path.rsplit('/', 1)[1]] = rows
print('CLIPFOOT ' + json.dumps(out))
