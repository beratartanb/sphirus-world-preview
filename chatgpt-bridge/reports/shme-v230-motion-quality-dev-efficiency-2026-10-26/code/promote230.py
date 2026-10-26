"""promote230.py (editor job): V2.30 production switch. builtins.V230_PROMO = {'lowrev': True} (missing = leave) / {'rollback': True}.
  lowrev : DA_SHM RedirectLowRevSpeed 30 (backpedal reversal class at low speed, requested gait jog / sprint) + ABP SHM230_EarlyRevMin 30
           (frame-0 authored reversal entry down to 30 cm/s for the same gait gate).
  idleguard: ABP SHM230_IdleGuard 1 (idle entry may not end a held authored reversal inside its brake / release-resume window).
  rollback: all 0. Content re-authoring (in place) rolls back from Saved/Codex/SHME_V230_20261026/checkpoint/pre_reauthor/ with the editor
  closed; candidates that stay OFF: SHM230_FamGate, SHM230_LoadedOn (loaded family), StepPrepEnabled.
builtins.V230_SAVE saves. Prints PROMO230 {...}."""
import builtins, json, unreal as u
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
P = dict(getattr(builtins, 'V230_PROMO', {})); rb = bool(P.get('rollback'))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
abp = u.load_asset(AP); cp = u.load_asset(CP); sda = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default')
v = 0.0 if rb else (30.0 if P.get('lowrev') else None)
out = {'groups': P}
if v is not None:
    sda.set_editor_property('RedirectLowRevSpeed', v); set_defaults(abp, {'SHM230_EarlyRevMin': v})
ig = 0.0 if rb else (1.0 if P.get('idleguard') else None)
if ig is not None: set_defaults(abp, {'SHM230_IdleGuard': ig})
st, errs = compile_ok(abp); st2 = compile_ok(cp)[0]
cdo = u.get_default_object(abp.generated_class())
out['abp_after'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM230_EarlyRevMin', 'SHM230_EarlyRevPeak', 'SHM230_FamGate', 'SHM230_LoadedOn', 'SHM230_IdleGuard', 'SHM229_PushCancel', 'SHM229_ResumeWin')}
out['shm_after'] = {k: str(sda.get_editor_property(k)) for k in ('RedirectLowRevSpeed', 'RedirectLowRevPeak', 'StepPrepEnabled', 'EffortEnabled', 'EffortScaleMin')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in str(st2); out['ok'] = ok
if ok and getattr(builtins, 'V230_SAVE', False):
    save(abp, cp); sda.modify(True); u.EditorAssetLibrary.save_loaded_asset(sda, False)
    out['saved'] = True; out['dirty_after'] = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('PROMO230 ' + json.dumps(out, default=str))
