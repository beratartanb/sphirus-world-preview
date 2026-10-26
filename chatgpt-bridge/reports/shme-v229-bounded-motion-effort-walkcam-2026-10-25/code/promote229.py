"""promote229.py (editor job): V2.29 production switch. builtins.V229_PROMO = dict of groups (missing = leave as is):
  camera : DA_SHM CamSwapMinSpeed 230, CamFolDZLatWalk 3, CamFolDZFwdWalk 4 (walk framing; jog / sprint follow unchanged)
  effort : DA_SHM EffortEnabled true (+ V229_EFFORT dict of tuned values, optional)
  resume : ABP SHM229_ResumeWin 0.2 (release -> re-press continues the reversal clip)
  pushcancel : ABP SHM229_PushCancel 1 (a request for the old travel during the reversal PUSH phase re-routes to the opposite family)
  rollback: {rollback: True} = camera 60 / 12 / 10, EffortEnabled false, ResumeWin 0. (The RevTurn content fix is a bug fix: its rollback is the
            file checkpoint Saved/Codex/SHME_V229_20261025/checkpoint/revturn/ with the editor closed.)
builtins.V229_SAVE saves. Prints PROMO229 {...}."""
import builtins, json, unreal as u
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
P = dict(getattr(builtins, 'V229_PROMO', {})); rb = bool(P.get('rollback')); EF = dict(getattr(builtins, 'V229_EFFORT', {}))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
abp = u.load_asset(AP); cp = u.load_asset(CP); sda = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default')
out = {'groups': P}
SD = {}
if rb: SD.update({'CamSwapMinSpeed': 60.0, 'CamFolDZLatWalk': 12.0, 'CamFolDZFwdWalk': 10.0, 'EffortEnabled': False})
if P.get('camera'): SD.update({'CamSwapMinSpeed': 230.0, 'CamFolDZLatWalk': 3.0, 'CamFolDZFwdWalk': 4.0})
if P.get('effort'): SD['EffortEnabled'] = True; SD.update(EF)
for k, v in SD.items(): sda.set_editor_property(k, v)
KN = {}
if rb: KN['SHM229_ResumeWin'] = 0.0; KN['SHM229_PushCancel'] = 0.0
if P.get('pushcancel'): KN['SHM229_PushCancel'] = 1.0
if P.get('resume'): KN['SHM229_ResumeWin'] = 0.2
if KN: set_defaults(abp, KN)
st, errs = compile_ok(abp); st2 = compile_ok(cp)[0]
cdo = u.get_default_object(abp.generated_class())
out['abp_after'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM229_ResumeWin', 'SHM229_PushCancel', 'SHM227_RevHold', 'SHM228_ClipSpeed', 'SHM228_RelHold', 'SHM228_CancelOn')}
out['shm_after'] = {k: str(sda.get_editor_property(k)) for k in ('CamSwapMinSpeed', 'CamFolDZLatWalk', 'CamFolDZFwdWalk', 'EffortEnabled', 'EffortGain', 'EffortTurnK', 'EffortAccK', 'EffortLoadK', 'EffortTauRec', 'EffortUseTau', 'EffortReqTau', 'EffortScaleMin')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in str(st2); out['ok'] = ok; out['status'] = [str(st), str(st2)]
if ok and getattr(builtins, 'V229_SAVE', False):
    if KN: save(abp, cp)
    sda.modify(True); u.EditorAssetLibrary.save_loaded_asset(sda, False)
    out['saved'] = True; out['dirty_after'] = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('PROMO229 ' + json.dumps(out, default=str))
