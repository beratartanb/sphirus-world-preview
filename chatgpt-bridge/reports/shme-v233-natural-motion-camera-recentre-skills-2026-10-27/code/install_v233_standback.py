"""install_v233_standback.py (editor job, write manifest: ABP base + child) - V2.33 chain 1 route: the stand-back start database is
searched ONLY by a truly stopped body asking to go backward.
  SHM_Snapshot (game thread): SHM233_StandBack = knob SHM233_StandBackOn > 0.5 AND component HasIntent AND backward intent
    (dot(Facing, DesiredDir) < -0.7) AND [ truly stopped: component Speed < 15 cm/s AND ContactL AND ContactR AND BrakingDemand < 0.05
    OR the latch already set (held while the backward intent holds; any other request / release clears it) ].
  Update_MotionMatching: in front of the two jog start-transfer searches (SetDatabaseToSearch SHM_JogStartDB_L / _R) a branch on
    SHM233_StandBack searches SHM233_DB_StandBack (V233/PSD_SHM233_StandBackStart) on the same Motion Matching node / interrupt mode.
Knob default 0 = production unchanged. Idempotent (SHM233_StandBack setter present). V2.31 exec rule: new Set node inserted after the
existing SetSHM228_On (its old successors re-linked). builtins.V233_SAVE saves. Prints SBK233 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
DB = '/Game/GraceRanger/SHME/Animations/V233/PSD_SHM233_StandBackStart'
bp = u.load_asset(AP); out = {}
PSD = u.PoseSearchDatabase.static_class()
ensure_vars(bp, [('SHM233_StandBackOn', 'float', 'SHM233'), ('SHM233_StandBack', 'bool', 'SHM233'), ('SHM233_DB_StandBack', PSD, 'SHM233'), ('SHM233_SBT', 'float', 'SHM233')]); compile_ok(bp)
set_defaults(bp, {'SHM233_DB_StandBack': u.load_asset(DB), 'SHM233_StandBackOn': 0.0})
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
# ---- snapshot term (v2: no BrakingDemand term - a new request from a stand already reads 0.15-0.17 there; latch limited to the start)
#   SHM233_StandBack = want AND (stopped OR (latch AND SHM233_SBT < 1.2 s)); SHM233_SBT = time since the latch was set (0 when off)
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'
ct = (comp[0], 'ReturnValue')
back = gs.within(gs.pure(M + 'Dot_VectorVector', {'A': gs.get('Facing', COMP, ct), 'B': gs.get('DesiredDir', COMP, ct)}), -1.0e9, -0.95)   # straight backward only (+-18 deg): diagonal back starts keep their own clips (C1B jstart)
# intent: the component's (one frame late: it ticks post-physics) OR the ABP's own current-frame CMC acceleration (AAMS Acceleration /
# HasAcceleration, updated before this snapshot) pointing backward - the first intent frame is covered
backA = gs.within(gs.pure(M + 'Dot_VectorVector', {'A': gs.get('Facing', COMP, ct), 'B': gs.pure(M + 'Normal', {'A': gs.get('Acceleration')})}), -1.0e9, -0.95)
# jog gait only (the clip is a jog backward start; walk / sprint keep their own starts): SHM_StartGait 0 walk, 1 jog, 2 sprint
want = gs.AND(gs.AND(gs.within(gs.get('SHM233_StandBackOn'), 0.5, 1.0e9), gs.within(gs.get('SHM_StartGait'), 0.5, 1.5)), gs.OR(gs.AND(gs.get('HasIntent', COMP, ct), back), gs.AND(gs.get('HasAcceleration'), backA)))
# truly stopped = low speed, both feet in contact AND the pose really is the idle pose (Motion Matching is in an idle database) - a body
# still finishing its stop (stop clip) or re-pressing during a brake never takes the stand-back start (V2.33 C1B: j30_rel_3200)
idlep = gs.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': gs.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': gs.get('CurrentSelectedDatabase')}), 'Substring': 'Idle'})
stopped = gs.AND(gs.AND(gs.within(gs.get('Speed', COMP, ct), -1.0, 15.0), idlep), gs.AND(gs.get('ContactL', COMP, ct), gs.get('ContactR', COMP, ct)))
held = gs.AND(gs.get('SHM233_StandBack'), gs.within(gs.get('SHM233_SBT'), -1.0, 1.2))
val = gs.AND(want, gs.OR(stopped, held))
dtp = gs.pure('/Script/Engine.GameplayStatics:GetWorldDeltaSeconds', {})
setn = [p for p in sn if tid(p).endswith('|SetSHM233_StandBack')]
if setn:
    disconnect((setn[0], 'SHM233_StandBack')); connect(val, (setn[0], 'SHM233_StandBack')); s_ = (setn[0], 'then'); out['snapshot'] = 'rewired'
else:
    son = [p for p in sn if tid(p).endswith('SetSHM228_On')]; assert len(son) == 1, son
    nxt = [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0])
           for o in info(son[0]).output_pins if str(o.name) == 'then' for q in o.connected_pins]
    for tn, tp in nxt: disconnect((tn, tp))
    s_ = gs.set('SHM233_StandBack', val, (son[0], 'then'))
    for tn, tp in nxt: connect(s_, (tn, tp))
    out['snapshot'] = 'wired'
# the timer: set right after SHM233_StandBack (value = select(StandBack, SBT + dt, 0))
tset = [p for p in sn if tid(p).endswith('|SetSHM233_SBT')]
tval = gs.select(gs.get('SHM233_StandBack'), gs.math(gs.get('SHM233_SBT'), dtp), 0.0)
if tset: disconnect((tset[0], 'SHM233_SBT')); connect(tval, (tset[0], 'SHM233_SBT')); out['timer'] = 'rewired'
else:
    sb = s_[0]
    nxt = [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0])
           for o in info(sb).output_pins if str(o.name) == 'then' for q in o.connected_pins]
    for tn, tp in nxt: disconnect((tn, tp))
    t_ = gs.set('SHM233_SBT', tval, (sb, 'then'))
    for tn, tp in nxt: connect(t_, (tn, tp))
    out['timer'] = 'wired'
# ---- route in Update_MotionMatching
gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = [pn(n) for n in B.find_nodes(obj(gp))]
def db_var_of(p):
    s_ = src((p, 'Database'))
    return tid(s_[0][0]).rsplit('|', 1)[-1] if s_ else ''
if any(db_var_of(p) == 'GetSHM233_DB_StandBack' for p in nodes if 'SetDatabaseToSearch' in tid(p)): out['route'] = 'already'
else:
    done = []
    for side in ('L', 'R'):
        calls = [p for p in nodes if 'SetDatabaseToSearch' in tid(p) and db_var_of(p) == 'GetSHM_JogStartDB_' + side]; assert len(calls) == 1, (side, calls)
        call = calls[0]; pred = src((call, 'execute')); assert len(pred) == 1, pred
        mm = src((call, 'MotionMatchingNode'))[0]; mode = [str(x.value) for x in info(call).input_pins if str(x.name) == 'InterruptMode'][0]
        nxt = [pn(q.node) for q in [x for x in info(call).output_pins if str(x.name) == 'then'][0].connected_pins]
        disconnect((call, 'execute'))
        bt, bf = g.branch(g.get('SHM233_StandBack'), pred[0])
        connect(bf, (call, 'execute'))
        s = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(bt, (s, 'execute'))
        connect(mm, (s, 'MotionMatchingNode')); connect(g.get('SHM233_DB_StandBack'), (s, 'Database')); arg(s, 'InterruptMode', mode)
        for n in nxt: connect((s, 'then'), (n, 'execute'))
        done.append([side, call.rsplit('.', 1)[-1], mode, [n.rsplit('.', 1)[-1] for n in nxt]])
    out['route'] = done
# ---- v2 entry override (knob >= 1.5): at the ENTRY of Update_MotionMatching, while SHM233_StandBack holds, ONLY the stand-back DB is
#   searched (the rest of the function is skipped for that frame) - this also covers the first intent frame, where the family is still 0
#   and the default chooser would pick the vendor dense start for one frame (tick-order lag). Knob 1 = the family-4 branch only.
ent = g.entry(); en = ent[0]
cur = [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0])
       for o in info(en).output_pins if str(o.name) == 'then' for q in o.connected_pins]
if any(tid(a).endswith('IfThenElse') or 'Branch' in tid(a) for a, _ in cur) and any(db_var_of(p) == 'GetSHM233_DB_StandBack' and p not in [] for p in nodes if 'SetDatabaseToSearch' in tid(p) and not src((p, 'execute')) == []) and out.get('route') == 'already' and getattr(builtins, 'V233_ENTRY_DONE', False):
    out['entry'] = 'already'
else:
    have = [p for p in nodes if tid(p).endswith('|GetSHM233_StandBackOn') and any(tid(a).endswith('InRange_FloatFloat') for a in [pn(q.node) for o in info(p).output_pins for q in o.connected_pins])]
    calls = [p for p in nodes if 'SetDatabaseToSearch' in tid(p) and db_var_of(p) == 'GetSHM_JogStartDB_L']
    mm = src((calls[0], 'MotionMatchingNode'))[0] if calls else None
    marker = [p for p in nodes if tid(p).endswith('|GetSHM233_SBT')]
    if marker: out['entry'] = 'already (SBT marker)'
    else:
        assert mm, 'MM node source'
        for tn, tp in cur: disconnect((tn, tp))
        cond = g.AND(g.get('SHM233_StandBack'), g.AND(g.within(g.get('SHM233_StandBackOn'), 1.5, 1.0e9), g.within(g.get('SHM233_SBT'), -1.0, 1.0e9)))
        bt, bf = g.branch(cond, ent)
        for tn, tp in cur: connect(bf, (tn, tp))
        s2 = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(bt, (s2, 'execute'))
        connect(mm, (s2, 'MotionMatchingNode')); connect(g.get('SHM233_DB_StandBack'), (s2, 'Database')); arg(s2, 'InterruptMode', 'InterruptOnDatabaseChangeAndInvalidateContinuingPose')
        out['entry'] = {'wired': True, 'old_first': [a.rsplit('.', 1)[-1] for a, _ in cur]}
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = float(cdo.get_editor_property('SHM233_StandBackOn'))
out['db_default'] = str(cdo.get_editor_property('SHM233_DB_StandBack'))[:90]
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and out['knob'] == 0.0; out['ok'] = ok
if ok and getattr(builtins, 'V233_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('SBK233 ' + json.dumps(out, default=str))
