"""promote231.py (editor job): V2.31 production switch, one knob group at a time. builtins.V231_PROMO = {group: True, ...} (missing = leave),
{'rollback': True} = every V2.31 knob back to its V2.30 value. Groups:
  slow     ABP SHM231_SlowOn 1 (low-speed reversal family PSD_SHM231S_SlowRev* for episodes that start below SHM231_SlowV 90 cm/s)
  exit     ABP SHM231_ExitAuth 1 (sprint exit of an authored reversal clip -> the jog -> sprint push PSD_SHM218_JogPush, not the V2.14 RevPush window)
  fwdrev   DA RedirectLowRevFwdMax 330 (the low-speed reversal class also while moving FORWARD for a jog-mode request: release -> re-press)
  inspect  DA InspectFocusMode 2 (inspection: GR_Inspect tag resolved behind IsValid, focus = the mask mesh bounds, identity = object path)
  steplift DA SwingLiftBaseComp 1 (the capsule step-up no longer lifts the swing foot: lift loses the capsule's rise of the frame)
  tipend   ABP SHM231_TipEndHold 1 (turn-in-place end frame at rest keeps the TIP database one frame instead of the vendor sprint pivot)
  loaded   ABP SHM230_LoadedOn 1 + SHM230_DB_JRFwdL = PSD_SHM231L_LoadRevFwd (catch-step loaded F_B), SHM230_DB_JRBwdL = production B_F
Content edited in place (curved sprint loops, rate 1.0) rolls back from Saved/Codex/SHME_V231_20261026/checkpoint/pre_v231/ (editor closed).
builtins.V231_SAVE saves. Prints PROMO231 {...}."""
import builtins, json, unreal as u
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
P = dict(getattr(builtins, 'V231_PROMO', {})); rb = bool(P.get('rollback'))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
abp = u.load_asset(AP); cp = u.load_asset(CP); sda = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default')
V = '/Game/GraceRanger/SHME/Animations/'
ABPG = {'slow': {'SHM231_SlowOn': (1.0, 0.0)}, 'exit': {'SHM231_ExitAuth': (1.0, 0.0)}, 'tipend': {'SHM231_TipEndHold': (1.0, 0.0)},
        'loaded': {'SHM230_LoadedOn': (1.0, 0.0), 'SHM230_DB_JRFwdL': (V + 'V231/PSD_SHM231L_LoadRevFwd', V + 'V230L/PSD_SHM230L_JogRevFwd'),
                   'SHM230_DB_JRBwdL': (V + 'V226/PSD_SHM226_JogRevBwd', V + 'V230L/PSD_SHM230L_JogRevBwd')}}
DAG = {'fwdrev': {'RedirectLowRevFwdMax': (330.0, 0.0)}, 'inspect': {'InspectFocusMode': (2.0, None)}, 'steplift': {'SwingLiftBaseComp': (1.0, 0.0)}}
out = {'groups': P, 'set': {}}
before_insp = float(sda.get_editor_property('InspectFocusMode'))
out['inspect_focus_mode_before'] = before_insp
for g, kv in ABPG.items():
    if not (P.get(g) or rb): continue
    vals = {}
    for k, (on, off) in kv.items():
        val = off if rb else on
        vals[k] = u.load_asset(val) if isinstance(val, str) else val
    set_defaults(abp, vals); out['set'][g] = {k: str(v)[:80] for k, v in vals.items()}
for g, kv in DAG.items():
    if not (P.get(g) or rb): continue
    for k, (on, off) in kv.items():
        val = (off if off is not None else P.get('inspect_rollback_value', 1.0)) if rb else on
        sda.set_editor_property(k, val); out['set'].setdefault(g, {})[k] = val
st, errs = compile_ok(abp); st2 = compile_ok(cp)[0]
cdo = u.get_default_object(abp.generated_class())
out['abp_after'] = {k: str(cdo.get_editor_property(k))[:70] for k in ('SHM231_SlowOn', 'SHM231_SlowV', 'SHM231_ExitAuth', 'SHM231_TipEndHold', 'SHM230_LoadedOn', 'SHM230_LoadedE', 'SHM230_DB_JRFwdL', 'SHM230_DB_JRBwdL', 'SHM230_IdleGuard', 'SHM230_EarlyRevMin')}
out['shm_after'] = {k: str(sda.get_editor_property(k)) for k in ('RedirectLowRevSpeed', 'RedirectLowRevFwdMax', 'InspectFocusMode', 'SwingLiftBaseComp', 'StepPrepEnabled', 'EffortEnabled')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in str(st2); out['ok'] = ok
if ok and getattr(builtins, 'V231_SAVE', False):
    save(abp, cp); sda.modify(True); u.EditorAssetLibrary.save_loaded_asset(sda, False)
    out['saved'] = True; out['dirty_after'] = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('PROMO231 ' + json.dumps(out, default=str))
