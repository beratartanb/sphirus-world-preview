"""install_v231_inspect.py (editor job) - V2.31 inspection resolver on BP_SHM_HumanMotionComponent (see apply_insp231.py).
1. component variables SHM231_InsHit (PrimitiveComponent ref), SHM231_InsTag (bool), SHM231_InsFocus (vector), SHM231_InsId / SHM231_InsPrevId
2. function SHM231_InspectResolve (exec graph, NOT the DSL - it needs branches): IsValid(InsHit) -> owner -> IsValid(owner) ->
   ComponentHasTag(InsHit, GR_Inspect) OR ActorHasTag(owner, GR_Inspect) -> InsTag true, InsId = GetPathName(owner),
   InsFocus = GetComponentBounds(owner root component).Origin; every other path: InsTag false. No member call can see None.
3. SHM_Tick: the call is inserted right after the SHM_UpdateCameraV21 call (Tools/SHME_V1_20260925/build_tick.py does the same on rebuilds).
Idempotent. builtins.V231_SAVE saves the component. Prints INSPECT231 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
CP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent'; CLS = CP + '.BP_SHM_HumanMotionComponent_C'
bp = u.load_asset(CP); out = {}
ensure_vars(bp, [('SHM231_InsHit', u.PrimitiveComponent.static_class(), 'SHM|V231'), ('SHM231_InsTag', 'bool', 'SHM|V231'), ('SHM231_InsFocus', 'Vector', 'SHM|V231'),
                 ('SHM231_InsId', 'string', 'SHM|V231'), ('SHM231_InsPrevId', 'string', 'SHM|V231')])
compile_ok(bp)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
fn = graph(bp, 'SHM231_InspectResolve')
if fn is None:
    fn = B.add_function_graph(bp, 'SHM231_InspectResolve')
    g = G(pn(fn)); tail = g.entry()
    hit = g.get('SHM231_InsHit')
    y1, n1 = g.branch(g.pure('/Script/Engine.KismetSystemLibrary:IsValid', {'Object': hit}), tail)
    own = g.pure('/Script/Engine.ActorComponent:GetOwner', {'self': hit})
    y2, n2 = g.branch(g.pure('/Script/Engine.KismetSystemLibrary:IsValid', {'Object': own}), y1)
    tagged = g.OR(g.pure('/Script/Engine.ActorComponent:ComponentHasTag', {'self': hit, 'Tag': 'GR_Inspect'}), g.pure('/Script/Engine.Actor:ActorHasTag', {'self': own, 'Tag': 'GR_Inspect'}))
    y3, n3 = g.branch(tagged, y2)
    root = g.pure('/Script/Engine.Actor:K2_GetRootComponent', {'self': own})
    org = g.pure('/Script/Engine.KismetSystemLibrary:GetComponentBounds', {'Component': root}, 'Origin')
    t = g.set('SHM231_InsFocus', org, y3)
    t = g.set('SHM231_InsId', g.pure('/Script/Engine.KismetSystemLibrary:GetPathName', {'Object': own}), t)
    t = g.set('SHM231_InsTag', True, t)
    f1 = g.set('SHM231_InsTag', False, n1); f2 = g.set('SHM231_InsTag', False, n2); f3 = g.set('SHM231_InsTag', False, n3)
    out['fn'] = 'built'
else: out['fn'] = 'already'
st, errs = compile_ok(bp); out['fn_status'] = str(st); out['fn_errs'] = errs[:6]
tick = graph(bp, 'SHM_Tick'); tg = G(pn(tick)); tn = [pn(n) for n in B.find_nodes(tick)]
have = [p for p in tn if tid(p).split('|')[-1] == 'SHM231_InspectResolve' or p.rsplit('.', 1)[-1].startswith('K2Node_CallFunction') and 'SHM231_InspectResolve' in tid(p)]
if have: out['tick'] = 'already'
else:
    cam = [p for p in tn if tid(p).split('|')[-1] == 'SHM_UpdateCameraV21' or ('SHM_UpdateCameraV21' in tid(p) and 'CallFunction' in p)]
    assert len(cam) == 1, ('camera call in SHM_Tick', cam, [tid(p)[-40:] for p in tn][:80])
    nxt = [p for p in tn if any(q.name == 'execute' for q in info(p).input_pins) and (cam[0], 'then') in src((p, 'execute'))]
    assert len(nxt) == 1, ('successor of the camera call', nxt)
    out['tick_next_before'] = tid(nxt[0])[-50:]
    others = [x for x in src((nxt[0], 'execute')) if x != (cam[0], 'then')]   # keep every other exec source (the CameraPhysicalSignals ELSE path)
    disconnect((nxt[0], 'execute'))
    n = tg.record(tg.editor().add_call_function_node(CLS + ':SHM231_InspectResolve'))
    connect((cam[0], 'then'), (n, 'execute')); connect((n, 'then'), (nxt[0], 'execute'))
    for x in others: connect(x, (nxt[0], 'execute'))
    out['tick'] = {'after': cam[0].rsplit('.', 1)[-1], 'call': n.rsplit('.', 1)[-1], 'next': nxt[0].rsplit('.', 1)[-1],
                   'next_exec_in': [(a.rsplit('.', 1)[-1], b) for a, b in src((nxt[0], 'execute'))]}
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
ok = 'UP_TO_DATE' in str(st) and not errs
out['ok'] = ok
if ok and getattr(builtins, 'V231_SAVE', False): save(bp); out['saved'] = True
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('INSPECT231 ' + json.dumps(out, default=str))
