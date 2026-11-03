"""promote251.py (editor job, write manifest = ABP base + child): V2.51 promotion - SHM251_StartEntry 1 (request-frame start database),
SHM251_YawSlew 1 (continuous yaw hand-over after the turn servo), SHM251_StartLoad 1 (load / relaxed-leg aware start foot); SHM251_ExitOn
stays 0. builtins.V251_PROM = 'promote' | 'rollback'. Prints PROMOTE251 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
mode = getattr(builtins, 'V251_PROM', 'promote'); v = 1.0 if mode == 'promote' else 0.0; out = {'mode': mode}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty: out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); set_defaults(bp, {'SHM251_StartEntry': v, 'SHM251_YawSlew': v, 'SHM251_StartLoad': v, 'SHM251_ExitOn': 0.0})
st_, errs = compile_ok(bp); cpb = u.load_asset(CPA); st2 = compile_ok(cpb)[0]
cdo = u.get_default_object(bp.generated_class()); out['now'] = {k: str(cdo.get_editor_property(k)) for k in ('SHM251_StartEntry', 'SHM251_YawSlew', 'SHM251_StartLoad', 'SHM251_ExitOn', 'SHM249_RM', 'SHM248_HoldT')}
ccdo = u.get_default_object(cpb.generated_class()); out['child'] = {k: str(ccdo.get_editor_property(k)) for k in ('SHM251_StartEntry', 'SHM251_YawSlew', 'SHM251_StartLoad')}
out['ok'] = all('UP_TO_DATE' in str(x) for x in (st_, st2)) and not errs and out['now']['SHM251_StartEntry'] == str(v)
if out['ok']: save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('PROMOTE251 ' + json.dumps(out, default=str))
