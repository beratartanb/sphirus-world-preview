"""install255_v7.py (editor job, write manifest = ABP base + child): V2.55 speed limits on the right quantity (knob SHM255_Ctl).
Measured (v255k60 s54_revR, 5.65-5.85 s): ClipSpeed is the BODY-AXIS component. While the yaw contract turns the body the component falls with cos(yaw) although the travel does not; install255_v5 clamped that component
against the total speed at 900 cm/s2, the capsule could not follow (Cmd 51, |v| 181, vy -95), and when Cmd went negative the clamp released: 181 -> 72 in one step, 2 g.
(1) The rate clamp of install255_v5 now applies only before the body turns: Phase < 0.5 (component == speed there).
(2) No free speed in any phase, on the VECTOR: after SetClipSpeedLat, mag = |(ClipSpeed, ClipSpeedLat)|, hi = speed + AccRate dt; both are scaled by hi / mag when mag > hi while a plan is in the pose.
Idempotent (variable SHM255_K). builtins.V255_SAVE saves. Prints V7255 {...}."""
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
assert 'SHM255_Fire' in V, 'install255_v6 first'
if 'SHM255_K' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM255_K', 'float', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM255_K': 1.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    def curve(n): return gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': n})
    ctl = gs.within(gs.get('SHM255_Ctl'), 0.5, 1.0e9)
    ng = [p for p in sn if tid(p).endswith('|SetSHM255_NoGain')]; assert len(ng) == 1, ng
    c3 = [x[0] for x in succ(ng[0]) if tid(x[0]).endswith('|SetClipSpeed')]; assert len(c3) == 1
    c4 = [x[0] for x in succ(c3[0]) if tid(x[0]).endswith('|SetClipSpeed')]; assert len(c4) == 1
    c5 = [x[0] for x in succ(c4[0]) if tid(x[0]).endswith('|SetClipSpeed')]; assert len(c5) == 1, succ(c4[0]); c5 = c5[0]
    sel = src((c5, 'ClipSpeed')); assert len(sel) == 1 and 'SelectFloat' in tid(sel[0][0]), (sel, tid(sel[0][0]) if sel else '')
    sel = sel[0][0]; disconnect((sel, 'bPickA'))
    own = curve('SHM254_Own'); ph = curve('SHM255_Phase')
    connect(gs.AND(gs.AND(ctl, gs.within(own, 0.02, 1.0e9)), gs.AND(gs.within(ph, -1.0, 0.5), gs.within(gs.get('ClipSpeed', COMP, ct), 0.0, 1.0e9))), (sel, 'bPickA'))
    sl = [p for p in sn if tid(p).endswith('|SetClipSpeedLat') and any('SetClipSpeedOn' in tid(s_[0]) for s_ in src((p, 'execute')))]; assert len(sl) == 1, sl; sl = sl[0]
    nx = succ(sl); assert len(nx) == 1 and len(src(nx[0])) == 1, nx; disconnect(nx[0])
    spd = gs.pure(M + 'VSize', {'A': gs.pure('/Script/Engine.Actor:GetVelocity', {'self': gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')})})
    dt = gs.pure('/Script/Engine.GameplayStatics:GetWorldDeltaSeconds')
    hi = gs.math(spd, gs.mul(gs.get('SHM255_AccRate'), dt))
    cs = gs.get('ClipSpeed', COMP, ct); cl = gs.get('ClipSpeedLat', COMP, ct)
    mag = gs.pure(M + 'VSize', {'A': gs.pure('MakeVector', {'X': cs, 'Y': cl, 'Z': 0.0})})
    plan = gs.AND(ctl, gs.OR(gs.within(curve('SHM254_Own'), 0.02, 1.0e9), gs.within(curve('SHM254_W'), 0.02, 1.0e9)))
    over = gs.AND(plan, gs.within(mag, hi, 1.0e9))
    k = gs.select(over, gs.pure(M + 'Divide_DoubleDouble', {'A': hi, 'B': gs.pure(M + 'FMax', {'A': mag, 'B': 1.0})}) if False else gs.pure(M + 'SafeDivide', {'A': hi, 'B': mag}), 1.0)
    t1 = gs.set('SHM255_K', k, (sl, 'then'))
    t2 = gs.set('ClipSpeed', gs.mul(gs.get('ClipSpeed', COMP, ct), gs.get('SHM255_K')), t1, COMP, ct)
    t3 = gs.set('ClipSpeedLat', gs.mul(gs.get('ClipSpeedLat', COMP, ct), gs.get('SHM255_K')), t2, COMP, ct)
    connect(t3, nx[0]); out['wired'] = {'sel': sel.rsplit('.', 1)[-1], 'lat': sl.rsplit('.', 1)[-1]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM255_Ctl'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V255_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('V7255 ' + json.dumps(out, default=str))
