import unreal as u, json
out = {}
for s in ('L', 'R'):
    db = u.load_asset('/Game/GraceRanger/SHME/Animations/V248/PSD_SHM248_JogStartT_' + s)
    out[s] = {'n': db.get_num_animation_assets(), 'entries': [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())], 'schema': str(db.get_editor_property('schema')).split('/')[-1][:50]} if db else None
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('TDBPROBE248 ' + json.dumps(out))
