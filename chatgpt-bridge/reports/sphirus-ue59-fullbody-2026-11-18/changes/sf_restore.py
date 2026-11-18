# sf_restore.py: return the vegetation show-flag console overrides to their default (2 = no override)
import unreal as u
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
for c in ('ShowFlag.InstancedFoliage 2', 'ShowFlag.InstancedGrass 2', 'ShowFlag.Foliage 2', 'ShowFlag.InstancedStaticMeshes 2'): u.SystemLibrary.execute_console_command(W, c)
print('SFRESTORE', [u.SystemLibrary.get_console_variable_int_value(c.split()[0]) for c in ('ShowFlag.InstancedFoliage', 'ShowFlag.InstancedGrass', 'ShowFlag.Foliage', 'ShowFlag.InstancedStaticMeshes')])
