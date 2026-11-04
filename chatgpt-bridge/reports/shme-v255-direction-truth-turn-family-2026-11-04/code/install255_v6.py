"""install255_v6.py (editor job, write manifest = ABP base + child): V2.55 (1) plan end as a stored one-frame event, (2) walking tier of the turn route (knob SHM255_Ctl).
(1) install255_v5 re-evaluated its pure 'fire' after InPlan had been written, so Ended read (Own low AND Phase high AND NOT InPlan): true on a blend-in from another plan's tail when the entry did not come through RouteOn.
    Now SHM255_Fire is STORED before InPlan is written and Ended latches only on it.
(2) want used SHM255_RouteMinV for the reversal too; a reversal now uses SHM255_RevMinV (walking counts), the cut keeps RouteMinV. Below SHM255_WalkV the reversal searches SHM255_DB_WalkR / L.
Idempotent (variable SHM255_Fire). builtins.V255_SAVE saves. Prints V6255 {...}."""
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
assert 'SHM255_InPlan' in V, 'install255_v5 first'
if 'SHM255_Fire' in V: out['patch'] = 'already'
else:
    PSD = u.PoseSearchDatabase.static_class()
    ensure_vars(bp, [('SHM255_Fire', 'bool', 'SHM'), ('SHM255_RevMinV', 'float', 'SHM'), ('SHM255_WalkV', 'float', 'SHM'), ('SHM255_DB_WalkR', PSD, 'SHM'), ('SHM255_DB_WalkL', PSD, 'SHM')]); compile_ok(bp)
    set_defaults(bp, {'SHM255_RevMinV': 190.0, 'SHM255_WalkV': 190.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    def curve(n): return gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': n})
    # ---- (1) stored fire
    ip = [p for p in sn if tid(p).endswith('|SetSHM255_InPlan')]; assert len(ip) == 1, ip; ip = ip[0]
    en = [p for p in sn if tid(p).endswith('|SetSHM255_Ended')]; assert len(en) == 1, en; en = en[0]
    pre = src((ip, 'execute')); assert len(pre) == 1, pre
    disconnect((ip, 'execute'))
    own = curve('SHM254_Own'); ph = curve('SHM255_Phase')
    tf = gs.set('SHM255_Fire', gs.AND(gs.get('SHM255_InPlan'), gs.AND(gs.within(own, -1.0e9, 0.3), gs.within(ph, 1.5, 1.0e9))), pre[0]); connect(tf, (ip, 'execute'))
    disconnect((ip, 'SHM255_InPlan'))
    own2 = curve('SHM254_Own')
    connect(gs.OR(gs.within(own2, 0.7, 1.0e9), gs.AND(gs.AND(gs.get('SHM255_InPlan'), gs.NOT(gs.get('SHM255_Fire'))), gs.within(own2, 0.02, 1.0e9))), (ip, 'SHM255_InPlan'))
    dbn = gs.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': gs.get('CurrentSelectedDatabase')})
    mine = gs.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': dbn, 'Substring': 'SHM254', 'bUseCase': False, 'bSearchFromEnd': False})
    disconnect((en, 'SHM255_Ended'))
    connect(gs.AND(gs.AND(gs.OR(gs.get('SHM255_Ended'), gs.get('SHM255_Fire')), gs.NOT(gs.get('SHM255_RouteOn'))), mine), (en, 'SHM255_Ended'))
    # ---- (2) reversal speed gate + walking tier
    ro = [p for p in sn if tid(p).endswith('|SetSHM255_RouteOn')]
    first = [p for p in ro if src((p, 'SHM255_RouteOn'))]; assert len(first) == 1, ro; first = first[0]
    hit = []
    def walk(p, d, seen):
        if d > 12 or p in seen: return
        seen.add(p)
        for q in info(p).input_pins:
            if q.name in ('execute', 'then'): continue
            for s_ in src((p, q.name)):
                if tid(s_[0]).endswith('|GetSHM255_RouteMinV'): hit.append((p, q.name))
                walk(s_[0], d + 1, seen)
    walk(first, 0, set()); assert len(hit) == 1, hit
    disconnect(hit[0]); connect(gs.get('SHM255_RevMinV'), hit[0])
    th = [x[0] for x in succ(first) if tid(x[0]).endswith('|SetSHM227_Thr')]; assert len(th) == 1, succ(first); th = th[0]
    nx = succ(th); assert len(nx) == 1, nx; disconnect(nx[0])
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; ct = (comp[0], 'ReturnValue')
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner'); vel = gs.pure('/Script/Engine.Actor:GetVelocity', {'self': pawn})
    spd = gs.pure(M + 'VSize', {'A': vel}); yv = gs.yaw(gs.pure(M + 'Conv_VectorToRotator', {'InVec': vel}))
    ydv = gs.yaw(gs.pure(M + 'Conv_VectorToRotator', {'InVec': gs.get('DesiredVelocity', COMP, ct)}))
    ra = gs.pure(M + 'NormalizeAxis', {'Angle': gs.sub(ydv, yv)}); ara = gs.pure(M + 'Abs', {'A': ra})
    sideReq = gs.within(ara, 20.0, 150.0)
    right = gs.OR(gs.AND(sideReq, gs.within(ra, 0.0, 1.0e9)), gs.AND(gs.NOT(sideReq), gs.within(gs.get('SupportSide', COMP, ct), 0.5, 1.0e9)))
    y, n = gs.branch(gs.AND(gs.get('SHM255_RouteOn'), gs.within(spd, -1.0, gs.get('SHM255_WalkV'))), (th, 'then'))
    wR, wL = gs.branch(right, y)
    a1 = gs.set('SHM255_RouteDB', gs.get('SHM255_DB_WalkR'), wR); a2 = gs.set('SHM255_RouteDB', gs.get('SHM255_DB_WalkL'), wL)
    for t_ in (n, a1, a2): connect(t_, nx[0])
    out['wired'] = {'minv': hit[0][0].rsplit('.', 1)[-1], 'thr': th.rsplit('.', 1)[-1]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM255_Ctl'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V255_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('V6255 ' + json.dumps(out, default=str))
