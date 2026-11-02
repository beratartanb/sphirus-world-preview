"""promote249.py (editor job, write manifest = ABP base + child [+ DA_SHM_Response_Default when idle]): V2.49 promotion.
  turn  : ABP SHM249_RM := 1.0, SHM248_HoldT := 0 (cropped turning start owned by the capsule position servo; request-frame T2 search; hold while the crop
          plays). The foot ground-contact repair is already in the turn clips (no switch).
  idle  : ABP SHM242_IdleOn := 1, SHM242_IdleDB := /Game/GraceRanger/SHME/Animations/V244/PSD_SHM242_IdleC (V2.44 weighted idle) and
          DA_SHM_Response_Default.StanceIdleGateEnabled := False (the V1.2 stance-hold snapshot no longer freezes the lower body)
builtins.V249_PROM = {'turn': bool, 'idle': bool, 'rollback': bool}. builtins.V249_SAVE saves. Prints PROMOTE249 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
DA = '/Game/GraceRanger/SHME/DA_SHM_Response_Default'; IDB = '/Game/GraceRanger/SHME/Animations/V244/PSD_SHM242_IdleC'
P = dict(getattr(builtins, 'V249_PROM', {})); RB = bool(P.get('rollback'))
dirty = [p for p in LS.get_dirty_content_packages()]
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); vals = {}; out = {'P': P, 'reloaded': [p.get_name().split('/')[-1] for p in dirty]}
if P.get('turn'): vals.update({'SHM249_RM': 0.0 if RB else 1.0, 'SHM248_HoldT': 1.0 if RB else 0.0})   # the crop hold replaces the V2.48 1.0 s timer hold (it re-searched the T2 DB at the crop end)
if P.get('idle'): vals.update({'SHM242_IdleOn': 0.0 if RB else 1.0, 'SHM242_IdleDB': None if RB else u.load_asset(IDB)})
if vals: set_defaults(bp, vals)
st, errs = compile_ok(bp); cpb = u.load_asset(CPA); st2 = compile_ok(cpb)[0]
out['compile'] = [str(st), errs[:3], str(st2)]; ok = all('UP_TO_DATE' in str(x) for x in (st, st2)) and not errs
da = None
if P.get('idle'):
    da = u.load_asset(DA); da.set_editor_property('StanceIdleGateEnabled', bool(RB)); out['da_gate'] = da.get_editor_property('StanceIdleGateEnabled')
out['ok'] = ok
if ok and getattr(builtins, 'V249_SAVE', False):
    save(bp, cpb)
    if da is not None: assert u.EditorAssetLibrary.save_asset(DA, False)
    out['saved'] = True
c1 = u.get_default_object(bp.generated_class()); c2 = u.get_default_object(cpb.generated_class())
out['now'] = {k: str(c.get_editor_property(k)).split('/')[-1][:40] for k in ('SHM249_RM', 'SHM248_HoldT', 'SHM242_IdleOn', 'SHM242_IdleDB') for c in (c1,)}
out['child_rm'] = c2.get_editor_property('SHM249_RM')
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('PROMOTE249 ' + json.dumps(out, default=str))
