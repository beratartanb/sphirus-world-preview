"""install255_cut.py (editor job, write manifest = ABP base + child): V2.55 hard 90 deg change on the same single route (knob SHM255_Ctl).
A 60..RevMin request while moving >= RouteMinV along the body takes the capture-built cut of its gait and side (SHM255_DB_CutR / CutL / JogCutR / JogCutL) instead of the V2.54 / V2.38 synthesised cuts.
Spliced after SetSHM227_Thr of install255_route: Branch(cut) -> RouteDB by speed and side -> RouteOn := true -> Thr := false.
Idempotent (variable SHM255_CutMin). builtins.V255_SAVE saves. Prints CUT255 {...}."""
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
assert 'SHM255_RouteOn' in V, 'install255_route first'
if 'SHM255_CutMin' in V: out['patch'] = 'already'
else:
    PSD = u.PoseSearchDatabase.static_class()
    ensure_vars(bp, [('SHM255_CutMin', 'float', 'SHM'), ('SHM255_DB_CutR', PSD, 'SHM'), ('SHM255_DB_CutL', PSD, 'SHM'), ('SHM255_DB_JogCutR', PSD, 'SHM'), ('SHM255_DB_JogCutL', PSD, 'SHM')]); compile_ok(bp)
    set_defaults(bp, {'SHM255_CutMin': 60.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    ro = [p for p in sn if tid(p).endswith('|SetSHM255_RouteOn')]; assert len(ro) == 1, ro
    th = [x[0] for x in succ(ro[0]) if tid(x[0]).endswith('|SetSHM227_Thr')]; assert len(th) == 1, succ(ro[0]); th = th[0]
    nx = succ(th); assert len(nx) == 1, nx; disconnect(nx[0])
    ctl = gs.within(gs.get('SHM255_Ctl'), 0.5, 1.0e9)
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner'); vel = gs.pure('/Script/Engine.Actor:GetVelocity', {'self': pawn})
    spd = gs.pure(M + 'VSize', {'A': vel}); yv = gs.yaw(gs.pure(M + 'Conv_VectorToRotator', {'InVec': vel}))
    ydv = gs.yaw(gs.pure(M + 'Conv_VectorToRotator', {'InVec': gs.get('DesiredVelocity', COMP, ct)}))
    ra = gs.pure(M + 'NormalizeAxis', {'Angle': gs.sub(ydv, yv)}); ara = gs.pure(M + 'Abs', {'A': ra})
    ay = gs.yaw(gs.pure('/Script/Engine.Actor:K2_GetActorRotation', {'self': pawn}))
    al = gs.pure(M + 'Abs', {'A': gs.pure(M + 'NormalizeAxis', {'Angle': gs.sub(yv, ay)})})
    own = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM254_Own'})
    cut = gs.AND(gs.AND(ctl, gs.get('HasIntent', COMP, ct)), gs.AND(gs.AND(gs.get('Grounded', COMP, ct), gs.within(spd, gs.get('SHM255_RouteMinV'), 1.0e9)),
                 gs.AND(gs.within(ara, gs.get('SHM255_CutMin'), gs.get('SHM255_RevMin')), gs.AND(gs.within(al, -1.0, 60.0), gs.within(own, -1.0e9, 0.3)))))
    y, n = gs.branch(cut, (th, 'then'))
    bS, bJ = gs.branch(gs.within(spd, gs.get('SHM255_SprintV'), 1.0e9), y)
    right = gs.within(ra, 0.0, 1.0e9)
    sR, sL = gs.branch(right, bS); jR, jL = gs.branch(right, bJ)
    tails = [gs.set('SHM255_RouteDB', gs.get('SHM255_DB_CutR'), sR), gs.set('SHM255_RouteDB', gs.get('SHM255_DB_CutL'), sL), gs.set('SHM255_RouteDB', gs.get('SHM255_DB_JogCutR'), jR), gs.set('SHM255_RouteDB', gs.get('SHM255_DB_JogCutL'), jL)]
    r1 = gs.set('SHM255_RouteOn', True, tails[0])
    for t_ in tails[1:]: connect(t_, (r1[0], 'execute'))
    r2 = gs.set('SHM227_Thr', False, r1)
    connect(r2, nx[0]); connect(n, nx[0])
    out['wired'] = {'after': th.rsplit('.', 1)[-1]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM255_Ctl'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V255_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('CUT255 ' + json.dumps(out, default=str))
