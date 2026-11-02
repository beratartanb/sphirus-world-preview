"""promote248.py (editor job, write manifest = ABP base + child): V2.48 promotion of the look-aware turning-start ownership + clip-bound turn: SHM248_On := 1.0
(databases, curves, contracts installed by the V2.48 chain). builtins.V248_PROMOTE_ROLLBACK := 0.0. builtins.V248_SAVE saves. Prints PROMOTE248 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
RB = bool(getattr(builtins, 'V248_PROMOTE_ROLLBACK', False))
dirty = [p for p in LS.get_dirty_content_packages()]
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); set_defaults(bp, {'SHM248_On': 0.0 if RB else 1.0})
st, errs = compile_ok(bp); cpb = u.load_asset(CPA); st2 = compile_ok(cpb)[0]
out = {'rollback': RB, 'reloaded': [p.get_name().split('/')[-1] for p in dirty], 'compile': [str(st), errs[:3], str(st2)], 'ok': all('UP_TO_DATE' in str(x) for x in (st, st2)) and not errs}
if out['ok'] and getattr(builtins, 'V248_SAVE', False): save(bp, cpb); out['saved'] = True
c1 = u.get_default_object(bp.generated_class()); c2 = u.get_default_object(cpb.generated_class())
out['now'] = {'base': c1.get_editor_property('SHM248_On'), 'child': c2.get_editor_property('SHM248_On')}
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('PROMOTE248 ' + json.dumps(out, default=str))
