"""install_v234_loco.py (editor job, write manifest: /Game/GraceRanger/BP_GR_Player + BP_PBI_Player) - V2.34 locomotion frame
(sphirus-camera-direction): the automatic camera must not change the body's speed class, gait, facing or backward intent.
  BP_GR_Player vars GR234_LocoOn (bool), GR234_LocoYaw (float); GR_UpdateSHMSignals, after SetGR233_MoveLatchYaw (same SHME gate):
    GR234_LocoOn <- gate AND SHM.LocoOn; GR234_LocoYaw <- SHM.LocoYaw.
  Every GetControlRotation read in the LOCOMOTION functions (CalculateMaxSpeed, CalculateMaxAcceleration, CalculateGroundFriction,
  GetDesiredGait, GR_Impl_CR_UpdateBackwardIntent, GR_Impl_CP_PhysicalRedirect, GR_UpdateIdleTurn) is replaced by
  MakeRotator(roll, pitch, Select(GR234_LocoOn, GR234_LocoYaw, control yaw)) - data only; with GR234_LocoOn false the result is the control
  rotation itself (V2.33 behaviour). Camera functions (GR_UpdateRig, orbit, CT_*) keep the control rotation.
Idempotent (a function already reading GR234_LocoYaw is skipped). builtins.V234_SAVE saves. Prints LOCO234 {...} incl. a census per function
(control-rotation reads left unrouted must be 0)."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, op, arg
import builtins, json
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
P = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
SHC = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
M = '/Script/Engine.KismetMathLibrary:'
FUNCS = ['CalculateMaxSpeed', 'CalculateMaxAcceleration', 'CalculateGroundFriction', 'GetDesiredGait', 'GR_Impl_CR_UpdateBackwardIntent',
         'GR_Impl_CP_PhysicalRedirect', 'GR_UpdateIdleTurn']
out = {}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def nodes(g): return {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g.path))}
bp = u.load_asset(P); ensure_vars(bp, [('GR234_LocoOn', 'bool', 'GR234'), ('GR234_LocoYaw', 'float', 'GR234')]); compile_ok(bp)
# ---- writer
g = G(op(P) + ':GR_UpdateSHMSignals'); nd = nodes(g)
if any(tid(p).endswith('|SetGR234_LocoYaw') for p in nd.values()): out['writer'] = 'already'
else:
    comp = nd['K2Node_CallFunction_0']; assert 'GetComponent' in tid(comp), tid(comp); ct = (comp, 'ReturnValue')
    gate = nd['K2Node_CommutativeAssociativeBinaryOperator_1']; assert 'AND' in tid(gate).upper(), tid(gate)
    last = [p for p in nd.values() if tid(p).endswith('|SetGR233_MoveLatchYaw')]; assert len(last) == 1, last; last = last[0]
    after = [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0])
             for o in info(last).output_pins if str(o.name) == 'then' for q in o.connected_pins]
    for tn, tp in after: disconnect((tn, tp))
    t1 = g.set('GR234_LocoOn', g.AND((gate, 'ReturnValue'), g.get('LocoOn', SHC, ct)), (last, 'then'))
    t2 = g.set('GR234_LocoYaw', g.get('LocoYaw', SHC, ct), t1)
    for tn, tp in after: connect(t2, (tn, tp))
    out['writer'] = {'after': [a.rsplit('.', 1)[-1] for a, _ in after]}
# ---- locomotion readers
cen = {}
for fname in FUNCS:
    gf = G(op(P) + ':' + fname); nf = nodes(gf)
    ctls = [p for p in nf.values() if tid(p).endswith('GetControlRotation')]
    if any(tid(p).endswith('|GetGR234_LocoYaw') for p in nf.values()):
        cen[fname] = {'ctl_reads': len(ctls), 'state': 'already'}; continue
    routed = 0
    for c in ctls:
        users = []
        for n in B.find_nodes(obj(gf.path)):
            for p_ in info(pn(n)).input_pins:
                if (c, 'ReturnValue') in src((pn(n), p_.name)): users.append((pn(n), p_.name))
        if not users: continue
        br = gf.fn(M + 'BreakRotator', {'InRot': (c, 'ReturnValue')})
        yaw = gf.select(gf.get('GR234_LocoOn'), gf.get('GR234_LocoYaw'), (br, 'Yaw'))
        mr = gf.fn(M + 'MakeRotator', {'Roll': (br, 'Roll'), 'Pitch': (br, 'Pitch'), 'Yaw': yaw})
        for ep in users:
            disconnect(ep); connect((mr, 'ReturnValue'), ep)
        routed += 1
    left = 0
    for c in ctls:   # census: every control-rotation read must now feed only the new BreakRotator
        for n in B.find_nodes(obj(gf.path)):
            for p_ in info(pn(n)).input_pins:
                if (c, 'ReturnValue') in src((pn(n), p_.name)) and 'BreakRotator' not in tid(pn(n)): left += 1
    cen[fname] = {'ctl_reads': len(ctls), 'routed': routed, 'unrouted_users': left}
out['readers'] = cen
res = {}
for path in (P, CHILD):
    b_ = u.load_asset(path); st, errs = compile_ok(b_); res[path.rsplit('/', 1)[-1]] = [str(st), errs[:3]]
out['compile'] = res
ok = all('UP_TO_DATE' in v[0] and not v[1] for v in res.values()) and all(c.get('unrouted_users', 0) == 0 for c in cen.values()) \
     and all(c['ctl_reads'] > 0 for c in cen.values())
out['ok'] = ok
if ok and getattr(builtins, 'V234_SAVE', False):
    save(*[u.load_asset(p_) for p_ in (P, CHILD)]); out['saved'] = True
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('LOCO234 ' + json.dumps(out, default=str))
