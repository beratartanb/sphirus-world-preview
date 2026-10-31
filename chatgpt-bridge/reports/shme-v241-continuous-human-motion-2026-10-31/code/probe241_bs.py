"""probe241_bs.py (measure): the vendor AO blend space samples (anim, value), each anim's additive settings and the per-bone magnitude
of its additive delta vs its base (pelvis / spine / neck / head / thigh). Prints BS241 {...}."""
import unreal as u, json, math
AL = u.AnimationLibrary
bs = u.load_asset('/Game/AAMS/AAMS/Animations/Locomotion/AimOffset/BS_Neutral_AO_Stand')
out = {'class': bs.get_class().get_name(), 'samples': []}
try: samples = bs.get_editor_property('sample_data')
except Exception as e: samples = []; out['err'] = str(e)[:100]
for s in samples:
    a = s.get_editor_property('animation'); v = s.get_editor_property('sample_value')
    r = {'anim': a.get_path_name() if a else None, 'v': [round(v.x), round(v.y)]}
    if a:
        for k in ('additive_anim_type', 'ref_pose_type', 'ref_pose_seq', 'ref_frame_index'):
            try: r[k] = str(a.get_editor_property(k))[:90]
            except Exception: pass
        try:
            r['len'] = round(float(a.get_play_length()), 2); r['frames'] = int(AL.get_num_frames(a))
        except Exception: pass
    out['samples'].append(r)
print('BS241 ' + json.dumps(out))
