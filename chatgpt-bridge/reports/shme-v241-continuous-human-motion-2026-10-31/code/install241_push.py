"""install241_push.py (editor job, write manifest = ABP_GR_MotionMatchingBase + child, BP_GR_Player, BP_PBI_Player) - V2.41 external push:
the body keeps its heading while it catches the push (knob SHM241_PushYawK, default 1.0 = unchanged).
Measured (v240reg_j39_push_plan_tkh, 300 cm/s shove to the left during the planned right 90): the external effect withdraws the plan
(clip speed + clip heading contracts off), the catch-step family (SHM_Rec_FL_Rfoot / SHM_RecS_LR_Rfoot) is selected - but GR's
facing slew (CP_PhysicalRedirect: SetActorRotation(RInterpTo_Constant(actor, LocoYaw target, dt, GR_V25TurnRate))) kept turning the
capsule toward the OLD plan's target at 280 -> 40 deg/s: 21 -> 84 deg in 0.4 s while the velocity pointed -45 -> +5 deg; the planted
catch foot slid 26.5 cm, the loop then ran 58 deg off its velocity. A pushed human catches with the trunk where it is and turns again
only after the support is re-established.
  ABP SHM_Snapshot (after SetSHM241_KDB): pawn.GR241_YawRateK := SHM239_Ext ? SHM241_PushYawK : 1
  BP_GR_Player.GR_Impl_CP_PhysicalRedirect: RInterpTo_Constant.InterpSpeed := InterpSpeed * GR241_YawRateK
Idempotent (marker SHM241_PushYawK). builtins.V241_SAVE saves. Prints PUSH241 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
PAWN = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA, PAWN, CHILD, '/Game/GraceRanger/SHME/Animations/V240/PSD_SHM240_E21') for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name().endswith('E21')]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {'reloaded': names}
pb = u.load_asset(PAWN); bp = u.load_asset(AP)
if 'SHM241_PushYawK' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    # pawn: rate multiplier variable + RInterpTo speed
    ensure_vars(pb, [('GR241_YawRateK', 'float', 'GR241')]); compile_ok(pb); set_defaults(pb, {'GR241_YawRateK': 1.0}); compile_ok(pb)
    gp = pn(graph(pb, 'GR_Impl_CP_PhysicalRedirect')); g = G(gp); gn = [pn(n) for n in B.find_nodes(obj(gp))]
    sar = [p for p in gn if tid(p).endswith('SetActorRotation')]
    ri = [p for p in gn if 'RInterpTo_Constant' in tid(p) and any((p, 'ReturnValue') in src((s, 'NewRotation')) for s in sar)]
    assert len(ri) == 1, ([tid(p) for p in sar], ri); ri = ri[0]
    old = src((ri, 'InterpSpeed')); assert len(old) == 1, old
    disconnect((ri, 'InterpSpeed')); connect(g.mul(old[0], g.get('GR241_YawRateK')), (ri, 'InterpSpeed'))
    out['pawn_patch'] = {'rinterp': ri.split('.')[-1], 'speed_was': old[0][0].split('.')[-1]}
    # ABP: knob + snapshot write
    pcls = pb.generated_class()
    ensure_vars(bp, [('SHM241_PushYawK', 'float', 'SHM241')]); compile_ok(bp); set_defaults(bp, {'SHM241_PushYawK': 1.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    last = [p for p in sn if tid(p).endswith('SetSHM241_KDB')]; assert len(last) == 1; lt = (last[0], 'then')
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and lt in src((p, 'execute'))]
    keep = {x: [s_ for s_ in src((x, 'execute')) if s_ != lt] for x in nxt}
    for x in nxt: disconnect((x, 'execute'))
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    ct, cv = gs.cast(pawn, pcls, lt)
    k = gs.select(gs.get('SHM239_Ext'), gs.get('SHM241_PushYawK'), 1.0)
    t1 = gs.set('GR241_YawRateK', k, ct, PAWN + '.BP_GR_Player_C', cv)
    for x in nxt:
        connect(t1, (x, 'execute')); connect((ct[0], 'CastFailed'), (x, 'execute'))
        for s_ in keep[x]: connect(s_, (x, 'execute'))
    out['splice'] = {x.rsplit('.', 1)[-1]: len(src((x, 'execute'))) for x in nxt}
    assert all(len(src((x, 'execute'))) == len(keep[x]) + 2 for x in nxt), out['splice']
for name, a in (('pawn', pb), ('pawn_child', u.load_asset(CHILD)), ('abp', bp), ('abp_child', u.load_asset(CPA))):
    st, errs = compile_ok(a); out[name] = [str(st), errs[:4]]
out['ok'] = all('UP_TO_DATE' in out[k][0] and not out[k][1] for k in ('pawn', 'pawn_child', 'abp', 'abp_child'))
if out['ok'] and getattr(builtins, 'V241_SAVE', False): save(pb, u.load_asset(CHILD), bp, u.load_asset(CPA)); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('PUSH241 ' + json.dumps(out, default=str))
