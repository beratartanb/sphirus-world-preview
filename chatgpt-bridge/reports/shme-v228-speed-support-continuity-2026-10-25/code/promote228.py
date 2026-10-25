"""promote228.py (editor job): V2.28 production switch. builtins.V228_PROMO = dict of groups to switch on (missing = leave as is):
  motion  : promote226 Reversal226 (32-bin reversal DBs) + ABP SHM227_RevHold 1, SHM228_ClipSpeed 1 + DA_GR GR228_ClipSpeed 1
  cancel  : ABP SHM228_RelHold 1, SHM228_CancelOn 1
  terrain : DA_SHM SwingLiftMax 36 (+ stepedge: StepEdgeOn true)
  inspect : DA_SHM InspectIdOn 1, InspectFocusMode 1
  rollback: {rollback: True} restores Reversal226 False / Reversal False, ABP knobs 0, GR228 0, SwingLiftMax 25, StepEdgeOn False, InspectIdOn / FocusMode 0.
builtins.V228_SAVE saves. Prints PROMO228 {...}."""
import builtins, json
P = dict(getattr(builtins, 'V228_PROMO', {}))
rb = bool(P.get('rollback'))
builtins.V225_PROMO = {'Reversal226': False, 'Reversal': False} if rb else ({'Reversal226': True} if P.get('motion') else {})
builtins.V225_PROMO_SAVE = False
g = {'__name__': 'p228'}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/promote226.py', encoding='utf8').read(), g)
u = g['u']; abp = g['abp']; cp = g['cp']; sda = g['sda']; out = {'promo226': g['out'], 'groups': P}
KN = {}
if rb: KN.update({'SHM227_RevHold': 0.0, 'SHM227_FPOff': 0.0, 'SHM228_ClipSpeed': 0.0, 'SHM228_RelHold': 0.0, 'SHM228_CancelOn': 0.0})
if P.get('motion'): KN.update({'SHM227_RevHold': 1.0, 'SHM227_FPOff': 0.0, 'SHM228_ClipSpeed': 1.0})
if P.get('cancel'): KN.update({'SHM228_RelHold': 1.0, 'SHM228_CancelOn': 1.0})
if KN: g['set_defaults'](abp, KN)
st, errs = g['compile_ok'](abp); st2 = g['compile_ok'](cp)[0]
cdo = u.get_default_object(abp.generated_class()); out['abp_after'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM227_RevHold', 'SHM227_FPOff', 'SHM228_ClipSpeed', 'SHM228_RelHold', 'SHM228_CancelOn', 'SHM228_LeadFrames')}
out['db_after'] = {v: cdo.get_editor_property(v).get_name() for v in ('SHM224_DB_JRBwd', 'SHM224_DB_JRFwd')}
da = u.load_asset('/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior')
if rb or P.get('motion'): da.set_editor_property('GR228_ClipSpeed', 0.0 if rb else 1.0)
out['gr_after'] = float(da.get_editor_property('GR228_ClipSpeed'))
SD = {}
if rb: SD.update({'SwingLiftMax': 25.0, 'StepEdgeOn': False, 'StepEdgeShift': 12.0, 'InspectIdOn': 0.0, 'InspectFocusMode': 0.0})
if P.get('terrain'): SD['SwingLiftMax'] = 36.0
if P.get('stepedge'): SD.update({'StepEdgeOn': True, 'StepEdgeShift': 18.0})
if P.get('inspect'): SD.update({'InspectIdOn': 1.0, 'InspectFocusMode': 1.0})
for k, v in SD.items(): sda.set_editor_property(k, v)
out['shm_after'] = {k: str(sda.get_editor_property(k)) for k in ('SwingLiftMax', 'StepEdgeOn', 'StepEdgeShift', 'StepEdgeShort', 'InspectIdOn', 'InspectFocusMode', 'InspectJump', 'InspectRadius')}
ok = g['out']['ok'] and 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in str(st2)
out['ok'] = ok; out['status'] = [str(st), str(st2)]
if ok and getattr(builtins, 'V228_SAVE', False):
    g['save'](abp, cp); sda.modify(True); u.EditorAssetLibrary.save_loaded_asset(sda, False); da.modify(True); u.EditorAssetLibrary.save_loaded_asset(da, False)
    out['saved'] = True; out['dirty_after'] = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('PROMO228 ' + json.dumps(out, default=str))
