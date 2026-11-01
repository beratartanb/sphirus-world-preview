"""promote244.py (editor job, write manifest = ABP base + child): V2.44 promotion of the lateral family candidate `lat4`:
  ABP SHM242_DB_LatStop := PSD_SHM244_LatStop (was PSD_SHM242_LatStop, V2.43). builtins.V244_PROMOTE_ROLLBACK restores V2.43. builtins.V244_SAVE saves.
Optional idle part (builtins.V244_PROMOTE_IDLE): SHM242_IdleOn 1, SHM242_IdleDB PSD_SHM242_IdleC, DA StanceIdleGateEnabled False (not promoted by default)."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
V42 = '/Game/GraceRanger/SHME/Animations/V242/'; V44 = '/Game/GraceRanger/SHME/Animations/V244/'
RB = bool(getattr(builtins, 'V244_PROMOTE_ROLLBACK', False)); IDLE = bool(getattr(builtins, 'V244_PROMOTE_IDLE', False))
dirty = [p for p in LS.get_dirty_content_packages()]
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'rollback': RB, 'idle_part': IDLE, 'reloaded': [p.get_name().split('/')[-1] for p in dirty]}
bp = u.load_asset(AP)
ldb = u.load_asset(V42 + 'PSD_SHM242_LatStop' if RB else V44 + 'PSD_SHM244_LatStop'); assert ldb, 'lat DB'
set_defaults(bp, {'SHM242_DB_LatStop': ldb})
if IDLE and not RB:
    idb = u.load_asset(V44 + 'PSD_SHM242_IdleC'); assert idb; set_defaults(bp, {'SHM242_IdleOn': 1.0, 'SHM242_IdleDB': idb})
st, errs = compile_ok(bp); cpb = u.load_asset(CPA); st2 = compile_ok(cpb)[0]
out['compile'] = [str(st), errs[:3], str(st2)]; out['ok'] = all('UP_TO_DATE' in str(x) for x in (st, st2)) and not errs
if out['ok'] and getattr(builtins, 'V244_SAVE', False): save(bp, cpb); out['saved'] = True
c1 = u.get_default_object(bp.generated_class()); c2 = u.get_default_object(cpb.generated_class())
out['now'] = {'base_LatStop': str(c1.get_editor_property('SHM242_DB_LatStop')).split('/')[-1][:24], 'child_LatStop': str(c2.get_editor_property('SHM242_DB_LatStop')).split('/')[-1][:24], 'IdleOn': c1.get_editor_property('SHM242_IdleOn')}
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('PROMOTE244 ' + json.dumps(out, default=str))
