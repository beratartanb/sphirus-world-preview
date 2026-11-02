"""install248_t2.py (editor job, write manifest = ABP base + child): point the V2.48 turning-start route at the T2 databases (cropped turn
clips, build248_turnstartdb.py v3): SHM248_DB_TurnStart_L/R := PSD_SHM248_JogStartT2_L/R. builtins.V248_SAVE saves. Prints T2_248 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
V = '/Game/GraceRanger/SHME/Animations/V248/'
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); dl = u.load_asset(V + 'PSD_SHM248_JogStartT2_L'); dr = u.load_asset(V + 'PSD_SHM248_JogStartT2_R'); assert dl and dr, 'T2 databases'
set_defaults(bp, {'SHM248_DB_TurnStart_L': dl, 'SHM248_DB_TurnStart_R': dr})
st, errs = compile_ok(bp); cpb = u.load_asset(CPA); st2 = compile_ok(cpb)[0]
out = {'reloaded': [p.get_name().split('/')[-1] for p in dirty], 'compile': [str(st), errs[:3], str(st2)], 'ok': all('UP_TO_DATE' in str(x) for x in (st, st2)) and not errs}
if out['ok'] and getattr(builtins, 'V248_SAVE', False): save(bp, cpb); out['saved'] = True
cdo = u.get_default_object(bp.generated_class()); out['now'] = {k: str(cdo.get_editor_property(k)).split('/')[-1][:40] for k in ('SHM248_DB_TurnStart_L', 'SHM248_DB_TurnStart_R', 'SHM248_On')}
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('T2_248 ' + json.dumps(out, default=str))
