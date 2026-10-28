"""probe236_stop.py (measure): V2.36 jog stop route + source facts. (1) Update_MotionMatching: every node with an input pin whose default
names PSD_CP2_JogStop (node id, pin, exec sources) and every node writing CurrentSelectedDatabase; (2) PSD_CP2_JogStop: assets (mirror,
sampling range), schema, biases; (3) the jog loop A_CT_Jog_Fwd and the stop clip: length, root speed, curves, notify tracks.
Prints PROBE236 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info, src
import json
AL = u.AnimationLibrary
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); out = {'route': [], 'csd_writers': []}
gp = graph(bp, 'Update_MotionMatching')
for n in B.find_nodes(gp):
    p = pn(n); ni = info(p)
    for q in ni.input_pins:
        dv = str(getattr(q, 'default_value', '') or '') + str(getattr(q, 'default_object', '') or '')
        if 'JogStop' in dv or 'RunStop' in dv or 'RR_Stop' in dv:
            ex = [s[0].rsplit('.', 1)[-1] for s in src((p, 'execute'))] if any(x.name == 'execute' for x in ni.input_pins) else []
            out['route'].append({'node': p.rsplit('.', 1)[-1], 'type': str(ni.type_id)[-80:], 'pin': q.name, 'val': dv[-90:], 'exec_from': ex,
                                 'pins': [x.name for x in ni.input_pins]})
    if 'CurrentSelectedDatabase' in str(ni.type_id) and 'Set' in str(ni.type_id):
        out['csd_writers'].append(p.rsplit('.', 1)[-1])
db = u.load_asset('/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogStop')
dd = {'n': db.get_num_animation_assets(), 'assets': []}
for k in ('schema', 'base_cost_bias', 'continuing_pose_cost_bias', 'looping_cost_bias', 'normalization_set'):
    try: dd[k] = str(db.get_editor_property(k))[-90:]
    except Exception as e: dd[k] = 'ERR ' + str(e)[:60]
for i in range(db.get_num_animation_assets()):
    a = db.get_animation_asset(i); dd['assets'].append(a.get_path_name() if a else None)
try:
    ents = db.get_editor_property('animation_assets'); dd['entries'] = [str(e)[:300] for e in ents]
except Exception as e: dd['entries_err'] = str(e)[:120]
out['db'] = dd
for c in ('/Game/GraceRanger/Animations/Continuity/A_CT_Jog_Fwd', '/Game/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop',
          '/Game/GraceRanger/Animations/Continuity/A_CT_Jog_Bwd'):
    s = u.load_asset(c)
    if not s: out[c] = None; continue
    ln = float(s.get_play_length()); N = AL.get_num_frames(s)
    rt = [AL.get_bone_pose_for_time(s, 'root', min(ln, k * ln / 20.0), False).translation for k in range(21)]
    out[c.rsplit('/', 1)[-1]] = {'len': round(ln, 4), 'frames': N, 'root_y': [round(v.y, 1) for v in rt], 'root_x': [round(v.x, 1) for v in rt[::5]],
        'curves': [str(x) for x in AL.get_animation_curve_names(s, u.RawCurveTrackTypes.RCT_FLOAT)],
        'tracks': [str(x) for x in AL.get_animation_notify_track_names(s)], 'rate': s.get_editor_property('rate_scale'),
        'root_motion': s.get_editor_property('enable_root_motion')}
print('PROBE236 ' + json.dumps(out, default=str))
