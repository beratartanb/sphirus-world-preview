"""promote254.py (editor job, write manifest = ABP base + child [+ DA_SHM_Response_Default when cam]): V2.54 promotion / rollback.
builtins.V254_PROM = {'mode': 'promote'|'rollback', 'turn': bool, 'cut': bool, 'cam': bool}.
promote, turn: SHM254_Turn 1 + the sprint reversal routes SHM_RedirectDB_SR / _SRL / _SRR and SHM212_RouteSRL / _SRR := PSD_SHM254_SprintRev
  (the authored brake -> plant -> transfer -> re-push turn-around; runtime install254_turn / hold / v2..v5 are inert while SHM254_Turn is 0).
promote, cut: SHM_RedirectDB_SL := PSD_SHM254_SprintCut (sprint 90 brake-cut; needs SHM254_Turn 1 for its yaw sign / hand-over).
promote, cam: DA_SHM_Response_Default CamSwapV21Enabled false (no automatic shoulder swap) + CamClose Stand/Walk 0.86, Jog 1.0, Sprint 1.06, Tau 1.0.
The values in place before the promotion are written to data/promote254_before.json (once); rollback restores exactly those.
Prints PROMOTE254 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
import builtins, json, pathlib
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
DA = '/Game/GraceRanger/SHME/DA_SHM_Response_Default'; V4 = '/Game/GraceRanger/SHME/Animations/V254/'
BEFORE = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/SHME_V254_20261104/data/promote254_before.json'
cfg = dict(getattr(builtins, 'V254_PROM', {})); mode = cfg.get('mode', 'promote'); out = {'cfg': cfg}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name() or 'DA_SHM_Response_Default' in p.get_name()]
if dirty: out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
ABPK = ['SHM254_Turn', 'SHM_RedirectDB_SR', 'SHM_RedirectDB_SRL', 'SHM_RedirectDB_SRR', 'SHM212_RouteSRL', 'SHM212_RouteSRR', 'SHM_RedirectDB_SL']
CAMK = ['CamSwapV21Enabled', 'CamCloseStand', 'CamCloseWalk', 'CamCloseJog', 'CamCloseSprint', 'CamCloseTau']
bp = u.load_asset(AP); cdo = u.get_default_object(bp.generated_class()); da = u.load_asset(DA)
def pv(v): return v.get_path_name().split('.')[0] if hasattr(v, 'get_path_name') else v
def rd():
    return {'abp': {k: pv(cdo.get_editor_property(k)) for k in ABPK}, 'da': {k: da.get_editor_property(k) for k in CAMK}}
now = rd()
if not BEFORE.exists(): BEFORE.write_text(json.dumps(now, indent=1, default=str)); out['before_written'] = True
before = json.loads(BEFORE.read_text())
abpv, dav = {}, {}
if mode == 'rollback':
    abpv = {k: (u.load_asset(v) if isinstance(v, str) and v.startswith('/Game/') else v) for k, v in before['abp'].items()}; dav = dict(before['da'])
else:
    if cfg.get('turn'):
        rev = u.load_asset(V4 + 'PSD_SHM254_SprintRev'); assert rev
        abpv.update({'SHM254_Turn': 1.0, 'SHM_RedirectDB_SR': rev, 'SHM_RedirectDB_SRL': rev, 'SHM_RedirectDB_SRR': rev, 'SHM212_RouteSRL': rev, 'SHM212_RouteSRR': rev})
    if cfg.get('cut'):
        assert cfg.get('turn'), 'cut needs turn'; cut = u.load_asset(V4 + 'PSD_SHM254_SprintCut'); assert cut; abpv['SHM_RedirectDB_SL'] = cut
    if cfg.get('cam'):
        dav = {'CamSwapV21Enabled': False, 'CamCloseStand': 0.86, 'CamCloseWalk': 0.86, 'CamCloseJog': 1.0, 'CamCloseSprint': 1.06, 'CamCloseTau': 1.0}
if abpv:
    set_defaults(bp, abpv); st_, errs = compile_ok(bp); cpb = u.load_asset(CPA); st2 = compile_ok(cpb)[0]
    out['abp_ok'] = 'UP_TO_DATE' in str(st_) and 'UP_TO_DATE' in str(st2) and not errs
else: cpb = None; out['abp_ok'] = True
for k, v in dav.items(): da.set_editor_property(k, v)
after = rd(); out['after'] = after
exp_abp = {k: pv(v) for k, v in abpv.items()}
out['ok'] = out['abp_ok'] and all(after['abp'][k] == exp_abp[k] for k in exp_abp) and all(abs(float(after['da'][k]) - float(v)) < 1e-4 if not isinstance(v, bool) else after['da'][k] == v for k, v in dav.items())
if out['ok']:
    if abpv: save(bp, cpb)
    if dav: assert u.EditorAssetLibrary.save_loaded_asset(da, False)
    out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('PROMOTE254 ' + json.dumps(out, default=str))
