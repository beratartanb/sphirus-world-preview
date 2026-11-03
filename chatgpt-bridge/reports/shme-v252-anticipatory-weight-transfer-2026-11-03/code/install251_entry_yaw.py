"""install251_entry_yaw.py (editor job, write manifest = ABP base + child): two V2.51 fixes, each behind its own knob (default 0 = production
unchanged).
(A) SHM251_StartEntry - REQUEST-FRAME START DATABASE for every jog start from rest. Measured (v250d60 jstart, 4 of 4 rest starts): on the
    request frame the family route is one frame late and Motion Matching searches the vendor dense databases: PSD_Dense_Stand_Run_Starts
    (af_Loco_Jog_Right/Bwd_Start_AAMS = the BROKEN CoreMotionAAMS/Candidate retarget, feet pitched down and back) or Dense_Stand_Run_Loops
    (Shuffle). That one sample enters the blend stack and fades out over ~0.15 s: both balls sink 6-7 cm at the 45 deg start (TurnR045),
    the lateral start (A_LS_Jog_Right_Start) and the backward start. V2.49 fixed this only for the turning starts (IfThenElse_84).
    Patch: on the false path of the V2.49 entry branch, Branch(StartEntry > 0.5 AND GroundSpeed < SHM249_RestSpeed AND HasAcceleration AND
    SHM_StartGait in [0.5, 1.5] AND the current database is not an SHM start database) -> SetDatabaseToSearch(StartSide ? SHM_JogStartDB_L :
    SHM_JogStartDB_R) (= the database the family route searches on the next frame), same node / interrupt mode; else the old flow.
(B) SHM251_YawSlew - CONTINUOUS YAW HAND-OVER after the V2.49 servo. Measured (v250d60 jstart 15.017 -> 15.033): the servo writes ClipYaw from
    the clip ROOT yaw curve (264.2), the V2.38 contract that takes over writes it from the normalised turn progress (89.5/90 -> 270.6):
    the capsule (and the whole body) snaps 6.4 deg in one 60 FPS frame -> shoulder 77 m/s2. Patch (SHM_Snapshot, after SetSHM249_PrevServo):
    SHM251_HandT := Servo ? 0 : HandT + dt; while NOT Servo AND HandT < SHM251_HandWin (0.35 s) the component ClipYaw approaches its target
    at most SHM251_YawRate (150 deg/s) * dt from the last applied yaw (NormalizeAxis error, FClamp); PrevYaw / PrevOn track the applied value.
Idempotent (variable SHM251_StartEntry). builtins.V251_SAVE saves. Prints ENTRYYAW251 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def succ(p, pin='then'):
    return [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for o in info(p).output_pins if str(o.name) == pin for q in o.connected_pins]
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
need = ['SHM249_Servo', 'SHM249_RestSpeed', 'SHM_StartGait', 'SHM_JogStartDB_L', 'SHM_JogStartDB_R', 'GroundSpeed', 'HasAcceleration']
out['missing'] = [v for v in need if v not in V]; assert not out['missing'], out['missing']
if 'SHM251_StartEntry' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM251_StartEntry', 'float', 'SHM'), ('SHM251_YawSlew', 'float', 'SHM'), ('SHM251_YawRate', 'float', 'SHM'), ('SHM251_HandWin', 'float', 'SHM'),
                     ('SHM251_HandT', 'float', 'SHM'), ('SHM251_PrevYaw', 'float', 'SHM'), ('SHM251_PrevOn', 'bool', 'SHM')]); compile_ok(bp)
    set_defaults(bp, {'SHM251_StartEntry': 0.0, 'SHM251_YawSlew': 0.0, 'SHM251_YawRate': 150.0, 'SHM251_HandWin': 0.35, 'SHM251_HandT': 10.0}); compile_ok(bp)
    # ---------------- (A) request-frame start database
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
    br84 = N['K2Node_IfThenElse_84']; assert 'IfThenElse' in br84
    old_else = succ(br84, 'else'); assert old_else, 'entry else successor'
    c254 = N['K2Node_CallFunction_254']; assert 'SetDatabaseToSearch' in tid(c254), tid(c254)
    mm = src((c254, 'MotionMatchingNode'))[0]; mode = [str(x.value) for x in info(c254).input_pins if str(x.name) == 'InterruptMode'][0]
    side = (N['K2Node_CallFunction_297'], 'ReturnValue'); assert 'InRange' in tid(side[0]), tid(side[0])
    for tn, tp in old_else: disconnect((tn, tp))
    dbn = g.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': g.get('CurrentSelectedDatabase')})
    has = lambda sub: g.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': dbn, 'Substring': sub, 'bUseCase': False, 'bSearchFromEnd': False})
    notStart = g.NOT(g.OR(g.OR(has('SHM237_JogStart'), has('SHM248_JogStart')), has('SHM237_JogResume')))
    cond = g.AND(g.AND(g.within(g.get('SHM251_StartEntry'), 0.5, 1.0e9), g.within(g.get('GroundSpeed'), -1.0, g.get('SHM249_RestSpeed'))),
                 g.AND(g.AND(g.get('HasAcceleration'), g.within(g.get('SHM_StartGait'), 0.5, 1.5)), notStart))
    bt, bf = g.branch(cond, (br84, 'else'))
    for tn, tp in old_else: connect(bf, (tn, tp))
    sbt, sbf = g.branch(side, bt)
    for br_, var in ((sbt, 'SHM_JogStartDB_L'), (sbf, 'SHM_JogStartDB_R')):
        s = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(br_, (s, 'execute'))
        connect(mm, (s, 'MotionMatchingNode')); connect(g.get(var), (s, 'Database')); arg(s, 'InterruptMode', mode)
    out['entry'] = {'else_was': [a.rsplit('.', 1)[-1] for a, _ in old_else], 'mode': mode}
    # ---------------- (B) continuous yaw hand-over after the servo
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    e1 = [p for p in sn if tid(p).endswith('|SetSHM249_PrevServo')]; assert len(e1) == 1, e1
    nxt = succ(e1[0]); assert nxt, 'PrevServo successor'
    for tn, tp in nxt: disconnect((tn, tp))
    dt = gs.pure('/Script/Engine.GameplayStatics:GetWorldDeltaSeconds', {})
    h1 = gs.set('SHM251_HandT', gs.select(gs.get('SHM249_Servo'), 0.0, gs.math(gs.get('SHM251_HandT'), dt, 1)), (e1[0], 'then'))
    tgt = gs.get('ClipYaw', COMP, ct); on = gs.AND(gs.within(gs.get('SHM251_YawSlew'), 0.5, 1.0e9), gs.get('ClipYawOn', COMP, ct))
    win = gs.AND(gs.AND(gs.NOT(gs.get('SHM249_Servo')), gs.within(gs.get('SHM251_HandT'), -1.0, gs.get('SHM251_HandWin'))), gs.AND(on, gs.get('SHM251_PrevOn')))
    err = gs.pure(M + 'NormalizeAxis', {'Angle': gs.math(tgt, gs.get('SHM251_PrevYaw'), -1)})
    mxdt = gs.mul(dt, gs.get('SHM251_YawRate'))
    step = gs.pure('FClamp', {'Value': err, 'Min': gs.mul(mxdt, -1.0), 'Max': mxdt})
    outy = gs.select(win, gs.math(gs.get('SHM251_PrevYaw'), step, 1), tgt)
    h2 = gs.set('ClipYaw', outy, h1, COMP, ct)
    h3 = gs.set('SHM251_PrevYaw', gs.get('ClipYaw', COMP, ct), h2)
    h4 = gs.set('SHM251_PrevOn', on, h3)
    for tn, tp in nxt: connect(h4, (tn, tp))
    out['yaw'] = {'after': e1[0].rsplit('.', 1)[-1], 'next': [a.rsplit('.', 1)[-1] for a, _ in nxt]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: str(cdo.get_editor_property(k)) for k in ('SHM251_StartEntry', 'SHM251_YawSlew', 'SHM251_YawRate', 'SHM251_HandWin')}
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knobs']['SHM251_StartEntry'] == '0.0' and out['knobs']['SHM251_YawSlew'] == '0.0'
if out['ok'] and getattr(builtins, 'V251_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('ENTRYYAW251 ' + json.dumps(out, default=str))
