"""promote252.py (editor job, write manifest = ABP base + child): V2.52 promotion - walk start-transfer databases := the anticipatory
weight transfer databases (PSD_SHM252_StartTransferAPA_L / _R), SHM252_YawTau := 0.08 (smooth yaw hand-over); SHM252_KeepRM stays 0.
builtins.V252_PROM = 'promote' | 'rollback'. Prints PROMOTE252 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
mode = getattr(builtins, 'V252_PROM', 'promote'); out = {'mode': mode}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty: out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
if mode == 'promote': dbl, dbr, tau = '/Game/GraceRanger/SHME/Animations/V252/PSD_SHM252_StartTransferAPA_L', '/Game/GraceRanger/SHME/Animations/V252/PSD_SHM252_StartTransferAPA_R', 0.08
else: dbl, dbr, tau = '/Game/GraceRanger/SHME/Animations/StartTransfer/PSD_SHM_StartTransfer_L', '/Game/GraceRanger/SHME/Animations/StartTransfer/PSD_SHM_StartTransfer_R', 0.0
bp = u.load_asset(AP); set_defaults(bp, {'SHM_StartTransferDB_L': u.load_asset(dbl), 'SHM_StartTransferDB_R': u.load_asset(dbr), 'SHM252_YawTau': tau, 'SHM252_KeepRM': 0.0})
st_, errs = compile_ok(bp); cpb = u.load_asset(CPA); st2 = compile_ok(cpb)[0]
cdo = u.get_default_object(bp.generated_class()); ccdo = u.get_default_object(cpb.generated_class())
gv = lambda o, k: (lambda v: v.get_name() if hasattr(v, 'get_name') else str(v))(o.get_editor_property(k))
out['now'] = {k: gv(cdo, k) for k in ('SHM_StartTransferDB_L', 'SHM_StartTransferDB_R', 'SHM252_YawTau', 'SHM252_KeepRM', 'SHM251_StartEntry', 'SHM251_YawSlew', 'SHM251_StartLoad', 'SHM249_RM')}
out['child'] = {k: gv(ccdo, k) for k in ('SHM_StartTransferDB_L', 'SHM_StartTransferDB_R', 'SHM252_YawTau')}
out['ok'] = all('UP_TO_DATE' in str(x) for x in (st_, st2)) and not errs and out['now']['SHM_StartTransferDB_L'] == dbl.split('/')[-1] and out['child']['SHM_StartTransferDB_L'] == dbl.split('/')[-1]
if out['ok']: save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('PROMOTE252 ' + json.dumps(out, default=str))
