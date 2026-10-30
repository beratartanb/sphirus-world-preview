"""install240_head.py (editor job) - V2.40: head priority between the player's MANUAL look and the body's physical motion (knob
SHM240_HeadOn, default 0 = production unchanged).
Measured (v240f30_j39_lr_o / _tk, j39_rl_tk, 30 FPS; head axis vaz_head, world yaw): after a hard 90 cut the head pointed at the CAMERA
forward (control yaw 0) while the body travelled +-90: head - travel = -80 deg at 6.4 s in production, +79 deg in the takeover, until
the camera recentre (V2.33 camrec, starts ~1 s later) turned the control yaw. The first layer that diverges from the travel is the
vendor aim offset: Get_AOValue = Delta(ControlRotation, RootTransform) -> Lerp(AO, 0, curve Disable_AO) -> AimYaw (|yaw| <= 115 in
Enable_AO). The source / MM pose and the V2.25 / V2.38 LookAt layers look along the travel; the AO turns the head back to the camera
although the player did not look (no IA_Look pulse). Priority:
  manual look      the player looked within SHM240_LookHold-ish (pawn TW_LastLookTime, the IA_Look pulse clock): AO owns the head
  physical motion  moving (|v| >= 80) and no manual look for 1.4 s: the AO fades out -> pose + travel gaze own the head
  standing         unchanged (the AO looks where the camera looks)
  SHM240_AOFadeT := HeadOn * map(|v|, 30, 80, 0, 1) * map(Now - TW_LastLookTime, 0.8, 1.4, 0, 1)
  SHM240_AOFade  := FInterpTo(AOFade, AOFadeT, dt, SHM240_AOFadeRate 4)       (no snap in either direction, frame-rate independent)
  Get_AOValue Lerp alpha := FMax(curve Disable_AO, SHM240_AOFade)
Snapshot splice after SetSHM240_Yield keeps every other incoming exec link (V2.40 exec-splice trap); a failed pawn cast continues the
chain. Idempotent (marker SHM240_HeadOn). builtins.V240_SAVE saves. Prints HEAD240 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
PAWN = '/Game/GraceRanger/BP_GR_Player'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {'reloaded': names}
bp = u.load_asset(AP)
if 'SHM240_HeadOn' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    pcls = u.load_asset(PAWN).generated_class(); assert pcls
    ensure_vars(bp, [('SHM240_HeadOn', 'float', 'SHM240'), ('SHM240_AOFade', 'float', 'SHM240'), ('SHM240_AOFadeT', 'float', 'SHM240'), ('SHM240_AOFadeRate', 'float', 'SHM240')]); compile_ok(bp)
    set_defaults(bp, {'SHM240_HeadOn': 0.0, 'SHM240_AOFadeRate': 4.0}); compile_ok(bp)
    # 1. snapshot: fade target + interpolated fade
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    last = [p for p in sn if tid(p).endswith('SetSHM240_Yield')]; assert len(last) == 1
    lt = (last[0], 'then')
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and lt in src((p, 'execute'))]
    keep = {x: [s_ for s_ in src((x, 'execute')) if s_ != lt] for x in nxt}
    for x in nxt: disconnect((x, 'execute'))
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    ct, cv = gs.cast(pawn, pcls, lt)
    spd = gs.pure(M + 'VSize', {'A': gs.pure('/Script/Engine.Actor:GetVelocity', {'self': pawn})})
    age = gs.sub(gs.pure('Now'), gs.get('TW_LastLookTime', PAWN + '.BP_GR_Player_C', cv))
    tgt = gs.mul(gs.mul(gs.get('SHM240_HeadOn'), gs.map(spd, 30.0, 80.0, 0.0, 1.0)), gs.map(age, 0.8, 1.4, 0.0, 1.0))
    t1 = gs.set('SHM240_AOFadeT', tgt, ct)
    dts = gs.pure('/Script/Engine.GameplayStatics:GetWorldDeltaSeconds')
    t2 = gs.set('SHM240_AOFade', gs.pure(M + 'FInterpTo', {'Current': gs.get('SHM240_AOFade'), 'Target': gs.get('SHM240_AOFadeT'), 'DeltaTime': dts, 'InterpSpeed': gs.get('SHM240_AOFadeRate')}), t1)
    for x in nxt:
        connect(t2, (x, 'execute')); connect((ct[0], 'CastFailed'), (x, 'execute'))
        for s_ in keep[x]: connect(s_, (x, 'execute'))
    out['splice'] = {x.rsplit('.', 1)[-1]: len(src((x, 'execute'))) for x in nxt}
    assert all(len(src((x, 'execute'))) == len(keep[x]) + 2 for x in nxt), out['splice']
    # 2. Get_AOValue: the Lerp alpha also reads the fade
    gp = pn(graph(bp, 'Get_AOValue')); g = G(gp); gn = [pn(n) for n in B.find_nodes(obj(gp))]
    lerp = [p for p in gn if 'Lerp' in tid(p)]; assert len(lerp) == 1, [tid(p) for p in gn]
    old = src((lerp[0], 'Alpha')); assert len(old) == 1, old
    disconnect((lerp[0], 'Alpha')); connect(g.pure(M + 'FMax', {'A': old[0], 'B': g.get('SHM240_AOFade')}), (lerp[0], 'Alpha'))
    out['patch'] = {'ao_alpha_was': old[0][0].rsplit('.', 1)[-1] + ':' + tid(old[0][0])[-30:]}
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V240_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('HEAD240 ' + json.dumps(out, default=str))
