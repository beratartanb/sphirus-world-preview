"""save241.py (editor job, write manifest = the listed BPs) - save already-compiled in-memory patches after checking every listed BP is
UP_TO_DATE (with or without warnings) and that no other package is dirty. builtins.V241_SAVEP = [paths]. Prints SAVE241 {...}."""
import unreal as u, json, builtins
EAL = u.EditorAssetLibrary; LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
P = list(builtins.V241_SAVEP); out = {}
dirty = [q.get_name() for q in LS.get_dirty_content_packages()]; out['dirty_before'] = dirty
assert all(d in P for d in dirty), ('unexpected dirty', dirty)
for p in P:
    a = u.load_asset(p); u.BlueprintEditorLibrary.compile_blueprint(a); st = str(a.get_editor_property('status')); out[p.split('/')[-1]] = st
    assert 'UP_TO_DATE' in st, (p, st)
for p in P:
    if p in dirty: assert EAL.save_loaded_asset(u.load_asset(p), False), p
out['dirty_after'] = [q.get_name() for q in LS.get_dirty_content_packages()]; out['ok'] = not out['dirty_after']
print('SAVE241 ' + json.dumps(out))
