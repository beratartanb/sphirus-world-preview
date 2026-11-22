# loadmap.py (control): load the map named in Saved/Codex/Day_20261107/loadmap.txt (no save).
import unreal as u
p=open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/loadmap.txt').read().strip()
print('LOADED',u.get_editor_subsystem(u.LevelEditorSubsystem).load_level(p),u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world().get_path_name())
