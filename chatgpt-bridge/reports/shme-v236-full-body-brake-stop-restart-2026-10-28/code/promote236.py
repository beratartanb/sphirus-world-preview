"""promote236.py (editor job, write manifest: ABP base + child) - V2.36 production switch per group (ABP database variables only; content
is new assets). builtins.V236_PROMO = {group: True} or {'rollback': True}. Groups:
  stop    SHM236_DB_JogStop -> V236/PSD_SHM236_JogStop2 (24 release-phase jog stops, brake foot L/R, whole-body brake, ends in the stance the
          straight jog start begins from)                                                   rollback PSD_CP2_JogStop
  start   SHM_JogStartDB_L / _R -> V236 copies of the production start databases + the straight jog starts (left / right first swing)
                                                                                            rollback PSD_SHM_JogStartS_L / _R
  rev     SHM224_DB_JRFwd / JRFwdM / JRBwd / JRBwdM -> V236 whole-body reversal DBs           rollback V235 DBs
  load    SHM230_DB_JRFwdL -> V236/PSD_SHM236L_LoadRevFwd (effort catch-step reversal without the 0.4 s hold)  rollback V231 PSD_SHM231L_LoadRevFwd
  resume  SHM236_DB_JogResume -> V236/PSD_SHM236_JogResume (re-press during a jog stop may continue the jog loop)  rollback PSD_CP2_JogStart
builtins.V236_SAVE saves. Prints PROMO236 {...} incl. the rollback values."""
import builtins, json, unreal as u
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
P_ = dict(getattr(builtins, 'V236_PROMO', {})); rb = bool(P_.get('rollback'))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
abp = u.load_asset(AP); cp = u.load_asset(CP)
V6 = '/Game/GraceRanger/SHME/Animations/V236/'; V5 = '/Game/GraceRanger/SHME/Animations/V235/'; S = '/Game/GraceRanger/SHME/Animations/Starts/'
ABPG = {'stop': {'SHM236_DB_JogStop': (V6 + 'PSD_SHM236_JogStop2', '/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogStop')},
        'start': {'SHM_JogStartDB_L': (V6 + 'PSD_SHM236_JogStartS_L', S + 'PSD_SHM_JogStartS_L'), 'SHM_JogStartDB_R': (V6 + 'PSD_SHM236_JogStartS_R', S + 'PSD_SHM_JogStartS_R')},
        'rev': {'SHM224_DB_JRFwd': (V6 + 'PSD_SHM236_JogRevFwd', V5 + 'PSD_SHM235_JogRevFwd'), 'SHM224_DB_JRFwdM': (V6 + 'PSD_SHM236_JogRevFwd', V5 + 'PSD_SHM235_JogRevFwd'),
                'SHM224_DB_JRBwd': (V6 + 'PSD_SHM236_JogRevBwdX', V5 + 'PSD_SHM235_JogRevBwdX'), 'SHM224_DB_JRBwdM': (V6 + 'PSD_SHM236_JogRevBwdX', V5 + 'PSD_SHM235_JogRevBwdX')},
        'load': {'SHM230_DB_JRFwdL': (V6 + 'PSD_SHM236L_LoadRevFwd', '/Game/GraceRanger/SHME/Animations/V231/PSD_SHM231L_LoadRevFwd')},
        'resume': {'SHM236_DB_JogResume': (V6 + 'PSD_SHM236_JogResume', '/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogStart')}}
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
if ok and getattr(builtins, 'V236_SAVE', False):
    save(abp, cp); out['saved'] = True
    out['dirty_after'] = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('PROMO236 ' + json.dumps(out, default=str))
