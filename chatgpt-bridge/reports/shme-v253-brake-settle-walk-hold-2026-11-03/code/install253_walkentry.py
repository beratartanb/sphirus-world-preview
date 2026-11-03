"""install253_walkentry.py (editor job, write manifest = ABP base + child): V2.53 REQUEST-FRAME WALK START DATABASE (knob SHM253_WalkEntry,
default 0 = production unchanged).
Measured (stance253.py + selection trace, V2.52 production, every walk start from rest at 30 / 60 / 120 FPS): on the request frame the walk
start route is one frame late and Motion Matching searches a vendor database (PSD_Dense_Stand_Walk_Loops: Walk_Loop_F_R_20 / Shuffle,
PSD_CR_Backward_Stand: Walk_Start_B/BR/BL); the start-transfer clip follows on the next frame. That one sample stays in the blend stack and
its own blend-in keeps rising under the next one (nested cross-fade: ~12 % at +0.10 s, ~25 % at +0.2 s), so the planted stance foot of
the visible body swims 9-11 cm forward and back while flat on the floor (25 cm path, 4-5 cm net) before FootPlacement re-locks it - the same
mechanism V2.51 removed for the jog starts (SHM251_StartEntry).
Patch (Update_MotionMatching, in front of the V2.51 jog entry branch on the false path of the V2.49 entry branch IfThenElse_84):
  Branch(SHM253_WalkEntry > 0.5 AND GroundSpeed < SHM249_RestSpeed AND HasAcceleration AND SHM_StartGait in [-0.5, 0.5] AND the current
  database name does not contain 'StartTransfer') -> SetDatabaseToSearch(side ? SHM_StartTransferDB_L : SHM_StartTransferDB_R)
  (side = the walk route's own InRange(SHM_StartSide) node, the database the family route searches on the next frame), same interrupt mode;
  else the old flow (V2.51 jog entry, then the rest).
Idempotent (variable SHM253_WalkEntry). builtins.V253_SAVE saves. Prints WALKENTRY253 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def succ(p, pin='then'):
    return [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for o in info(p).output_pins if str(o.name) == pin for q in o.connected_pins]
def db_var_of(p):
    s_ = src((p, 'Database'))
    return str(info(s_[0][0]).type_id).rsplit('|', 1)[-1] if s_ else ''
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
need = ['SHM251_StartEntry', 'SHM249_RestSpeed', 'SHM_StartGait', 'SHM_StartTransferDB_L', 'SHM_StartTransferDB_R', 'GroundSpeed', 'HasAcceleration', 'SHM_StartSide']
out['missing'] = [v for v in need if v not in V]; assert not out['missing'], out['missing']
if 'SHM253_WalkEntry' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM253_WalkEntry', 'float', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM253_WalkEntry': 0.0}); compile_ok(bp)
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
    br84 = N['K2Node_IfThenElse_84']; assert 'IfThenElse' in br84
    old_else = succ(br84, 'else'); assert len(old_else) == 1, old_else
    # the walk route's own calls: SetDatabaseToSearch(SHM_StartTransferDB_L) behind Branch(isStart AND InRange(StartSide, -1, 0.5))
    calls = {s: [p for p in N.values() if 'SetDatabaseToSearch' in tid(p) and db_var_of(p).endswith('SHM_StartTransferDB_' + s)] for s in 'LR'}
    out['walk_calls'] = {s: [c.rsplit('.', 1)[-1] for c in v] for s, v in calls.items()}
    assert len(calls['L']) >= 1 and len(calls['R']) >= 1, calls
    ref = calls['L'][0]; mm = src((ref, 'MotionMatchingNode'))[0]; mode = [str(x.value) for x in info(ref).input_pins if str(x.name) == 'InterruptMode'][0]
    side = (N['K2Node_CallFunction_297'], 'ReturnValue'); assert 'InRange' in tid(side[0]), tid(side[0])
    vs = src((side[0], 'Value')); out['side_src'] = [tid(vs[0][0]) if vs else None, [str(x.value) for x in info(side[0]).input_pins if str(x.name) in ('Min', 'Max')]]
    assert vs and 'SHM_StartSide' in tid(vs[0][0]), out['side_src']
    disconnect((old_else[0][0], old_else[0][1]))
    dbn = g.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': g.get('CurrentSelectedDatabase')})
    notWalkStart = g.NOT(g.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': dbn, 'Substring': 'StartTransfer', 'bUseCase': False, 'bSearchFromEnd': False}))
    cond = g.AND(g.AND(g.within(g.get('SHM253_WalkEntry'), 0.5, 1.0e9), g.within(g.get('GroundSpeed'), -1.0, g.get('SHM249_RestSpeed'))),
                 g.AND(g.AND(g.get('HasAcceleration'), g.within(g.get('SHM_StartGait'), -0.5, 0.5)), notWalkStart))
    bt, bf = g.branch(cond, (br84, 'else'))
    connect(bf, old_else[0])
    sbt, sbf = g.branch(side, bt)
    for br_, var in ((sbt, 'SHM_StartTransferDB_L'), (sbf, 'SHM_StartTransferDB_R')):
        s = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(br_, (s, 'execute'))
        connect(mm, (s, 'MotionMatchingNode')); connect(g.get(var), (s, 'Database')); arg(s, 'InterruptMode', mode)
    out['entry'] = {'else_was': old_else[0][0].rsplit('.', 1)[-1], 'mode': mode, 'side_node': 'K2Node_CallFunction_297'}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM253_WalkEntry'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V253_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('WALKENTRY253 ' + json.dumps(out, default=str))
