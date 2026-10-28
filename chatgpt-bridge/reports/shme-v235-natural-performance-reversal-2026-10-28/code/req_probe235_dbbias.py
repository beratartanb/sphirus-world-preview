import unreal as u, json
out = {}
for p in ['/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevFwd', '/Game/GraceRanger/SHME/Animations/V232/PSD_SHM232_JogRevBwdX', '/Game/GraceRanger/SHME/Animations/V235/PSD_SHM235_JogRevFwd', '/Game/GraceRanger/SHME/Animations/V231/PSD_SHM231S_SlowRevFwd', '/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogStop']:
    d = u.load_asset(p); r = {}
    for k in ('base_cost_bias', 'continuing_pose_cost_bias', 'looping_cost_bias', 'continuing_interaction_cost_bias'):
        try: r[k] = d.get_editor_property(k)
        except Exception as e: r[k] = 'n/a'
    r['schema'] = d.get_editor_property('schema').get_name()
    out[p.rsplit('/', 1)[1]] = r
print('DBBIAS ' + json.dumps(out, default=str))
