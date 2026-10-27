"""install_v233_camrec.py (editor job, write manifest: Integrated BP_ExampleCharacter_MotionMatching + /Game/GraceRanger/BP_GR_Player +
BP_Player_MM + BP_PBI_Player) - V2.33 camera auto recentre + movement input frame latch (sphirus-camera-direction).
  PARENT (Integrated BP_ExampleCharacter_MotionMatching, the AAMS integration copy - not the vendor original):
    vars GR233_MoveLatchOn (bool), GR233_MoveLatchYaw (float); the two IA_Move AddMovementInput frames (GetRightVector K2Node_CallFunction_55,
    GetForwardVector K2Node_CallFunction_39) take InRot_Yaw = Select(GR233_MoveLatchOn, GR233_MoveLatchYaw, <their control yaw>) - data only.
  CHILD (/Game/GraceRanger/BP_GR_Player GR_UpdateSHMSignals, after SetGR_SHM_CamOrbit, same SHME gate as the orbit / roll):
    GR233_MoveLatchOn <- gate AND SHM.MoveLatchOn; GR233_MoveLatchYaw <- SHM.MoveLatchYaw;
    branch(gate AND |SHM.CamRecDelta| > 1e-4) -> SetControlRotation(roll / pitch kept, yaw + CamRecDelta)  (the only control-yaw writer in
    LookDrivenLocomotion mode; the V2.21 TurnWorld writer in EventGraph runs only when LookDrivenLocomotion is false - CamRecEnabled must stay
    false there: verify233 checks).
Idempotent (state by node presence). V2.31 exec-rewire rule. builtins.V233_SAVE saves. Prints CAMREC233 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, op, arg
import builtins, json
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
PAR = '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_ExampleCharacter_MotionMatching'
MM_ = '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM'
P = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
SHC = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
M = '/Script/Engine.KismetMathLibrary:'
out = {}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
# ---- parent: vars + input frame select
par = u.load_asset(PAR); ensure_vars(par, [('GR233_MoveLatchOn', 'bool', 'GR233'), ('GR233_MoveLatchYaw', 'float', 'GR233')]); compile_ok(par)
ge = G(op(PAR) + ':EventGraph'); nde = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(ge.path))}
done = []
for vn in ('K2Node_CallFunction_55', 'K2Node_CallFunction_39'):
    vp = nde[vn]; assert 'GetRightVector' in tid(vp) or 'GetForwardVector' in tid(vp), tid(vp)
    ys = src((vp, 'InRot_Yaw')); assert len(ys) == 1, ys
    if 'SelectFloat' in tid(ys[0][0]): done.append([vn, 'already']); continue
    disconnect((vp, 'InRot_Yaw'))
    connect(ge.select(ge.get('GR233_MoveLatchOn'), ge.get('GR233_MoveLatchYaw'), ys[0]), (vp, 'InRot_Yaw'))
    done.append([vn, 'wired', ys[0][0].rsplit('.', 1)[-1]])
out['parent'] = done
# ---- child: setters + the control-yaw writer
bp = u.load_asset(P)
g = G(op(P) + ':GR_UpdateSHMSignals'); nd = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g.path))}
if any(tid(p).endswith('|SetGR233_MoveLatchOn') for p in nd.values()): out['child'] = 'already'
else:
    comp = nd['K2Node_CallFunction_0']; assert 'GetComponent' in tid(comp), tid(comp); ct = (comp, 'ReturnValue')
    gate = nd['K2Node_CommutativeAssociativeBinaryOperator_1']; assert 'AND' in tid(gate).upper(), tid(gate)
    last = [p for p in nd.values() if tid(p).endswith('SetGR_SHM_CamOrbit')]; assert len(last) == 1, last; last = last[0]
    after = []
    for n in B.find_nodes(obj(g.path)):
        for p_ in info(pn(n)).input_pins:
            s_ = src((pn(n), p_.name))
            if (last, 'then') in s_: after.append(((pn(n), p_.name), [x for x in s_ if x != (last, 'then')]))
    for ep, others in after: disconnect(ep)
    t1 = g.set('GR233_MoveLatchOn', g.AND((gate, 'ReturnValue'), g.get('MoveLatchOn', SHC, ct)), (last, 'then'))
    t2 = g.set('GR233_MoveLatchYaw', g.get('MoveLatchYaw', SHC, ct), t1)
    dl = g.get('CamRecDelta', SHC, ct)
    big = g.NOT(g.within(dl, -1.0e-4, 1.0e-4))
    bt, bf = g.branch(g.AND((gate, 'ReturnValue'), big), t2)
    ctl = g.pure('/Script/Engine.Pawn:GetControlRotation', {})
    cr = g.pure(M + 'BreakRotator', {'InRot': ctl}, 'Roll'); cp = (cr[0], 'Pitch'); cy = (cr[0], 'Yaw')
    nr = g.pure(M + 'MakeRotator', {'Roll': cr, 'Pitch': cp, 'Yaw': g.math(cy, dl)})
    gc = g.pure('/Script/Engine.Pawn:GetController', {})
    sc = g.fn('/Script/Engine.Controller:SetControlRotation'); connect(bt, (sc, 'execute')); arg(sc, 'self', gc); arg(sc, 'NewRotation', nr)
    for ep, others in after:
        connect((sc, 'then'), ep); connect(bf, ep)
        for o_ in others: connect(o_, ep)
    out['child'] = {'after': [(a[0][0].rsplit('.', 1)[-1], a[0][1]) for a in after]}
res = {}
for path in (PAR, MM_, P, CHILD):
    b_ = u.load_asset(path); st, errs = compile_ok(b_); res[path.rsplit('/', 1)[-1]] = [str(st), errs[:3]]
out['compile'] = res
ok = all('UP_TO_DATE' in v[0] and not v[1] for v in res.values()); out['ok'] = ok
if ok and getattr(builtins, 'V233_SAVE', False):
    save(*[u.load_asset(p_) for p_ in (PAR, MM_, P, CHILD)]); out['saved'] = True
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('CAMREC233 ' + json.dumps(out, default=str))
