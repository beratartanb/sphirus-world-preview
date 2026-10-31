"""probe241_traj.py (measure): trajectory channel samples (offset, weight, flags) of the entry schema and of PSS_Default. Prints TRJ241 {...}."""
import unreal as u, json
out = {}
for p in ('/Game/GraceRanger/SHME/Animations/V241/PSS_SHM241_TkEntry', '/Game/AAMS/AAMS/Animations/Locomotion/MotionMatchingData/Schemas/PSS_Default'):
    s = u.load_asset(p); r = []
    for c in s.get_editor_property('channels'):
        if 'Trajectory' not in c.get_class().get_name(): continue
        props = {}
        for k in dir(c):
            pass
        try:
            for smp in c.get_editor_property('samples'):
                d = {}
                for k in ('offset', 'weight', 'flags', 'debug_color'):
                    try: d[k] = str(smp.get_editor_property(k))[:40]
                    except Exception: pass
                r.append(d)
        except Exception as e: r.append({'err': str(e)[:100]})
        out[p.split('/')[-1]] = {'w': float(c.get_editor_property('weight')), 'samples': r}
    if 'Default' in p: out['default_channels'] = [x.get_class().get_name() for x in s.get_editor_property('channels')]
print('TRJ241 ' + json.dumps(out))
