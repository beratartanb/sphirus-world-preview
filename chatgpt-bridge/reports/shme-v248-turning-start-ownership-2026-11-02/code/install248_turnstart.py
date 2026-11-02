"""install248_turnstart.py (editor job, write manifest = ABP base + child; after build248_turnstartdb.py): V2.48 real-time wrong-backward-start
fix = LOOK-AWARE START-DATABASE OWNERSHIP, decided on the game thread from the pawn's real control rotation.
  SHM_Snapshot (game thread; inserted right after SetSHM228_On, i.e. before the V2.33 stand-back term):
    pawn = TryGetPawnOwner; if IsValid(pawn): SHM248_LookYaw := BreakRotator(pawn.GetControlRotation).Yaw      (the real look yaw - the
          V2.46 PreviousDesiredControllerYaw copy is NOT the control yaw)
    dir = Normal(Acceleration) (movement input direction, current frame); lookFwd = ForwardVector(Rotator(0, LookYaw, 0))
    bodyBack = Dot(Facing(component), dir) < SHM248_BackCos (-0.42 = beyond 115 deg behind the body; the LS lateral route owns 65-115)
    lookBack = Dot(lookFwd, dir) < SHM248_LookBackCos (-0.7 = the player really asks to back-pedal, more than 135 deg from the look)
    SHM248_TurnStart := SHM248_On > 0.5 AND jog gait (SHM_StartGait 0.5-1.5) AND HasAcceleration AND
                        ( (bodyBack AND NOT lookBack) OR (SHM248_TurnStart held AND SHM248_TT < SHM248_HoldT 1.0 s) );  SHM248_TT timer
    SHM233_StandBack (existing set node) := old AND (SHM248_On < 0.5 OR lookBack)   - the stand-back backward start only for a real back request
  Update_MotionMatching: in front of each SetDatabaseToSearch(SHM_JogStartDB_L / _R) (V2.33 pattern) a branch on SHM248_TurnStart searches
    SHM248_DB_TurnStart_<side> (= PSD_SHM248_JogStartT_<side>, the start database WITHOUT backward starts) on the same node / interrupt mode.
Knob SHM248_On default 0 = production unchanged. Idempotent (variable marker). builtins.V248_SAVE saves. Prints TURNSTART248 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
V = '/Game/GraceRanger/SHME/Animations/V248/'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); PSD = u.PoseSearchDatabase.static_class()
if 'SHM248_On' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    dbl = u.load_asset(V + 'PSD_SHM248_JogStartT_L'); dbr = u.load_asset(V + 'PSD_SHM248_JogStartT_R'); assert dbl and dbr, 'build248_turnstartdb.py first'
    ensure_vars(bp, [('SHM248_On', 'float', 'SHM'), ('SHM248_TurnStart', 'bool', 'SHM'), ('SHM248_TT', 'float', 'SHM'), ('SHM248_LookYaw', 'float', 'SHM'),
                     ('SHM248_BackCos', 'float', 'SHM'), ('SHM248_LookBackCos', 'float', 'SHM'), ('SHM248_HoldT', 'float', 'SHM'),
                     ('SHM248_DB_TurnStart_L', PSD, 'SHM'), ('SHM248_DB_TurnStart_R', PSD, 'SHM')]); compile_ok(bp)
    set_defaults(bp, {'SHM248_On': 0.0, 'SHM248_BackCos': -0.42, 'SHM248_LookBackCos': -0.7, 'SHM248_HoldT': 1.0, 'SHM248_DB_TurnStart_L': dbl, 'SHM248_DB_TurnStart_R': dbr}); compile_ok(bp)
    # ---- snapshot (game thread)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'; ct = (comp[0], 'ReturnValue')
    anchor = [p for p in sn if tid(p).endswith('SetSHM228_On')]; assert len(anchor) == 1, anchor; anchor = anchor[0]
    nxt = [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for o in info(anchor).output_pins if str(o.name) == 'then' for q in o.connected_pins]
    assert nxt, 'anchor has no successor'; out['anchor_next'] = [a.rsplit('.', 1)[-1] for a, _ in nxt]
    for tn, tp in nxt: disconnect((tn, tp))
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner', {})
    valid = gs.pure('/Script/Engine.KismetSystemLibrary:IsValid', {'Object': pawn})
    bt, bf = gs.branch(valid, (anchor, 'then'))
    crot = gs.pure('/Script/Engine.Pawn:GetControlRotation', {'self': pawn})
    s1 = gs.set('SHM248_LookYaw', gs.yaw(crot), bt)
    dirA = gs.pure(M + 'Normal', {'A': gs.get('Acceleration')})
    lookFwd = gs.pure(M + 'GetForwardVector', {'InRot': gs.rot(gs.get('SHM248_LookYaw'))})
    bodyBack = gs.within(gs.pure(M + 'Dot_VectorVector', {'A': gs.get('Facing', COMP, ct), 'B': dirA}), -1.0e9, gs.get('SHM248_BackCos'))
    lookBack = gs.within(gs.pure(M + 'Dot_VectorVector', {'A': lookFwd, 'B': dirA}), -1.0e9, gs.get('SHM248_LookBackCos'))
    on = gs.within(gs.get('SHM248_On'), 0.5, 1.0e9); jog = gs.within(gs.get('SHM_StartGait'), 0.5, 1.5)
    fresh = gs.AND(bodyBack, gs.NOT(lookBack)); held = gs.AND(gs.get('SHM248_TurnStart'), gs.within(gs.get('SHM248_TT'), -1.0, gs.get('SHM248_HoldT')))
    val = gs.AND(gs.AND(on, jog), gs.AND(gs.get('HasAcceleration'), gs.OR(fresh, held)))
    s2 = gs.set('SHM248_TurnStart', val, s1); connect(bf, (s2[0], 'execute'))
    dtp = gs.pure('/Script/Engine.GameplayStatics:GetWorldDeltaSeconds', {})
    s3 = gs.set('SHM248_TT', gs.select(gs.get('SHM248_TurnStart'), gs.math(gs.get('SHM248_TT'), dtp), 0.0), s2)
    for tn, tp in nxt: connect(s3, (tn, tp))
    # stand-back gate
    sb = [p for p in sn if tid(p).endswith('|SetSHM233_StandBack')]; assert len(sb) == 1, sb
    old = src((sb[0], 'SHM233_StandBack')); assert len(old) == 1, old
    disconnect((sb[0], 'SHM233_StandBack'))
    connect(gs.AND(old[0], gs.OR(gs.NOT(on), lookBack)), (sb[0], 'SHM233_StandBack')); out['standback_gated'] = True
    # ---- route in Update_MotionMatching
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = [pn(n) for n in B.find_nodes(obj(gp))]
    def db_var_of(p):
        s_ = src((p, 'Database')); return tid(s_[0][0]).rsplit('|', 1)[-1] if s_ else ''
    done = []
    for side in ('L', 'R'):
        calls = [p for p in nodes if 'SetDatabaseToSearch' in tid(p) and db_var_of(p) == 'GetSHM_JogStartDB_' + side]; assert len(calls) == 1, (side, calls)
        call = calls[0]; preds = src((call, 'execute')); assert preds, (side, 'no predecessor')
        mm = src((call, 'MotionMatchingNode'))[0]; mode = [str(x.value) for x in info(call).input_pins if str(x.name) == 'InterruptMode'][0]
        nxt2 = [pn(q.node) for q in [x for x in info(call).output_pins if str(x.name) == 'then'][0].connected_pins]
        disconnect((call, 'execute'))
        bt2, bf2 = g.branch(g.get('SHM248_TurnStart'), preds[0])
        for p_ in preds[1:]: connect(p_, (bt2[0], 'execute'))
        connect(bf2, (call, 'execute'))
        s = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(bt2, (s, 'execute'))
        connect(mm, (s, 'MotionMatchingNode')); connect(g.get('SHM248_DB_TurnStart_' + side), (s, 'Database')); arg(s, 'InterruptMode', mode)
        for n in nxt2: connect((s, 'then'), (n, 'execute'))
        done.append([side, call.rsplit('.', 1)[-1], mode, len(preds), [n.rsplit('.', 1)[-1] for n in nxt2]])
    out['route'] = done
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class())
out['defaults'] = {k: str(cdo.get_editor_property(k)).split('/')[-1][:40] for k in ('SHM248_On', 'SHM248_BackCos', 'SHM248_LookBackCos', 'SHM248_HoldT', 'SHM248_DB_TurnStart_L', 'SHM248_DB_TurnStart_R')}
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['defaults']['SHM248_On'] == '0.0'
if out['ok'] and getattr(builtins, 'V248_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('TURNSTART248 ' + json.dumps(out, default=str))
