"""probe241_sch2.py (measure job): bone names / sample offsets of the takeover schema and of the V2.38 cut schema. Prints SCHP2 {...}."""
import unreal as u, json
def ch(c):
    r = {'cls': c.get_class().get_name().replace('PoseSearchFeatureChannel_', '')}
    for k in ('weight', 'sample_time_offset', 'component_stripping', 'use_feature_time_offset'):
        try: r[k] = round(float(c.get_editor_property(k)), 3)
        except Exception: pass
    try: r['bone'] = str(c.get_editor_property('bone').get_editor_property('bone_name'))
    except Exception: pass
    try:
        r['samples'] = [[str(s.get_editor_property('bone').get_editor_property('bone_name')) if s.get_editor_property('bone') else '', round(float(s.get_editor_property('offset')), 2), str(s.get_editor_property('flags'))[:30]] for s in c.get_editor_property('samples')]
    except Exception as e: pass
    try: r['sub'] = [ch(x) for x in c.get_editor_property('sub_channels')]
    except Exception: pass
    return r
out = {}
for p in ('/Game/GraceRanger/SHME/Animations/V239/PSS_SHM239_Takeover',):
    s = u.load_asset(p); out[p.split('/')[-1]] = [ch(c) for c in s.get_editor_property('channels')]
d = u.load_asset('/Game/GraceRanger/SHME/Animations/V238/PSD_SHM238_JogCut'); out['cut_schema'] = str(d.get_editor_property('schema').get_path_name())
print('SCHP2 ' + json.dumps(out))
