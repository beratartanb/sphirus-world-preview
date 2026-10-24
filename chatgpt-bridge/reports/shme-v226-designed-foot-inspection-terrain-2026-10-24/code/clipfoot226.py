"""clipfoot226.py (editor job, read-only): per-clip root-motion flags and the ROOT-RELATIVE component-space positions of pelvis /
foot / ball bones sampled at 120 Hz, for the reversal chain diagnosis (which stage first breaks the authored foot path).
Output: Saved/Codex/SHME_V226_20261024/clipfoot226.json  { clip: {flags, T, NK, dt, rows:[[t, root(3), pelvis(3), foot_l(3), foot_r(3), ball_l(3), ball_r(3)], ...]} }
Root-relative = bone component position with the root translation removed (what the pose contains when root motion is extracted), so
visible_foot_world = capsule_pos + R_mesh * (root_relative + mesh_offset) if nothing else touches the foot."""
import unreal as u, json, math, sys, pathlib, importlib
P = pathlib.Path(u.Paths.project_dir()); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary
CLIPS = ['/Game/GraceRanger/SHME/Animations/V225/SHM225_JogRev_B_F_P6', '/Game/GraceRanger/SHME/Animations/V225/SHM225_JogRev_F_B_P1',
         '/Game/GraceRanger/SHME/Animations/V225/SHM225_JogRev_B_F_P5', '/Game/GraceRanger/SHME/Animations/V225/SHM225_JogRev_F_B_P4',
         '/Game/GraceRanger/SHME/Animations/V225/SHM225_JogRev_F_B_P5']
# the loops that precede / follow and the production pivots on the same route
import builtins
for extra in getattr(builtins, 'CF_EXTRA', []): CLIPS.append(extra)
reg = u.AssetRegistryHelpers.get_asset_registry()
def find(name):
    r = reg.get_assets_by_package_name(name) if name.startswith('/Game/') else None
    if r: return name
    for a in reg.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine', 'AnimSequence'), True):
        if str(a.asset_name) == name: return str(a.package_name)
    return None
for n in ('A_RB_Jog_Rear', 'A_CT_Jog_Fwd', 'A_RB_Jog_RearLeft', 'A_RB_Jog_RearRight', 'A_CT_Jog_Bwd', 'SHM_DPP_Jog_Bwd_Pivot', 'A_CP2_Jog_Fwd_Pivot', 'SHM224_Jog_Fwd_Pivot_M', 'SHM224_Jog_Bwd_Pivot_M'):
    p = find(n)
    if p and p not in CLIPS: CLIPS.append(p)
def lerp(a, b, t): return tuple(a[i] + (b[i] - a[i]) * t for i in range(len(a)))
def slerp(a, b, t):
    d = sum(a[i] * b[i] for i in range(4))
    if d < 0: b = tuple(-x for x in b); d = -d
    if d > 0.9995: return ae.qnorm(tuple(a[i] + (b[i] - a[i]) * t for i in range(4)))
    th = math.acos(min(d, 1.0)); s = math.sin(th)
    return tuple((math.sin((1 - t) * th) * a[i] + math.sin(t * th) * b[i]) / s for i in range(4))
out = {}
for path in CLIPS:
    seq = u.load_asset(path)
    if not seq: out[path] = {'err': 'missing'}; continue
    names = sorted(str(n) for n in AL.get_animation_track_names(seq))
    need = [b for b in ('root', 'pelvis', 'foot_l', 'foot_r', 'ball_l', 'ball_r', 'ik_foot_l', 'ik_foot_r', 'ik_foot_root') if b in names]
    NK = ae.num_frames(seq) - 1; T = float(seq.get_play_length())
    Lk = ae.read_local(seq, names, list(range(NK + 1)))
    clip = ae.Clip(seq, ['root', 'pelvis', 'foot_l', 'foot_r', 'ball_l', 'ball_r', 'calf_l', 'calf_r', 'thigh_l', 'thigh_r', 'spine_01'] + [b for b in ('ik_foot_l', 'ik_foot_r', 'ik_foot_root') if b in names])
    flags = {}
    for prop in ('enable_root_motion', 'force_root_lock', 'root_motion_root_lock', 'rate_scale'):
        try: flags[prop] = str(seq.get_editor_property(prop))
        except Exception as e: flags[prop] = 'n/a'
    try: flags['curves'] = [str(c.get_editor_property('name')) for c in seq.get_editor_property('raw_curve_data').get_editor_property('float_curves')][:12]
    except Exception: flags['curves'] = 'n/a'
    try: flags['notifies'] = sorted(set(str(n.get_editor_property('notify_name')) for n in seq.get_editor_property('notifies')))[:12]
    except Exception: flags['notifies'] = 'n/a'
    rows = []; dt = 1.0 / 120.0; k = 0
    while k * dt <= T + 1e-6:
        tau = min(k * dt, T); f = tau / T * NK; i = int(math.floor(f)); w = f - i; i = min(i, NK - 1)
        loc = {}
        for b in names:
            (t0, q0, s0), (t1, q1, s1) = Lk[b][i], Lk[b][i + 1]
            loc[b] = (lerp(t0, t1, w), slerp(q0, q1, w), lerp(s0, s1, w))
        rootT = loc['root'][0]
        tmp = {b: [loc[b]] for b in loc}; tmp['root'] = [((0.0, 0.0, 0.0), loc['root'][1], loc['root'][2])]
        row = [round(tau, 4), [round(x, 2) for x in rootT]]
        for b in ('pelvis', 'foot_l', 'foot_r', 'ball_l', 'ball_r'):
            c = clip.comp(b, 0, tmp)[0]; row.append([round(x, 2) for x in c])
        rows.append(row); k += 1
    out[path.rsplit('/', 1)[-1]] = {'path': path, 'flags': flags, 'T': round(T, 4), 'NK': NK, 'dt': dt, 'cols': ['t', 'root', 'pelvis', 'foot_l', 'foot_r', 'ball_l', 'ball_r'], 'rows': rows}
(P / 'Saved/Codex/SHME_V226_20261024/clipfoot226.json').write_text(json.dumps(out))
print('CLIPFOOT226 ' + json.dumps({k: (v.get('flags'), v.get('T'), len(v.get('rows', []))) for k, v in out.items()}, default=str))
