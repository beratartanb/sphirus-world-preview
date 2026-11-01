"""pre244_walk.py (A/B PRE, in memory only - never saved): apply gen244_walk.py to the loaded vendor A_LB_Walk_Fwd (yaw_scale from
builtins.V244_WALK_SCALE, default 0.65). POST = post244_walk.py reloads the package from disk. Prints PREWALK244 ..."""
import unreal as u, builtins, json
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
builtins.G244W = {'inplace': True, 'yaw_scale': float(getattr(builtins, 'V244_WALK_SCALE', 0.65)), 'chest_scale': float(getattr(builtins, 'V244_CHEST_SCALE', 0.55)), 'arm_scale': float(getattr(builtins, 'V244_ARM_SCALE', 1.0)), 'lean_deg': float(getattr(builtins, 'V244_LEAN', 0.0))}
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V244_20261101/gen244_walk.py', encoding='utf-8').read(), 'gen244_walk.py', 'exec'), {'__name__': '__job__'})
print('PREWALK244 applied yaw_scale %s' % builtins.G244W['yaw_scale'])
