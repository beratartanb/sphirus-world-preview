"""load_production.py (measure job): bring the production map back (after a reference map was loaded). Refuses when anything is dirty."""
import unreal as u, time
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
S = u.EditorLoadingAndSavingUtils
dirty = sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
assert not dirty, 'dirty packages: %s' % dirty[:8]
t0 = time.monotonic(); ok = u.get_editor_subsystem(u.LevelEditorSubsystem).load_level('/Game/GraceRanger/Maps/L_GR_SphirusHouse')
w = E.get_editor_world()
print('LOAD_PRODUCTION', bool(ok), w.get_path_name(), round(time.monotonic() - t0, 1), 's; levels', [str(l.get_outer().get_name()) for l in u.EditorLevelUtils.get_levels(w)])
