"""promote243.py (editor job, write manifest = ABP base + child, BP_GR_Player + BP_PBI_Player, DA_SHM_Response_Default): V2.43 promotion
(regression PASS required before running this). Always (candidate `latgl`):
  ABP       SHM242_DB_LatStop := PSD_SHM242_LatStop;  pawn  GR242_TurnSettleGate := True, GR243_TurnNeedsLook := True
Only with builtins.V243_PROMOTE_IDLE (candidate `idlg3`): SHME DA StanceIdleGateEnabled := False (V1.2 stance-idle hold off: the V2.6
  stops already end in the idle stance; idle = MM), ABP SHM242_IdleOn := 1, SHM242_IdleDB := builtins.V243_IDLE_DB (default PSD_SHM242_IdleB)
builtins.V243_PROMOTE_ROLLBACK = True restores the V2.42 production values instead. builtins.V243_SAVE saves. Prints PROMOTE243 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
PAWN = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'; DA = '/Game/GraceRanger/SHME/DA_SHM_Response_Default'
V42 = '/Game/GraceRanger/SHME/Animations/V242/'; RB = bool(getattr(builtins, 'V243_PROMOTE_ROLLBACK', False))
IDLE = bool(getattr(builtins, 'V243_PROMOTE_IDLE', False))          # False = lateral/turn part only (idle chain stays a candidate)
IDLE_DB = getattr(builtins, 'V243_IDLE_DB', 'PSD_SHM242_IdleB')     # hook-conforming name (must contain 'SHM242_Idle')
dirty = [p for p in LS.get_dirty_content_packages()]
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'rollback': RB, 'reloaded': [p.get_name().split('/')[-1] for p in dirty]}
bp = u.load_asset(AP); pb = u.load_asset(PAWN); da = u.load_asset(DA)
if RB:
    set_defaults(bp, {'SHM242_IdleOn': 0.0, 'SHM242_IdleDB': None, 'SHM242_DB_LatStop': u.load_asset('/Game/GraceRanger/Animations/LookStrafe/PSD_LS_CoreLateralStop')})
    set_defaults(pb, {'GR242_TurnSettleGate': False, 'GR243_TurnNeedsLook': False}); da.set_editor_property('StanceIdleGateEnabled', True)
else:
    ldb = u.load_asset(V42 + 'PSD_SHM242_LatStop'); assert ldb, 'lat DB'
    set_defaults(bp, {'SHM242_DB_LatStop': ldb}); set_defaults(pb, {'GR242_TurnSettleGate': True, 'GR243_TurnNeedsLook': True})
    if IDLE:
        idb = u.load_asset(V42 + IDLE_DB); assert idb and 'SHM242_Idle' in IDLE_DB, ('idle DB', IDLE_DB)
        set_defaults(bp, {'SHM242_IdleOn': 1.0, 'SHM242_IdleDB': idb}); da.set_editor_property('StanceIdleGateEnabled', False)
out['idle_part'] = IDLE
st, errs = compile_ok(bp); cpb = u.load_asset(CPA); st2 = compile_ok(cpb)[0]; st3, errs3 = compile_ok(pb); st4 = compile_ok(u.load_asset(CHILD))[0]
out['compile'] = [str(st), errs[:3], str(st2), str(st3), errs3[:3], str(st4)]
out['ok'] = all('UP_TO_DATE' in str(x) for x in (st, st2, st3, st4)) and not errs and not errs3
if out['ok'] and getattr(builtins, 'V243_SAVE', False):
    da.modify(); save(bp, cpb, pb, u.load_asset(CHILD)); out['saved_da'] = u.EditorAssetLibrary.save_asset(DA, False); out['saved'] = True
c1 = u.get_default_object(bp.generated_class()); c2 = u.get_default_object(pb.generated_class())
out['now'] = {'IdleOn': c1.get_editor_property('SHM242_IdleOn'), 'IdleDB': str(c1.get_editor_property('SHM242_IdleDB')), 'LatStop': str(c1.get_editor_property('SHM242_DB_LatStop')).split('/')[-1],
              'SettleGate': bool(c2.get_editor_property('GR242_TurnSettleGate')), 'NeedsLook': bool(c2.get_editor_property('GR243_TurnNeedsLook')), 'StanceIdleGate': bool(da.get_editor_property('StanceIdleGateEnabled'))}
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('PROMOTE243 ' + json.dumps(out, default=str))
