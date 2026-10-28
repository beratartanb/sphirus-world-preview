"""install_v234_revkeep.py (editor job, write manifest: ABP base + child) - V2.34 release-repress (sphirus-natural-motion): a reversal whose
input is released for a moment and pressed again must CONTINUE as the reversal. Owner trace (v234b4_j30_rel_3200): the ABP family stays 3
through the gap, but Update_MotionMatching's default chooser (CHT_PBI_PlayerDense) searches the dense stand STOP database as soon as the
acceleration is gone and the dense stand START database at the re-press (speed ~0) - a stand start from a mid-reversal pose = 34-51 cm drag.
  SHM_Snapshot: SHM234_RevDB = the last selected reversal database (name contains RevFwd / RevBwd), SHM234_RevDBT = s since it was selected.
  Update_MotionMatching ENTRY, after the V2.33 stand-back branch's false exit: knob SHM234_RevKeepOn >= 0.5 AND SHM_Family == 3 AND
    SHM234_RevDBT < 0.6 AND (NOT HasAcceleration OR Speed2D < 60) -> search ONLY SHM234_RevDB this frame
    (InterruptOnDatabaseChange: the continuing reversal pose stays a candidate); otherwise the original flow (every other state unchanged).
Knob default 0 = production unchanged. Idempotent (SHM234_RevDBT setter present). builtins.V234_SAVE saves. Prints REVKEEP234 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
bp = u.load_asset(AP); out = {}
PSD = u.PoseSearchDatabase.static_class()
ensure_vars(bp, [('SHM234_RevKeepOn', 'float', 'SHM234'), ('SHM234_RevDB', PSD, 'SHM234'), ('SHM234_RevDBT', 'float', 'SHM234')]); compile_ok(bp)
set_defaults(bp, {'SHM234_RevKeepOn': 0.0, 'SHM234_RevDBT': 10.0})
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def succ(node):
    return [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0])
            for o in info(node).output_pins if str(o.name) == 'then' for q in o.connected_pins]
# ---- snapshot memory, after SetSHM233_SBT
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any(tid(p).endswith('|SetSHM234_RevDBT') for p in sn): out['snapshot'] = 'already'
else:
    anchor = [p for p in sn if tid(p).endswith('|SetSHM233_SBT')]; assert len(anchor) == 1, anchor; anchor = anchor[0]
    nxt = succ(anchor)
    for tn, tp in nxt: disconnect((tn, tp))
    nm = gs.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': gs.get('CurrentSelectedDatabase')})
    isrev = gs.OR(gs.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': nm, 'Substring': 'RevFwd'}),
                  gs.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': nm, 'Substring': 'RevBwd'}))
    bt, bf = gs.branch(isrev, (anchor, 'then'))
    s1 = gs.set('SHM234_RevDB', gs.get('CurrentSelectedDatabase'), bt)
    s2 = gs.set('SHM234_RevDBT', 0.0, s1)
    dtp = gs.pure('/Script/Engine.GameplayStatics:GetWorldDeltaSeconds', {})
    s3 = gs.set('SHM234_RevDBT', gs.math(gs.get('SHM234_RevDBT'), dtp), bf)
    for tn, tp in nxt: connect(s2, (tn, tp)); connect(s3, (tn, tp))
    out['snapshot'] = {'after': 'SetSHM233_SBT', 'next': [a.rsplit('.', 1)[-1] for a, _ in nxt]}
# ---- entry override after the stand-back branch (false exit)
gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = [pn(n) for n in B.find_nodes(obj(gp))]
if any(tid(p).endswith('|GetSHM234_RevDB') for p in nodes): out['entry'] = 'already'
else:
    ent = g.entry(); en = ent[0]
    first = succ(en); assert len(first) == 1 and ('IfThenElse' in first[0][0] or 'Dal' in tid(first[0][0])), first
    sbb = first[0][0]   # the V2.33 stand-back branch
    fo = [o for o in info(sbb).output_pins if str(o.name) == 'else'][0]
    cur = [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for q in fo.connected_pins]
    for tn, tp in cur: disconnect((tn, tp))
    calls = [p for p in nodes if 'SetDatabaseToSearch' in tid(p) and src((p, 'MotionMatchingNode'))]
    mm = src((calls[0], 'MotionMatchingNode'))[0]
    slow = g.OR(g.NOT(g.get('HasAcceleration')), g.within(g.get('Speed2D'), -1.0, 60.0))
    cond = g.AND(g.AND(g.within(g.get('SHM234_RevKeepOn'), 0.5, 1.0e9), g.within(g.get('SHM_Family'), 2.5, 3.5)),
                 g.AND(g.within(g.get('SHM234_RevDBT'), -1.0, 0.6), slow))   # no IsValid: not thread-safe in this thread-safe function; RevDB is written whenever RevDBT is reset (default RevDBT 10)
    bt, bf = g.branch(cond, (sbb, 'else'))
    for tn, tp in cur: connect(bf, (tn, tp))
    s = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(bt, (s, 'execute'))
    connect(mm, (s, 'MotionMatchingNode')); connect(g.get('SHM234_RevDB'), (s, 'Database')); arg(s, 'InterruptMode', 'InterruptOnDatabaseChange')
    out['entry'] = {'after_branch': sbb.rsplit('.', 1)[-1], 'old_else': [a.rsplit('.', 1)[-1] for a, _ in cur]}
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = float(cdo.get_editor_property('SHM234_RevKeepOn'))
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and out['knob'] == 0.0; out['ok'] = ok
if ok and getattr(builtins, 'V234_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('REVKEEP234 ' + json.dumps(out, default=str))
