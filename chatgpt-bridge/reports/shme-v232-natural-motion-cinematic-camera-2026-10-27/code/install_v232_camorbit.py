"""SHME V2.32 cinematic-orbit installer for BP_GR_Player (idempotent; state key v232_orbit; V2.4 install_v24_cam pattern).
- new var GR_SHM_CamOrbit (float);
- GR_UpdateSHMSignals: after SetGR_SHM_CamRoll -> GR_SHM_CamOrbit <- Select(HumanStateEnabled AND CameraPhysicalSignalsEnabled, SHM.CamOrbitYaw, 0)
  (the same gate the V2.4 roll uses);
- GR_UpdateRig: the RangerCameraBoom relative rotation (MakeRotator K2Node_CallFunction_43) Yaw <- (its current source) + GR_SHM_CamOrbit.
  The boom AND every collision trace of the rig are built from that rotator (K2Node_CallFunction_101 / 268 / 437 / 452), so the orbited
  camera is collision-checked; the control rotation and the movement input frame (control yaw) are untouched.
V2.31 exec-rewire rule: every exec input touched keeps ALL its other sources (printed before / after). builtins.V232_SAVE saves."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, op
import builtins
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
P = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
SHC = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
STATE = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/SHME_V232_20261027/install_state.json'
state = json.loads(STATE.read_text()) if STATE.exists() else {}; out = {}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
bp = u.load_asset(P); ensure_vars(bp, [('GR_SHM_CamOrbit', 'float', 'SHM')]); compile_ok(bp)
g = G(op(P) + ':GR_UpdateSHMSignals'); nd = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g.path))}
g2 = G(op(P) + ':GR_UpdateRig'); nd2 = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g2.path))}
mk = nd2['K2Node_CallFunction_43']; assert 'MakeRotator' in tid(mk), tid(mk)
have_set = [p for p in nd.values() if tid(p).endswith('SetGR_SHM_CamOrbit')]
ysrc = src((mk, 'Yaw'))
out['before'] = {'yaw_src': [(a.rsplit('.', 1)[-1], b) for a, b in ysrc], 'orbit_sets': len(have_set)}
if not have_set:
    comp = nd['K2Node_CallFunction_0']; assert 'GetComponent' in tid(comp), tid(comp)
    last = [p for p in nd.values() if tid(p).endswith('SetGR_SHM_CamRoll')]; assert len(last) == 1, last; last = last[0]
    gate = nd['K2Node_CommutativeAssociativeBinaryOperator_1']; assert 'AND' in tid(gate).upper(), tid(gate)
    # every exec input fed by CamRoll.then, with ALL its sources (an exec input may have several)
    after = []
    for n in B.find_nodes(obj(g.path)):
        for p in info(pn(n)).input_pins:
            s_ = src((pn(n), p.name))
            if (last, 'then') in s_: after.append(((pn(n), p.name), [x for x in s_ if x != (last, 'then')]))
    out['after_exec'] = [(a[0][0].rsplit('.', 1)[-1], a[0][1], [x[0].rsplit('.', 1)[-1] for x in a[1]]) for a in after]
    orb = g.get('CamOrbitYaw', SHC, (comp, 'ReturnValue'))
    t = g.set('GR_SHM_CamOrbit', g.select((gate, 'ReturnValue'), orb, 0.0), (last, 'then'))
    for ep, others in after:
        disconnect(ep); connect(t, ep)
        for o_ in others: connect(o_, ep)
    out['after_exec_now'] = [(a[0][0].rsplit('.', 1)[-1], a[0][1], [x[0].rsplit('.', 1)[-1] for x in src(a[0])]) for a in after]
if not any('Dot_VectorVector' in tid(a) or 'DotProduct' in tid(a) for a, _ in ysrc) or not have_set:
    assert len(ysrc) == 1, ysrc
    old = ysrc[0]
    disconnect((mk, 'Yaw')); connect(g2.math(old, g2.get('GR_SHM_CamOrbit')), (mk, 'Yaw'))
    out['yaw_rewired'] = True
out['after'] = {'yaw_src': [(a.rsplit('.', 1)[-1], tid(a).split('|')[-1]) for a, b in src((mk, 'Yaw'))]}
bp = u.load_asset(P); st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:4]
ch = u.load_asset(CHILD); out['child'] = str(compile_ok(ch)[0])
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child']
if ok and getattr(builtins, 'V232_SAVE', False):
    save(bp, ch); out['saved'] = True; state['v232_orbit'] = out.get('after'); STATE.parent.mkdir(parents=True, exist_ok=True); STATE.write_text(json.dumps(state, default=str))
print('ORBIT232 ' + json.dumps(out, default=str))
