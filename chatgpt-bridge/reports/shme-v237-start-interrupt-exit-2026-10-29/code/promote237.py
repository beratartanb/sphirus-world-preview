"""promote237.py (editor job, write manifest: ABP base + child) - V2.37 production switch per group (ABP database variables only; content is
new assets; the FootPlacement DisablePelvisCurveName was installed by install237_fppelvis.py and is a no-op for clips without the curve).
builtins.V237_PROMO = {group: True} or {'rollback': True}. Groups:
  stop    SHM236_DB_JogStop -> V237/PSD_SHM237_JogStop (V2.36 stop family + clip-owned brake pelvis curve)      rollback V236/PSD_SHM236_JogStop2
  start   SHM_JogStartDB_L / _R -> V237 copies of the vendor start DBs + footstep-planned straight starts           rollback V236 start DB copies
  resume  SHM236_DB_JogResume -> V237/PSD_SHM237_JogResume (CP start route: vendor CP2 start + the straight starts + 97 re-push links)
                                                                                                                  rollback PSD_CP2_JogStart
builtins.V237_SAVE saves. Prints PROMO237 {...} incl. the rollback values."""
import builtins, json, unreal as u
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
P_ = dict(getattr(builtins, 'V237_PROMO', {})); rb = bool(P_.get('rollback'))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
abp = u.load_asset(AP); cp = u.load_asset(CP)
V7 = '/Game/GraceRanger/SHME/Animations/V237/'; V6 = '/Game/GraceRanger/SHME/Animations/V236/'
ABPG = {'stop': {'SHM236_DB_JogStop': (V7 + 'PSD_SHM237_JogStop', V6 + 'PSD_SHM236_JogStop2')},
        'start': {'SHM_JogStartDB_L': (V7 + 'PSD_SHM237_JogStartS_L', V6 + 'PSD_SHM236_JogStartS_L'), 'SHM_JogStartDB_R': (V7 + 'PSD_SHM237_JogStartS_R', V6 + 'PSD_SHM236_JogStartS_R')},
        'resume': {'SHM236_DB_JogResume': (V7 + 'PSD_SHM237_JogResume', '/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogStart')}}
out = {'groups': P_, 'set': {}, 'rollback_values': {g: {k: v[1] for k, v in kv.items()} for g, kv in ABPG.items()}}
for g, kv in ABPG.items():
    if not (P_.get(g) or rb): continue
    vals = {k: u.load_asset(off if rb else on) for k, (on, off) in kv.items()}
    assert all(vals.values()), (g, vals)
    set_defaults(abp, vals); out['set'][g] = {k: v.get_name() for k, v in vals.items()}
st, errs = compile_ok(abp); st2 = compile_ok(cp)[0]
cdo = u.get_default_object(abp.generated_class())
out['abp_after'] = {k: str(cdo.get_editor_property(k).get_name()) for kv in ABPG.values() for k in kv}
ok = all('UP_TO_DATE' in str(s) for s in (st, st2)) and not errs; out['ok'] = ok
if ok and getattr(builtins, 'V237_SAVE', False):
    save(abp, cp); out['saved'] = True
    out['dirty_after'] = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('PROMO237 ' + json.dumps(out, default=str))
