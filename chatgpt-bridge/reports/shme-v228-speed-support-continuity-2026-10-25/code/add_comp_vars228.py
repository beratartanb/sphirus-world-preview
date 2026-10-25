"""add_comp_vars228.py (editor job): two member variables on BP_SHM_HumanMotionComponent for the V2.28 clip-bound capsule speed contract:
  ClipSpeed   (float, SHM|V228) = the designed capsule speed along the character forward axis while an authored reversal clip is in the pose
  ClipSpeedOn (bool,  SHM|V228) = that speed is valid this frame (written by ABP_GR_MotionMatchingBase SHM_Snapshot, read by BP_GR_Player)
No function body changes (vars only; shm_component_vars.py carries the same entries). builtins.V228_SAVE saves. Prints COMPVARS228 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
CP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent'
dirty = [p.get_name() for p in LS.get_dirty_content_packages()]; assert not dirty, ('dirty before', dirty)
bp = u.load_asset(CP)
before = len(B.list_variables(bp))
ensure_vars(bp, [('ClipSpeed', 'float', 'SHM|V228'), ('ClipSpeedOn', 'bool', 'SHM|V228')])
st, errs = compile_ok(bp)
out = {'vars_before': before, 'vars_after': len(B.list_variables(bp)), 'status': str(st), 'errs': errs[:6]}
ok = 'UP_TO_DATE' in str(st) and not errs
out['ok'] = ok
if ok and getattr(builtins, 'V228_SAVE', False): save(bp); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('COMPVARS228 ' + json.dumps(out, default=str))
