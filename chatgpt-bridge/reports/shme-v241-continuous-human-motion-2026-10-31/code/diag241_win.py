"""diag241_win.py (editor job, write manifest = the listed Tk clips) - V2.41 DIAGNOSTIC / window edit: re-make the V2.40 entry BranchIn
window (track SHME_V240_E, same database) of each clip: builtins.V241_WIN = {'clips': {path: [start, end]}}. Prints WIN241 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
c = dict(getattr(builtins, 'V241_WIN', {})); out = {'done': [], 'errors': []}
for p, (a, b) in c.get('clips', {}).items():
    try:
        s = u.load_asset(p); tr = 'SHME_V240_E'; db = None
        for ev in L.get_animation_notify_events(s):
            ns = ev.get_editor_property('notify_state_class')
            if ns and 'BranchIn' in ns.get_class().get_name():
                try:
                    d = ns.get_editor_property('database')
                    if d and 'PSD_SHM240_E' in d.get_name(): db = d
                except Exception: pass
        assert db, 'no V2.40 entry BranchIn on ' + p
        L.remove_animation_notify_track(s, tr); L.add_animation_notify_track(s, tr)
        st = L.add_animation_notify_state_event(s, tr, float(a), float(b) - float(a), u.AnimNotifyState_PoseSearchBranchIn); st.set_editor_property('database', db)
        assert EAL.save_asset(p, False); out['done'].append([p.split('/')[-1], a, b, db.get_name()])
    except Exception as e: out['errors'].append([p.split('/')[-1], str(e)[:160]])
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('WIN241 ' + json.dumps(out))
