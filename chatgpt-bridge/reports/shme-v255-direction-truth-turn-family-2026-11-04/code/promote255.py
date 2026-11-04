"""promote255.py (editor job, write manifest = ABP base + child + DA_SHM_Response_Default + BP_GR_Player + BP_PBI_Player): V2.55 promotion / rollback.
builtins.V255_PROM = {'mode': 'promote'|'rollback', 'head': bool, 'frame': bool}.
promote: the ABP defaults of the measured candidate (Saved/Codex/SHME_V255_20261104/req/c5_flags.json: Ctl, routes, cut DBs, cancel threshold, JogB, retired old reversal routes), DA EffortScaleMin 0.85,
pawn GR255_RawOn 1, GR255_FrameV1 320. Option head: ABP SHM240_HeadOn 1 (AO head / shoulder twist). Option frame: pawn GR255_FrameOn 1 (speed framing).
The values in place before the promotion go to data/promote255_before.json (once); rollback restores exactly those. Prints PROMOTE255 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
import builtins, json, pathlib
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
DA = '/Game/GraceRanger/SHME/DA_SHM_Response_Default'; PB = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
PD = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/SHME_V255_20261104'; BEFORE = PD / 'data/promote255_before.json'
cfg = dict(getattr(builtins, 'V255_PROM', {})); mode = cfg.get('mode', 'promote'); out = {'cfg': cfg}
dirty = [p for p in LS.get_dirty_content_packages() if any(x in p.get_name() for x in ('ABP_GR_MotionMatching', 'DA_SHM_Response_Default', 'BP_GR_Player', 'BP_PBI_Player'))]
if dirty: out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
FL = json.loads((PD / 'req/c5_flags.json').read_text()); FL['SHM240_HeadOn'] = 1.0 if cfg.get('head') else None
ABPK = [k for k in FL]; DAK = ['EffortScaleMin']; PAWNK = ['GR255_RawOn', 'GR255_FrameOn', 'GR255_FrameV1']
bp = u.load_asset(AP); cdo = u.get_default_object(bp.generated_class()); da = u.load_asset(DA); pb = u.load_asset(PB); pcdo = u.get_default_object(pb.generated_class())
def pv(v): return v.get_path_name().split('.')[0] if hasattr(v, 'get_path_name') else v
def rd(): return {'abp': {k: pv(cdo.get_editor_property(k)) for k in ABPK}, 'da': {k: da.get_editor_property(k) for k in DAK}, 'pawn': {k: pcdo.get_editor_property(k) for k in PAWNK}}
now = rd()
if not BEFORE.exists(): BEFORE.write_text(json.dumps(now, indent=1, default=str)); out['before_written'] = True
before = json.loads(BEFORE.read_text())
def conv(v): return u.load_asset(v) if isinstance(v, str) and v.startswith('/Game/') else v
if mode == 'rollback':
    abpv = {k: conv(v) for k, v in before['abp'].items()}; dav = dict(before['da']); pawnv = dict(before['pawn'])
else:
    abpv = {k: conv(v) for k, v in FL.items() if v is not None}; dav = {'EffortScaleMin': 0.85}; pawnv = {'GR255_RawOn': 1.0, 'GR255_FrameOn': 1.0 if cfg.get('frame') else 0.0, 'GR255_FrameV1': 320.0}
    assert all(v is not None for v in abpv.values()), 'missing asset'
set_defaults(bp, abpv); st_, errs = compile_ok(bp); cpb = u.load_asset(CPA); st2 = compile_ok(cpb)[0]
set_defaults(pb, pawnv); st3, errs3 = compile_ok(pb); ch = u.load_asset(CHILD); st4 = compile_ok(ch)[0]
for k, v in dav.items(): da.set_editor_property(k, v)
out['compile'] = [str(st_), str(st2), str(st3), str(st4), errs[:3], errs3[:3]]
after = rd(); out['after_keys'] = {k: (str(v).rsplit('/', 1)[-1]) for k, v in after['abp'].items()}; out['after_da'] = after['da']; out['after_pawn'] = after['pawn']
def same(a, b):
    if isinstance(b, (int, float)) and not isinstance(b, bool) and isinstance(a, (int, float)): return abs(float(a) - float(b)) < 1e-4
    return a == b
exp = {k: pv(v) for k, v in abpv.items()}
out['ok'] = all('UP_TO_DATE' in x for x in out['compile'][:4]) and not errs and not errs3 and all(same(after['abp'][k], exp[k]) for k in exp) and all(same(after['da'][k], v) for k, v in dav.items()) and all(same(after['pawn'][k], v) for k, v in pawnv.items())
if out['ok']:
    save(bp, cpb, pb, ch); assert u.EditorAssetLibrary.save_loaded_asset(da, False); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('PROMOTE255 ' + json.dumps(out, default=str))
