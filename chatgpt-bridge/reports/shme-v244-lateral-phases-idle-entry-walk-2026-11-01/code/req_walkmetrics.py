import unreal as u, json, math, pathlib, sys, importlib
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; out = {}
for path in ('/Game/GraceRanger/Animations/LocomotionBehavior/A_LB_Walk_Fwd', '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/Phase275Support/Walk/M_Ranger_Walk_Loop_F_PureForward_CWF'):
    seq = u.load_asset(path)
    if not seq:
        ar = u.AssetRegistryHelpers.get_asset_registry(); nm = path.split('/')[-1]
        c = [a for a in ar.get_assets_by_path('/Game', True) if str(a.asset_name) == nm]
        if not c: out[nm] = 'NOT FOUND'; continue
        seq = c[0].get_asset(); path = str(c[0].package_name)
    NAMES = [str(n) for n in AL.get_animation_track_names(seq)]; N = ae.num_frames(seq); T = float(seq.get_play_length())
    L = ae.read_local(seq, NAMES, list(range(N)))
    clip = ae.Clip(seq, ['root', 'pelvis', 'spine_03', 'spine_05', 'head', 'hand_l', 'hand_r', 'upperarm_l', 'upperarm_r', 'foot_l', 'foot_r', 'ball_l', 'ball_r', 'thigh_l', 'thigh_r'])
    local = {b: [L[b][f] for f in range(N)] for b in NAMES}
    def yaw_of(q):  # yaw of the bone's forward axis (component space): use x axis
        v = ae.qrot(q, (1.0, 0.0, 0.0)); return math.degrees(math.atan2(v[1], v[0]))
    rows = []
    for f in range(N):
        pp, pq = clip.comp('pelvis', f, local); cp, cq = clip.comp('spine_05', f, local); hp, hq = clip.comp('head', f, local)
        hl = clip.comp('hand_l', f, local)[0]; hr = clip.comp('hand_r', f, local)[0]; rp = clip.comp('root', f, local)[0]
        bl = clip.comp('ball_l', f, local)[0]; br = clip.comp('ball_r', f, local)[0]
        rows.append({'f': f, 'root': rp, 'pel': pp, 'pel_yaw': yaw_of(pq), 'chest_yaw': yaw_of(cq), 'head_yaw': yaw_of(hq), 'hand_l': hl, 'hand_r': hr, 'ball_l': bl, 'ball_r': br})
    root_d = ae.vsub(rows[-1]['root'], rows[0]['root']); speed = ae.vlen(root_d) / T if T else 0
    py = [r['pel_yaw'] for r in rows]; cy = [r['chest_yaw'] for r in rows]; cr = [c - p for c, p in zip(cy, py)]
    def p2p(a): return round(max(a) - min(a), 2)
    pz = [r['pel'][2] for r in rows]; px = [r['pel'][0] - r['root'][0] for r in rows]; pyy = [r['pel'][1] - r['root'][1] for r in rows]
    blz = [r['ball_l'][2] for r in rows]; brz = [r['ball_r'][2] for r in rows]
    out[path.split('/')[-1]] = {'path': path, 'frames': N, 'len_s': round(T, 3), 'root_speed': round(speed, 1), 'root_dir': [round(x, 2) for x in ae.vnorm(root_d)] if speed else None,
        'pelvis_yaw_p2p': p2p(py), 'chest_yaw_p2p': p2p(cy), 'counter_rot_p2p': p2p(cr), 'pelvis_z_p2p': p2p(pz), 'pelvis_lat_p2p': p2p(px), 'pelvis_fwd_p2p': p2p(pyy),
        'ball_l_z_min_max': [round(min(blz), 1), round(max(blz), 1)], 'ball_r_z': [round(min(brz), 1), round(max(brz), 1)],
        'series': {'pel_yaw': [round(x, 1) for x in py], 'chest_yaw': [round(x, 1) for x in cy], 'ball_l_z': [round(x, 1) for x in blz], 'ball_r_z': [round(x, 1) for x in brz],
                   'hand_l_y': [round(r['hand_l'][1] - r['root'][1], 1) for r in rows], 'hand_r_y': [round(r['hand_r'][1] - r['root'][1], 1) for r in rows]}}
pathlib.Path(str(P / 'Saved/Codex/SHME_V244_20261101/data/walkmetrics.json')).write_text(json.dumps(out, indent=1))
print('WALKMET244 ' + json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'series'} if isinstance(v, dict) else v for k, v in out.items()}))
