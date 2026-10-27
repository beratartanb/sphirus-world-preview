"""startdb_probe232.py (editor job, read-only): which PoseSearch databases list the owned JogQ start clips (BranchIn notify states on
each clip -> their 'database'), and what each such database holds. Prints SDB232 {...}."""
import unreal as u, json
AL = u.AnimationLibrary; AR = u.AssetRegistryHelpers.get_asset_registry()
clips = [str(a.package_name) for a in AR.get_assets_by_path('/Game/GraceRanger/SHME/Animations/Starts', recursive=True) if str(a.asset_class_path.asset_name) == 'AnimSequence']
out = {'clips': {}, 'dbs': {}}
for p in clips:
    s = u.load_asset(p); dbs = []
    for ev in AL.get_animation_notify_events(s):
        st = ev.get_editor_property('notify_state_class')
        if st and 'BranchIn' in st.get_class().get_name():
            db = st.get_editor_property('database'); dbs.append((db.get_path_name().split('.')[0] if db else None, round(ev.get_editor_property('trigger_time_offset') if False else 0, 2)))
    out['clips'][p.rsplit('/', 1)[-1]] = sorted(set(d for d, _ in dbs if d))
for d in sorted(set(x for v in out['clips'].values() for x in v)):
    db = u.load_asset(d); n = db.get_num_animation_assets()
    out['dbs'][d.rsplit('/', 1)[-1]] = [db.get_animation_asset(i).get_name() for i in range(n)]
print('SDB232 ' + json.dumps(out, default=str))
