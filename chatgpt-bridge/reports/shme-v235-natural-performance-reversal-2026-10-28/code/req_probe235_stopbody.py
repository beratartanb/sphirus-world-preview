import unreal as u, sys, pathlib, json, math
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae
AL = u.AnimationLibrary; out = {}
for path in ['/Game/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop', '/Game/GraceRanger/Animations/Continuity/A_CT_Jog_Fwd']:
    seq = u.load_asset(path); names = [str(n) for n in AL.get_animation_track_names(seq)]
    nk = ae.num_frames(seq); L = ae.read_local(seq, names, list(range(nk)))
    clip = ae.Clip(seq, ['root', 'pelvis', 'spine_05', 'head', 'hand_l', 'hand_r', 'ball_l', 'ball_r', 'calf_l', 'calf_r'])
    rows = []
    for f in range(nk):
        c = {b: clip.comp(b, f, L)[0] for b in ('root', 'pelvis', 'spine_05', 'head', 'hand_l', 'hand_r', 'ball_l', 'ball_r', 'calf_l', 'calf_r')}
        rel = lambda b, o='pelvis': [round(c[b][i] - c[o][i], 1) for i in range(3)]
        rows.append({'t': round(f / 30.0, 3), 'root_y': round(c['root'][1], 1), 'pel_z': round(c['pelvis'][2], 1), 'hl': rel('hand_l'), 'hr': rel('hand_r'),
                     'head_y': round(c['head'][1] - c['pelvis'][1], 1), 'bl': [round(c['ball_l'][1] - c['root'][1], 1), round(c['ball_l'][2], 1)], 'br': [round(c['ball_r'][1] - c['root'][1], 1), round(c['ball_r'][2], 1)],
                     'kl': round(c['calf_l'][2], 1), 'kr': round(c['calf_r'][2], 1)})
    out[path.rsplit('/', 1)[1]] = rows
json.dump(out, open(str(P / 'Saved/Codex/SHME_V235_20261028/stopbody235.json'), 'w'))
print('STOPBODY ok', {k: len(v) for k, v in out.items()})
