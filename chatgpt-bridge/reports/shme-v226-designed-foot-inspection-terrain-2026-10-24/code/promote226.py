"""promote226.py (editor job): V2.26 production (V2.25 keys + Reversal226 = the 32-bin databases, StepEdge, InspectZoom). Decision in builtins.V225_PROMO (keys below, defaults = keep current); every value written is
read back. builtins.V225_PROMO_SAVE saves.
  Reversal  True : ABP_GR_MotionMatchingBase CDO SHM224_DB_JRBwd / JRBwdM -> PSD_SHM225_JogRevBwd, SHM224_DB_JRFwd / JRFwdM -> PSD_SHM225_JogRevFwd
                   (the authored brake-support-push clips, 8 phase bins per family, serve the V2.24 request-identity route). Rollback: the
                   V2.24 databases (PSD_SHM224_JogRevBwdO / BwdM / FwdO / FwdM).
  StepPrep  bool : DA_SHM_Response_Default StepPrepEnabled (planned step preparation on the pelvis owner; the T1 lift-gate fix is code).
  Inspect   bool : DA_SHM_Response_Default CamInspectEnabled (inspection camera + look-at).
Refuses with PIE or unexpected dirty packages; prints PROMO225 {before, after, saved}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
SDA = '/Game/GraceRanger/SHME/DA_SHM_Response_Default'; GDA = '/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior'
V5 = '/Game/GraceRanger/SHME/Animations/V225/'; V6 = '/Game/GraceRanger/SHME/Animations/V226/'; V4 = '/Game/GraceRanger/SHME/Animations/V224/'
DAS = {GDA, SDA, '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
D = dict(getattr(builtins, 'V225_PROMO', {}))
abp = u.load_asset(AP); cdo = u.get_default_object(abp.generated_class()); sda = u.load_asset(SDA)
DBV = ('SHM224_DB_JRBwd', 'SHM224_DB_JRBwdM', 'SHM224_DB_JRFwd', 'SHM224_DB_JRFwdM')
def rd(): return dict({v: cdo.get_editor_property(v).get_name() for v in DBV}, **{k: sda.get_editor_property(k) for k in ('StepPrepEnabled', 'CamInspectEnabled', 'SwingLiftEnabled', 'CamFollowEnabled', 'StepEdgeOn', 'InspectZoomOn', 'SwingLiftMargin')})
out = {'before': rd(), 'decision': D}
if 'Reversal226' in D and D['Reversal226']:   # V2.26: the 32-bin clips
    tgt = {'SHM224_DB_JRBwd': V6 + 'PSD_SHM226_JogRevBwd', 'SHM224_DB_JRBwdM': V6 + 'PSD_SHM226_JogRevBwd', 'SHM224_DB_JRFwd': V6 + 'PSD_SHM226_JogRevFwd', 'SHM224_DB_JRFwdM': V6 + 'PSD_SHM226_JogRevFwd'}
    for v, pth in tgt.items():
        a = u.load_asset(pth); assert a, pth; set_defaults(abp, {v: a})
if 'Reversal' in D:
    tgt = {'SHM224_DB_JRBwd': V5 + 'PSD_SHM225_JogRevBwd', 'SHM224_DB_JRBwdM': V5 + 'PSD_SHM225_JogRevBwd', 'SHM224_DB_JRFwd': V5 + 'PSD_SHM225_JogRevFwd', 'SHM224_DB_JRFwdM': V5 + 'PSD_SHM225_JogRevFwd'} if D['Reversal'] else \
          {'SHM224_DB_JRBwd': V4 + 'PSD_SHM224_JogRevBwdO', 'SHM224_DB_JRBwdM': V4 + 'PSD_SHM224_JogRevBwdM', 'SHM224_DB_JRFwd': V4 + 'PSD_SHM224_JogRevFwdO', 'SHM224_DB_JRFwdM': V4 + 'PSD_SHM224_JogRevFwdM'}
    for v, p in tgt.items():
        a = u.load_asset(p); assert a, p; set_defaults(abp, {v: a})
st, errs = compile_ok(abp); cp = u.load_asset(CP); st2 = compile_ok(cp)[0]
cdo = u.get_default_object(abp.generated_class())
for k, dk in (('StepPrepEnabled', 'StepPrep'), ('CamInspectEnabled', 'Inspect'), ('StepEdgeOn', 'StepEdge'), ('InspectZoomOn', 'InspectZoom')):
    if dk in D: sda.set_editor_property(k, bool(D[dk]))
for k, v in getattr(builtins, 'V226_PROMO_EXTRA', {}).items(): sda.set_editor_property(k, v)   # V2.26: tuned knobs (SwingLiftMargin with the T3g lift)
out['after'] = rd(); out['status'] = [str(st), str(st2)]
a = out['after']
ok = 'UP_TO_DATE' in str(st) and not errs and ('Reversal226' not in D or not D['Reversal226'] or a['SHM224_DB_JRBwd'] == 'PSD_SHM226_JogRevBwd') and ('Reversal' not in D or (a['SHM224_DB_JRBwd'] == ('PSD_SHM225_JogRevBwd' if D['Reversal'] else 'PSD_SHM224_JogRevBwdO')))
out['ok'] = ok
if ok and getattr(builtins, 'V225_PROMO_SAVE', False):
    save(abp, cp); sda.modify(True); u.EditorAssetLibrary.save_loaded_asset(sda, False)
    out['saved'] = True; out['dirty_after'] = [p.get_name() for p in LS.get_dirty_content_packages()]
print('PROMO226 ' + json.dumps(out, default=str))
