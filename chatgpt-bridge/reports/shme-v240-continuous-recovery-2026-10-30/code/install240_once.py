"""install240_once.py (editor job) - V2.40: the takeover switch is decided by what motion matching ACTUALLY selected, not by frame counts or
a blending curve (behind SHM239_Own; after all V2.39 installers).
First real cause of the V2.39 120 FPS failures (v239x120_j39_rw_tk 116 cm, cc90 112 cm; 30 FPS counter-example v239reg_j39_rw_tk 0 cm):
the switch latch ended when the takeover clip's target curve SHM239_Tgt - a BLENDED value - passed 20, and re-forced the search on
alternate frames for up to 16 frames. At 120 FPS a frame moves the 0.05 s blend only ~17 %, the curve read 4 -> 14, the latch never
closed, and every second frame a new forced search restarted the selection: P21_K1 -> P10_K1 -> P22_K4 -> P00_K4 -> P15_K4 ... for 0.35 s
(the feet are dragged by the hopping). At 30 FPS one frame was long enough to pass 20, so it closed after one force. (Category E -> A.)
Now (no new bias / hold / duration):
  SHM240_TkDone := SHM239_OwnOn AND (TkDone OR CurrentSelectedDatabase is a takeover database)   (PostSelection = the real selection)
  SHM239_TkGo   := <V2.39 request AND contact available> AND NOT TkDone
  SHM239_TkOn   := TkGo AND Now - SHM240_TkT >= SHM240_Retry (0.05 s)  -> ONE forced search; a retry only by time (DB not ready yet)
  SHM240_TkT    := Now on a force
  SHM239_TkPlay := SHM239_Own AND TkDone AND SHM239_W > 0.3          (play database + throttle as soon as the entry is CONFIRMED)
Idempotent (marker SHM240_TkDone). builtins.V240_SAVE saves. Prints ONCE240 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {'reloaded': names}
bp = u.load_asset(AP)
if 'SHM240_TkDone' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM240_TkDone', 'bool', 'SHM240'), ('SHM240_TkT', 'float', 'SHM240'), ('SHM240_Retry', 'float', 'SHM240')]); compile_ok(bp)
    set_defaults(bp, {'SHM240_Retry': 0.05}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    one = lambda sfx: [p for p in sn if tid(p).endswith(sfx)]
    go, on, play = one('SetSHM239_TkGo'), one('SetSHM239_TkOn'), one('SetSHM239_TkPlay'); assert len(go) == 1 and len(on) == 1 and len(play) == 1
    now = gs.pure('Now')
    # object '==' is a promotable operator (refused): the selected database's NAME carries the takeover prefix
    nm = gs.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': gs.get('CurrentSelectedDatabase')})
    istk = gs.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': nm, 'Substring': 'PSD_SHM239_Tk', 'bUseCase': False, 'bSearchFromEnd': False})
    # TkDone just before the TkGo setter (TkGo reads it this frame)
    pre = src((go[0], 'execute')); assert len(pre) == 1; disconnect((go[0], 'execute'))
    t = gs.set('SHM240_TkDone', gs.AND(gs.get('SHM239_OwnOn'), gs.OR(gs.get('SHM240_TkDone'), istk)), pre[0]); connect(t, (go[0], 'execute'))
    old = src((go[0], 'SHM239_TkGo')); assert len(old) == 1; disconnect((go[0], 'SHM239_TkGo'))
    connect(gs.AND(old[0], gs.NOT(gs.get('SHM240_TkDone'))), (go[0], 'SHM239_TkGo'))
    # TkOn: one forced search, retry only by time
    disconnect((on[0], 'SHM239_TkOn'))
    connect(gs.AND(gs.get('SHM239_TkGo'), gs.within(gs.sub(now, gs.get('SHM240_TkT')), gs.get('SHM240_Retry'), 1.0e9)), (on[0], 'SHM239_TkOn'))
    nx = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (on[0], 'then') in src((p, 'execute'))]
    for x in nx: disconnect((x, 'execute'))
    t = gs.set('SHM240_TkT', gs.select(gs.get('SHM239_TkOn'), now, gs.get('SHM240_TkT')), (on[0], 'then'))
    for x in nx: connect(t, (x, 'execute'))
    # TkPlay on the CONFIRMED entry
    disconnect((play[0], 'SHM239_TkPlay'))
    connect(gs.AND(gs.AND(gs.within(gs.get('SHM239_Own'), 0.5, 1.0e9), gs.get('SHM240_TkDone')), gs.within(gs.get('SHM239_W'), 0.3, 1.0e9)), (play[0], 'SHM239_TkPlay'))
    out['patch'] = 'one-shot force, confirmed-entry done/play'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V240_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('ONCE240 ' + json.dumps(out, default=str))
