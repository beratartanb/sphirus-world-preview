"""ao241_copy.py (editor job, write manifest = NEW assets only) - V2.41 regional aim offset: a copy of the vendor aim offset
(/Game/AAMS/.../BS_Neutral_AO_Stand + its 9 mesh-space rotation-offset samples; originals untouched) whose additive no longer carries
the pelvis and legs and only a share of the spine:
  root / pelvis / thigh / calf / foot / ball / ik_* (and their twist bones): every frame := the base frame (X0_Y0 frame 0) -> zero offset
  spine_01..05: slerp(base, sample, SHM241_AO_SPINE = 0.3)            neck_* / head (and everything else): unchanged
Why (V2.40, sphirus-camera-direction): the vendor offset Delta(ControlRotation, Root) turned head, chest AND pelvis toward the camera;
fading the whole offset inside a planned cut moved a planted ball 3 cm in one frame (the pelvis share), so V2.40 could fade it only
after the plan. With the pelvis / legs out of the offset the head can be owned separately from the body. builtins.V241_AO =
{'dry': bool, 'spine': 0.3}. Prints AOC241 {...}."""
import unreal as u, json, builtins, sys, pathlib, importlib
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
c = dict(getattr(builtins, 'V241_AO', {})); DRY = bool(c.get('dry', True)); SP = float(c.get('spine', 0.3))
SRC = '/Game/AAMS/AAMS/Animations/Locomotion/AimOffset/'; DST = '/Game/GraceRanger/SHME/Animations/V241/AO'
bs0 = u.load_asset(SRC + 'BS_Neutral_AO_Stand'); samples = list(bs0.get_editor_property('sample_data'))
names = [s.get_editor_property('animation').get_name() for s in samples]
out = {'dry': DRY, 'samples': names, 'new': [DST + '/SHM241_' + n for n in names] + [DST + '/BS_SHM241_AO_Head']}
LEG = ('root', 'pelvis', 'thigh_', 'calf_', 'foot_', 'ball_', 'ik_', 'leg_')
def is_leg(b): return b == 'root' or b == 'pelvis' or b.startswith(LEG[2:])
def is_spine(b): return b.startswith('spine_')
if not DRY:
    cp = {}
    for n in names:
        p = DST + '/SHM241_' + n
        if not EAL.does_asset_exist(p): assert AT.duplicate_asset('SHM241_' + n, DST, u.load_asset(SRC + n)), n
        cp[n] = u.load_asset(p)
    base = cp['M_Neutral_AO_Stand_X0_Y0']
    tracks = [str(t) for t in AL.get_animation_track_names(base)]
    b0 = ae.read_local(base, tracks, [0])
    stat = {'leg': 0, 'spine': 0}
    for n, a in cp.items():
        a.set_editor_property('ref_pose_seq', base)
        nk = ae.num_frames(a); fr = list(range(nk))
        bl = [b for b in tracks if is_leg(b) or is_spine(b)]
        L = ae.read_local(a, bl, fr)
        for b in bl:
            t0, q0, s0 = b0[b][0]
            if is_leg(b): L[b] = [(t0, q0, s0) for _ in fr]; stat['leg'] += 1
            else:
                nl = []
                for (t, q, s) in L[b]:
                    d = q if (q[0] * q0[0] + q[1] * q0[1] + q[2] * q0[2] + q[3] * q0[3]) >= 0 else (-q[0], -q[1], -q[2], -q[3])
                    qq = ae.qnorm(tuple(q0[i] + (d[i] - q0[i]) * SP for i in range(4)))
                    nl.append((t, qq, s))
                L[b] = nl; stat['spine'] += 1
        ae.write_tracks(a, L, bl, note='SHME V2.41 regional AO', guard=False)
        assert EAL.save_asset(a.get_path_name().split('.')[0], False)
    bp = DST + '/BS_SHM241_AO_Head'
    if not EAL.does_asset_exist(bp): assert AT.duplicate_asset('BS_SHM241_AO_Head', DST, bs0)
    bs = u.load_asset(bp); sd = list(bs.get_editor_property('sample_data'))
    for s in sd: s.set_editor_property('animation', cp[s.get_editor_property('animation').get_name()])
    bs.set_editor_property('sample_data', sd); assert EAL.save_asset(bp, False)
    bs = u.load_asset(bp); out['bs_samples'] = [s.get_editor_property('animation').get_path_name().split('/')[-1] for s in bs.get_editor_property('sample_data')]
    out['stat'] = stat; out['tracks'] = len(tracks)
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('AOC241 ' + json.dumps(out, default=str))
