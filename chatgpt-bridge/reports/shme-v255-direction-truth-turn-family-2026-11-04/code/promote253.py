"""promote253.py (editor job, write manifest = ABP base + child): V2.53 promotion. builtins.V253_PROM = {'mode': 'promote'|'rollback',
'walk_entry': bool, 'walk_hold': bool, 'apa3': bool, 'settle': bool}. promote: SHM253_WalkEntry 1 (request-frame walk start database) / SHM253_WalkHold 1 (request-frame hold), walk start-transfer
databases := PSD_SHM253_StartTransferAPA_L/_R (APA v3), jog stop database SHM236_DB_JogStop := PSD_SHM253_JogStop (post-brake settle), each
only when its key is true. rollback = V2.52 values (WalkEntry 0, PSD_SHM252_StartTransferAPA_*, PSD_SHM237_JogStop).
The crop kink re-key (fix253_cropkink.py) is content (manifest v253_kink backups) and is not touched here. Prints PROMOTE253 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
cfg = dict(getattr(builtins, 'V253_PROM', {})); mode = cfg.get('mode', 'promote'); out = {'cfg': cfg}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty: out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
V2, V3 = '/Game/GraceRanger/SHME/Animations/V252/', '/Game/GraceRanger/SHME/Animations/V253/'
pro = mode == 'promote'
vals = {'SHM253_WalkEntry': 1.0 if (pro and cfg.get('walk_entry')) else 0.0, 'SHM253_WalkHold': 1.0 if (pro and cfg.get('walk_hold')) else 0.0,
        'SHM_StartTransferDB_L': u.load_asset((V3 + 'PSD_SHM253_StartTransferAPA_L') if (pro and cfg.get('apa3')) else (V2 + 'PSD_SHM252_StartTransferAPA_L')),
        'SHM_StartTransferDB_R': u.load_asset((V3 + 'PSD_SHM253_StartTransferAPA_R') if (pro and cfg.get('apa3')) else (V2 + 'PSD_SHM252_StartTransferAPA_R')),
        'SHM236_DB_JogStop': u.load_asset((V3 + 'PSD_SHM253_JogStop') if (pro and cfg.get('settle')) else '/Game/GraceRanger/SHME/Animations/V237/PSD_SHM237_JogStop')}
assert all(v is not None for v in vals.values()), vals
bp = u.load_asset(AP); set_defaults(bp, vals)
st_, errs = compile_ok(bp); cpb = u.load_asset(CPA); st2 = compile_ok(cpb)[0]
cdo = u.get_default_object(bp.generated_class()); ccdo = u.get_default_object(cpb.generated_class())
gv = lambda o, k: (lambda v: v.get_name() if hasattr(v, 'get_name') else str(v))(o.get_editor_property(k))
out['now'] = {k: gv(cdo, k) for k in list(vals) + ['SHM252_YawTau', 'SHM251_StartEntry', 'SHM249_RM']}
out['child'] = {k: gv(ccdo, k) for k in vals}
exp = {k: (v.get_name() if hasattr(v, 'get_name') else str(v)) for k, v in vals.items()}
out['ok'] = all('UP_TO_DATE' in str(x) for x in (st_, st2)) and not errs and all(out['now'][k] == exp[k] and out['child'][k] == exp[k] for k in vals)
if out['ok']: save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('PROMOTE253 ' + json.dumps(out, default=str))
