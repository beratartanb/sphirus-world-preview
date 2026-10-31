"""install241_start.py (editor job, write manifest = ABP_GR_MotionMatchingBase + child, BP_GR_Player, BP_PBI_Player) - V2.41 START
heading contract (knob SHM241_StartOn, default 0 = unchanged).
Measured (v240reg_j39_rl_tkh 78.9 cm, v241a30_j41_rl_p10_tkh, v240reg_jstart 57-83 cm): a standing start toward a direction 45-70 deg off
the body plays the vendor TURNING start (af_Loco_Jog_Start_TurnL045 / R045, root yaw -45 / +45 in its first 0.6 s) while GR's facing
slew turns the capsule to the locomotion frame (camera input frame, LocoState 0): in j39_rl the clip turned the body 45 deg LEFT while
the capsule turned 37 deg RIGHT -> the planted feet were dragged 78.9 cm. The only start clips whose root turns now carry SHM241_SYaw
(root yaw from frame 0) / SHM241_SW (bake241_syaw.py). While such a clip is in the pose the capsule heading follows it:
  ABP SHM_Snapshot (after SetGR241_YawRateK):
    on    = StartOn & curve SW > 0.5;  rise = on & !SOnPrev
    Yaw0  := rise ? actor yaw - SY : Yaw0;   SCmd := on ? Yaw0 + SY + (SY - SYPrev) : SCmd   (one-frame look-ahead as V2.28 / V2.38)
    HoldT := on ? 0 : HoldT + dt          (default 99 = not held)
    pawn.GR241_StartYaw := SCmd;  pawn.GR241_StartOn := StartOn & HoldT <= SHM241_StartHold   (the final heading is held briefly after
    the clip so the camera frame does not turn the body back before the locomotion frame's exploration takes over)
  BP_GR_Player.GR_Impl_CP_PhysicalRedirect facing slew: Target := StartOn ? (0, StartYaw, 0) : Target;  InterpSpeed := StartOn ? 5000 : InterpSpeed
Idempotent (marker SHM241_StartOn). builtins.V241_SAVE saves. Prints START241I {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
PAWN = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'; PC = PAWN + '.BP_GR_Player_C'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA, PAWN, CHILD, '/Game/GraceRanger/SHME/Animations/V240/PSD_SHM240_E21') for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name().endswith('E21') or (p.get_name() in (AP, CPA) and not getattr(builtins, 'V241_KEEP', False))]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {'dirty_in': names}
pb = u.load_asset(PAWN); bp = u.load_asset(AP)
if 'SHM241_StartOn' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(pb, [('GR241_StartYaw', 'float', 'GR241'), ('GR241_StartOn', 'bool', 'GR241')]); compile_ok(pb)
    gp = pn(graph(pb, 'GR_Impl_CP_PhysicalRedirect')); g = G(gp); gn = [pn(n) for n in B.find_nodes(obj(gp))]
    sar = [p for p in gn if tid(p).endswith('SetActorRotation')]
    ri = [p for p in gn if 'RInterpTo_Constant' in tid(p) and any((p, 'ReturnValue') in src((s, 'NewRotation')) for s in sar)]; assert len(ri) == 1; ri = ri[0]
    otg = src((ri, 'Target')); osp = src((ri, 'InterpSpeed')); assert len(otg) == 1 and len(osp) == 1
    disconnect((ri, 'Target')); connect(g.pure(M + 'SelectRotator', {'A': g.rot(g.get('GR241_StartYaw')), 'B': otg[0], 'bPickA': g.get('GR241_StartOn')}), (ri, 'Target'))
    disconnect((ri, 'InterpSpeed')); connect(g.select(g.get('GR241_StartOn'), 5000.0, osp[0]), (ri, 'InterpSpeed'))
    out['pawn_patch'] = {'rinterp': ri.split('.')[-1], 'target_was': otg[0][0].split('.')[-1], 'speed_was': osp[0][0].split('.')[-1]}
    pcls = pb.generated_class()
    ensure_vars(bp, [('SHM241_StartOn', 'float', 'SHM241'), ('SHM241_StartHold', 'float', 'SHM241'), ('SHM241_SOnPrev', 'bool', 'SHM241'), ('SHM241_SRise', 'bool', 'SHM241'),
                     ('SHM241_SYaw0', 'float', 'SHM241'), ('SHM241_SCmd', 'float', 'SHM241'), ('SHM241_SHoldT', 'float', 'SHM241'), ('SHM241_SYPrev', 'float', 'SHM241'), ('SHM241_SOn', 'bool', 'SHM241')]); compile_ok(bp)
    set_defaults(bp, {'SHM241_StartOn': 0.0, 'SHM241_StartHold': 0.8, 'SHM241_SHoldT': 99.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    last = [p for p in sn if tid(p).endswith('SetGR241_YawRateK')]; assert len(last) == 1; lt = (last[0], 'then')
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and lt in src((p, 'execute'))]
    keep = {x: [s_ for s_ in src((x, 'execute')) if s_ != lt] for x in nxt}
    for x in nxt: disconnect((x, 'execute'))
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    ct, cv = gs.cast(pawn, pcls, lt)
    sw = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM241_SW'}); sy = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM241_SYaw'})
    onb = gs.AND(gs.within(gs.get('SHM241_StartOn'), 0.5, 1.0e9), gs.within(sw, 0.5, 1.0e9))
    t = gs.set('SHM241_SOn', onb, ct)
    t = gs.set('SHM241_SRise', gs.AND(gs.get('SHM241_SOn'), gs.NOT(gs.get('SHM241_SOnPrev'))), t)
    ay = gs.yaw(gs.pure('/Script/Engine.Actor:K2_GetActorRotation', {'self': cv}))
    t = gs.set('SHM241_SYaw0', gs.select(gs.get('SHM241_SRise'), gs.sub(ay, sy), gs.get('SHM241_SYaw0')), t)
    look = gs.select(gs.get('SHM241_SRise'), 0.0, gs.sub(sy, gs.get('SHM241_SYPrev')))   # no look-ahead on the entry frame (stale SYPrev)
    t = gs.set('SHM241_SCmd', gs.select(gs.get('SHM241_SOn'), gs.math(gs.math(gs.get('SHM241_SYaw0'), sy, 1), look, 1), gs.get('SHM241_SCmd')), t)
    dts = gs.pure('/Script/Engine.GameplayStatics:GetWorldDeltaSeconds')
    t = gs.set('SHM241_SHoldT', gs.select(gs.get('SHM241_SOn'), 0.0, gs.math(gs.get('SHM241_SHoldT'), dts, 1)), t)
    t = gs.set('SHM241_SYPrev', sy, t)
    t = gs.set('SHM241_SOnPrev', gs.get('SHM241_SOn'), t)
    t = gs.set('GR241_StartYaw', gs.get('SHM241_SCmd'), t, PC, cv)
    t = gs.set('GR241_StartOn', gs.AND(gs.within(gs.get('SHM241_StartOn'), 0.5, 1.0e9), gs.within(gs.get('SHM241_SHoldT'), -1.0, gs.get('SHM241_StartHold'))), t, PC, cv)
    for x in nxt:
        connect(t, (x, 'execute')); connect((ct[0], 'CastFailed'), (x, 'execute'))
        for s_ in keep[x]: connect(s_, (x, 'execute'))
    out['splice'] = {x.rsplit('.', 1)[-1]: len(src((x, 'execute'))) for x in nxt}
    assert all(len(src((x, 'execute'))) == len(keep[x]) + 2 for x in nxt), out['splice']
for name, a in (('pawn', pb), ('pawn_child', u.load_asset(CHILD)), ('abp', bp), ('abp_child', u.load_asset(CPA))):
    st, errs = compile_ok(a); out[name] = [str(st), errs[:4]]
out['ok'] = all('UP_TO_DATE' in out[k][0] and not out[k][1] for k in ('pawn', 'pawn_child', 'abp', 'abp_child'))
if out['ok'] and getattr(builtins, 'V241_SAVE', False): save(pb, u.load_asset(CHILD), bp, u.load_asset(CPA)); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('START241I ' + json.dumps(out, default=str))
