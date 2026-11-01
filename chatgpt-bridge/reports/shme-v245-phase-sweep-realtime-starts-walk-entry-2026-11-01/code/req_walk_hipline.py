import unreal as u, json, math, pathlib, sys, importlib, builtins
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary
seq = u.load_asset('/Game/GraceRanger/Animations/LocomotionBehavior/A_LB_Walk_Fwd'); NAMES = [str(n) for n in AL.get_animation_track_names(seq)]; N = ae.num_frames(seq)
L = ae.read_local(seq, NAMES, list(range(N))); local = {b: [L[b][f] for f in range(N)] for b in NAMES}
clip = ae.Clip(seq, ['root', 'pelvis', 'thigh_l', 'thigh_r', 'clavicle_l', 'clavicle_r', 'spine_05'])
def yaw(a, b): return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
def wrap(a): return (a + 180) % 360 - 180
hip = [yaw(clip.comp('thigh_r', f, local)[0], clip.comp('thigh_l', f, local)[0]) for f in range(N)]
cla = [yaw(clip.comp('clavicle_r', f, local)[0], clip.comp('clavicle_l', f, local)[0]) for f in range(N)]
p2p = lambda a: round(max(a) - min(a), 2)
print('HIPLINE245 ' + json.dumps({'hip_line_p2p': p2p([wrap(h - hip[0]) for h in hip]), 'clav_line_p2p': p2p([wrap(c - cla[0]) for c in cla]), 'counter_p2p': p2p([wrap(c - h) for c, h in zip(cla, hip)]), 'hip_series': [round(wrap(h - hip[0]), 1) for h in hip[::5]]}))
