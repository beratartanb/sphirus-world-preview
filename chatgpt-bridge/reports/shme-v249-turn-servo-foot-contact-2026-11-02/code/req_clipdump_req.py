"""clipdump_req.py (measure): V2.49 frame-by-frame ground truth for the turning starts.
Per cropped turn clip (V248/SHM248_Jog_Start_Turn*_crop) and its full project copy: every key frame's root (x, y, yaw) and ball_l / ball_r /
foot_l / foot_r in CLIP space (root included), plus the root-motion settings (enable_root_motion, root lock) and the curves' sample values.
Also reports whether AnimInstance exposes SetRootMotionMode to scripts and the ABP CDO root motion mode. Writes data/clipdump.json."""
import unreal as u, json, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary
V = '/Game/GraceRanger/SHME/Animations/V248/'; J = '/Game/GraceRanger/SHME/Animations/Starts/Jog/'
out = {'clips': {}}
paths = [V + 'SHM248_Jog_Start_Turn%s%s_crop' % (s, d) for s in ('L', 'R') for d in ('090', '135', '180')]
paths += [J + 'SHM_JogQ_af_Loco_Jog_Start_Turn%s%s_%sfoot_AAMS' % (s, d, s) for s, d in (('L', '135'), ('L', '180'))]
for p in paths:
    seq = u.load_asset(p); c = ae.Clip(seq, ['root', 'ball_l', 'ball_r', 'foot_l', 'foot_r', 'pelvis'])
    rows = []
    for f in range(c.nf):
        rt, rq = c.comp('root', f); ry = u.Quat(rq[0], rq[1], rq[2], rq[3]).rotator().yaw
        r = [round(rt[0], 2), round(rt[1], 2), round(ry, 2)]
        for b in ('ball_l', 'ball_r', 'foot_l', 'foot_r', 'pelvis'):
            t_ = c.comp(b, f)[0]; r += [round(t_[0], 2), round(t_[1], 2), round(t_[2], 2)]
        rows.append(r)
    d = {'nf': c.nf, 'len': float(seq.get_play_length()), 'rows': rows, 'cols': 'root_x root_y root_yaw ball_l xyz ball_r xyz foot_l xyz foot_r xyz pelvis xyz'}
    for k in ('enable_root_motion', 'root_motion_root_lock', 'force_root_lock', 'use_normalized_root_motion_scale'):
        try: d[k] = str(seq.get_editor_property(k))
        except Exception as e: d[k] = 'n/a'
    out['clips'][p.split('/')[-1]] = d
out['anim_instance_set_root_motion_mode'] = hasattr(u.AnimInstance, 'set_root_motion_mode')
out['anim_instance_methods_root'] = [m for m in dir(u.AnimInstance) if 'root' in m.lower()][:20]
bp = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase')
cdo = u.get_default_object(bp.generated_class())
for k in ('root_motion_mode',):
    try: out['abp_' + k] = str(cdo.get_editor_property(k))
    except Exception as e: out['abp_' + k] = 'err ' + str(e)[:80]
json.dump(out, open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V249_20261102/data/clipdump.json', 'w'))
print('CLIPDUMP249 ' + json.dumps({k: v for k, v in out.items() if k != 'clips'}) + ' ' + json.dumps({k: {kk: vv for kk, vv in v.items() if kk not in ('rows',)} for k, v in out['clips'].items()}))
