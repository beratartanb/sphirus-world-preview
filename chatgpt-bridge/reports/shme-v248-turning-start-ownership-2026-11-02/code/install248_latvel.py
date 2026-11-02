"""install248_latvel.py (editor job, write manifest = BP_SHM_HumanMotionComponent, ABP base + child, BP_GR_Player + BP_PBI_Player):
V2.48 lateral clip-bound velocity (the V2.28 contract extended with the sideways root motion of turning starts).
  component : ClipSpeedLat (float, SHM|V228)
  ABP SHM_Snapshot (right after SetClipSpeedOn): component ClipSpeedLat := SHM228_On ? SHM226_VL / SHM226_W : 0   (0 for every clip without
              the curve: the reversal / start clips keep their pure forward contract)
  BP_GR_Player GR_Impl_CP_PhysicalRedirect, V2.28 branch: Velocity = Forward * ClipSpeed + Right * ClipSpeedLat (Z kept)
Production unchanged until a turning start is bound (SHM248_On). Idempotent (component variable marker). builtins.V248_SAVE saves.
Prints LATVEL248 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, op, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMPP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent'; COMP = COMPP + '.BP_SHM_HumanMotionComponent_C'
PB = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if any(k in p.get_name() for k in ('ABP_GR_MotionMatching', 'BP_GR_Player', 'BP_PBI_Player', 'BP_SHM_HumanMotionComponent'))]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
cb = u.load_asset(COMPP)
if 'ClipSpeedLat' in [str(v) for v in B.list_variables(cb)]: out['patch'] = 'already'
else:
    ensure_vars(cb, [('ClipSpeedLat', 'float', 'SHM|V228')]); st, errs = compile_ok(cb); out['comp'] = [str(st), errs[:4]]
    # ---- ABP snapshot
    bp = u.load_asset(AP); sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    last = [p for p in sn if tid(p).endswith('SetClipSpeedOn')]; assert len(last) == 1, last
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'; ct = (comp[0], 'ReturnValue')
    nxt = [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for o in info(last[0]).output_pins if str(o.name) == 'then' for q in o.connected_pins]
    for tn, tp in nxt: disconnect((tn, tp))
    vL = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM226_VL'}); vW = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM226_W'})
    val = gs.select(gs.get('SHM228_On'), gs.pure(M + 'SafeDivide', {'A': vL, 'B': vW}), 0.0)
    tail = gs.set('ClipSpeedLat', val, (last[0], 'then'), COMP, ct)
    for tn, tp in nxt: connect(tail, (tn, tp))
    out['abp_next'] = [a.rsplit('.', 1)[-1] for a, _ in nxt]
    # ---- pawn velocity write
    g = G(op(PB) + ':GR_Impl_CP_PhysicalRedirect'); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g.path))}
    def leaves(ep, depth, acc):   # variable getters feeding a pin (the V2.28 write is the one fed by ClipSpeed + ActorForwardVector; later
        if depth > 7: return         # rounds added DesiredDir / MaxAcceleration terms to it, so the wiring, not the node id, identifies it)
        for n_, _ in src(ep):
            t_ = tid(n_).rsplit('|', 1)[-1]
            if t_.startswith('Get'): acc.add(t_)
            for q_ in info(n_).input_pins:
                if q_.name not in ('self', 'execute'): leaves((n_, q_.name), depth + 1, acc)
    def v228_set(p):
        if not tid(p).endswith('SetVelocity'): return False
        acc = set(); leaves((p, 'Velocity'), 0, acc); return 'GetClipSpeed' in acc and 'GetActorForwardVector' in acc
    sets = [p for p in N.values() if v228_set(p)]
    assert len(sets) == 1, ('V2.28 Velocity set nodes', [p.rsplit('.', 1)[-1] for p in sets])
    mk = src((sets[0], 'Velocity')); assert len(mk) == 1, mk; mk = mk[0][0]; assert 'MakeVector' in tid(mk), tid(mk)
    xs = src((mk, 'X')); ys = src((mk, 'Y')); assert len(xs) == 1 and len(ys) == 1, (xs, ys)
    disconnect((mk, 'X')); disconnect((mk, 'Y'))
    compn = g.pure('/Script/Engine.Actor:GetComponentByClass', {'ComponentClass': COMP})
    lat = g.get('ClipSpeedLat', COMP, compn)
    rt = g.pure('/Script/Engine.Actor:GetActorRightVector'); br = g.fn('BreakVector', {'InVec': rt})
    connect(g.math(xs[0], g.mul((br, 'X'), lat)), (mk, 'X')); connect(g.math(ys[0], g.mul((br, 'Y'), lat)), (mk, 'Y'))
    out['pawn'] = {'set': sets[0].rsplit('.', 1)[-1], 'x_old': xs[0][0].rsplit('.', 1)[-1]}
    for name, a in (('abp', bp), ('abp_child', u.load_asset(CPA)), ('pawn', u.load_asset(PB)), ('pawn_child', u.load_asset(CHILD))):
        st, errs = compile_ok(a); out[name] = [str(st), errs[:4]]
    out['ok'] = all('UP_TO_DATE' in out[k][0] and not out[k][1] for k in ('comp', 'abp', 'abp_child', 'pawn', 'pawn_child'))
    if out['ok'] and getattr(builtins, 'V248_SAVE', False): save(cb, bp, u.load_asset(CPA), u.load_asset(PB), u.load_asset(CHILD)); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('LATVEL248 ' + json.dumps(out, default=str))
