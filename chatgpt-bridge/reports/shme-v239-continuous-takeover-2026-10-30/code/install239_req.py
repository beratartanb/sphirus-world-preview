"""install239_req.py (editor job) - V2.39: the takeover database switch happens AT THE REQUEST (after install239_own / _tkon).
Measured (v239f/g j39_rl_tk / rw_tk): switching on the touchdown into clips that START at the touchdown let motion matching pick a mid-run
frame of another takeover clip (root-relative features: a late running frame already heading to the new side matched better than the
exact braking frame 0; a lower trajectory weight did not change it). Takeover clips now carry their PREFIX (an exact copy of the source cut
up to contact K, gen239_tk prefix mode) - at the request the current cut frame exists identically (pose AND past trajectory) in the
takeover clips of this source whose contact K is still ahead; their future trajectory chooses the target (Back / Opp) and the nearest K;
the divergence then happens inside the clip at the planned touchdown.
  SHM239_StepN := curve SHM239_StepN (last contact index a takeover exists for; cut clips + takeover clips carry it)
  SHM239_TkGo  := request AND 1 <= SHM239_Step <= SHM239_StepN (the next contact K = Step has a takeover clip)   [was: request AND step edge]
Idempotent (marker SHM239_StepN variable). builtins.V239_SAVE saves. Prints REQ239 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': names}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
bp = u.load_asset(AP)
if 'SHM239_StepN' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM239_StepN', 'float', 'SHM239')]); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    first = [p for p in sn if tid(p).endswith('SetSHM239_TgtC')]; assert len(first) == 1
    nx = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (first[0], 'then') in src((p, 'execute'))]
    for x in nx: disconnect((x, 'execute'))
    t = gs.set('SHM239_StepN', gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM239_StepN'}), (first[0], 'then'))
    for x in nx: connect(t, (x, 'execute'))
    go = [p for p in sn if tid(p).endswith('SetSHM239_TkGo')]; assert len(go) == 1
    a = src((go[0], 'SHM239_TkGo')); assert len(a) == 1
    ab = src((a[0][0], 'B')); assert len(ab) == 1, 'TkGo = AND(req, stepup) expected'
    disconnect((a[0][0], 'B'))
    stepok = gs.AND(gs.within(gs.get('SHM239_Step'), 0.5, 1.0e9), gs.within(gs.math(gs.get('SHM239_StepN'), gs.get('SHM239_Step'), -1), 0.0, 1.0e9))
    connect(stepok, (a[0][0], 'B')); out['patch'] = 'TkGo = req AND 1 <= Step <= StepN'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]
cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
ok = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
out['ok'] = ok
if ok and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('REQ239 ' + json.dumps(out, default=str))
