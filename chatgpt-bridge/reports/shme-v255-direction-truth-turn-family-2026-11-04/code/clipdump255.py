"""clipdump255.py (editor job, SHME_KIND=measure, read only): V2.55 stick / measurement JSON of source clips (component space incl. the root bone)
into Saved/Codex/SHME_V255_20261104/src/<name>.json in the stick238 format. builtins.CD255 = {'clips': [paths]} or the default list below.
LOCAL evidence only (per-frame bone data of paid clips is never published)."""
import unreal as u, json, pathlib, sys, builtins, importlib
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
OUT = P / 'Saved/Codex/SHME_V255_20261104/src'; OUT.mkdir(parents=True, exist_ok=True)
SP = '/Game/AAMS/AAMS/Animations/Locomotion/Sprint/M_Neutral_Sprint_'; RN = '/Game/AAMS/AAMS/Animations/Locomotion/Run/M_Neutral_Run_'; WK = '/Game/AAMS/AAMS/Animations/Locomotion/Walk/M_Neutral_Walk_'
CM = '/Game/CoreMotion_Retargeted/AAMS/Walk/'
D = [SP + 'Turn_%s_%s_%sfoot' % (s, a, f) for s in 'RL' for a in ('090', '180') for f in 'RL'] + [SP + 'Loop_F']
D += [RN + 'Turn_%s_%s_%sfoot' % (s, a, f) for s in 'RL' for a in ('090', '135', '180') for f in 'RL'] + [RN + 'Pivot_F_B_Lfoot', RN + 'Pivot_F_B_Rfoot']
D += [CM + 'af_Loco_Jog_Fwd_Pivot', CM + 'af_Loco_Jog_Left_Pivot', CM + 'af_Loco_Jog_Right_Pivot', CM + 'af_Loco_Walk_Fwd_Pivot', CM + 'af_Loco_Walk_Left_Pivot', CM + 'af_Loco_Walk_Right_Pivot', CM + 'af_Loco_Run_Fwd', CM + 'af_Loco_Run_Fwd_Stop']
D += ['/Game/GraceRanger/SHME/Animations/V233/SprintCalm/SHM233_Calm_A_LB_Sprint_Fwd', '/Game/GraceRanger/Animations/LocomotionBehavior/A_LB_Sprint_Fwd']
clips = list(getattr(builtins, 'CD255', {}).get('clips', D))
SB = ['root', 'pelvis', 'spine_03', 'spine_05', 'neck_01', 'head', 'clavicle_l', 'upperarm_l', 'lowerarm_l', 'hand_l', 'clavicle_r', 'upperarm_r', 'lowerarm_r', 'hand_r', 'thigh_l', 'calf_l', 'foot_l', 'ball_l', 'thigh_r', 'calf_r', 'foot_r', 'ball_r']
done = []
for p in clips:
    try:
        s = u.load_asset(p)
        if not s: done.append([p, 'missing']); continue
        c = ae.Clip(s, SB); n = c.nf; L = float(s.get_play_length()); dt = L / max(1, n - 1)
        fr = []; ro = []; ry = []
        for f in range(n):
            row = [[round(x, 2) for x in c.comp(b, f)[0]] for b in SB]; fr.append(row); ro.append(row[0])
            q = c.comp('root', f)[1]; ry.append([round(x, 4) for x in ae.qrot(q, (0.0, 1.0, 0.0))])
        sk = s.get_editor_property('skeleton'); nm = p.rsplit('/', 1)[-1]
        (OUT / (nm + '.json')).write_text(json.dumps({'name': nm, 'path': p, 'dt': dt, 'len': L, 'bones': SB, 'fwd': [0.0, 1.0, 0.0], 'right': [-1.0, 0.0, 0.0], 'root': ro, 'rootfwd': ry, 'frames': fr, 'skeleton': sk.get_path_name() if sk else ''}))
        done.append([nm, n, round(L, 2), sk.get_name() if sk else ''])
    except Exception as e: done.append([p, 'ERR ' + str(e)[:120]])
print('CD255 ' + json.dumps(done))
