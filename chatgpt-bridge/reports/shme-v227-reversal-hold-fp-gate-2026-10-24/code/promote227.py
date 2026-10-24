"""promote227.py (editor job): V2.27 production switch = promote226 with Reversal226 True (ABP CDO SHM224_DB_JRBwd/BwdM/Fwd/FwdM -> the 32-bin
PSD_SHM226_JogRevBwd/Fwd databases) + the ABP knobs SHM227_RevHold / SHM227_FPOff (builtins.V227_KNOBS, default 1.0 / 1.0; 0/0 = rollback
together with V227_REV False). builtins.V227_SAVE saves. Prints PROMO227 {...}."""
import builtins, json
REV = bool(getattr(builtins, 'V227_REV', True)); KN = dict({'SHM227_RevHold': 1.0, 'SHM227_FPOff': 1.0}, **getattr(builtins, 'V227_KNOBS', {}))
builtins.V225_PROMO = {'Reversal226': REV} if REV else {'Reversal226': False, 'Reversal': False}
builtins.V225_PROMO_SAVE = False
g = {'__name__': 'p227'}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/promote226.py', encoding='utf8').read(), g)
u = g['u']; abp = g['abp']; cp = g['cp']; sda = g['sda']; out = {'promo226': g['out'], 'rev': REV, 'knobs_target': KN}
g['set_defaults'](abp, KN); st, errs = g['compile_ok'](abp); st2 = g['compile_ok'](cp)[0]
cdo = u.get_default_object(abp.generated_class()); out['knobs_after'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM227_RevHold', 'SHM227_FPOff', 'SHM227_HoldExit', 'SHM227_FlatMax')}
out['db_after'] = {v: cdo.get_editor_property(v).get_name() for v in ('SHM224_DB_JRBwd', 'SHM224_DB_JRBwdM', 'SHM224_DB_JRFwd', 'SHM224_DB_JRFwdM')}
ok = g['out']['ok'] and 'UP_TO_DATE' in str(st) and not errs and all(abs(out['knobs_after'][k] - v) < 1e-6 for k, v in KN.items()) and (out['db_after']['SHM224_DB_JRBwd'] == ('PSD_SHM226_JogRevBwd' if REV else 'PSD_SHM224_JogRevBwdO'))
out['ok'] = ok; out['status'] = [str(st), str(st2)]
if ok and getattr(builtins, 'V227_SAVE', False):
    g['save'](abp, cp); sda.modify(True); u.EditorAssetLibrary.save_loaded_asset(sda, False)
    out['saved'] = True; out['dirty_after'] = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('PROMO227 ' + json.dumps(out, default=str))
