"""install_v233_camdev.py v2 (editor job, write manifest camB) - V2.33 input-device profile for the auto recentre (sphirus-camera-direction):
the applied control-yaw turn = SHM.CamRecDelta x (GR233_RecPadScale if the most recently used hardware device is a GAMEPAD (assisted
follow, default 1.0) else GR233_RecMouseScale (mouse / keyboard: less intrusive, default 0.35)). InputDeviceSubsystem
GetMostRecentlyUsedHardwareDevice(Pawn GetPlatformUserId) -> Break -> PrimaryDeviceType == Gamepad. Auto follow and the cinematic
reaction stay separately switchable (DA CamRecEnabled / CamOrbitEnabled). Data-only rewire of the yaw sum of the V2.33 writer.
builtins.V233_SAVE saves. Prints CAMDEV233 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, op, arg
import builtins, json
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
P = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
out = {}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
bp = u.load_asset(P); ensure_vars(bp, [('GR233_RecPadScale', 'float', 'GR233'), ('GR233_RecMouseScale', 'float', 'GR233'), ('GR233_PadActive', 'bool', 'GR233')]); compile_ok(bp)
set_defaults(bp, {'GR233_RecPadScale': 1.0, 'GR233_RecMouseScale': 0.35})
g = G(op(P) + ':GR_UpdateSHMSignals'); nd = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g.path))}
sc = [p for p in nd.values() if tid(p).endswith('SetControlRotation')]; assert len(sc) == 1, sc; sc = sc[0]
mr = src((sc, 'NewRotation'))[0][0]; assert 'MakeRotator' in tid(mr), tid(mr)
dotn = src((mr, 'Yaw'))[0][0]; assert 'Dot' in tid(dotn), tid(dotn)
mv = src((dotn, 'A'))[0][0]; assert 'MakeVector' in tid(mv), tid(mv)
ysrc = src((mv, 'Y')); assert len(ysrc) == 1, ysrc
SHC = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
comp = nd['K2Node_CallFunction_0']; assert 'GetComponent' in tid(comp), tid(comp); ct = (comp, 'ReturnValue')
# v2: the scale lives IN the component (CamRecScale) so its own look detection subtracts exactly the applied turn (v1 scaled here ->
# the unscaled remainder read as a player look and stopped the recentre: mouse profile moved 1.2 deg). Undo the v1 product if present.
if 'MapRangeUnclamped' in tid(ysrc[0][0]):
    raw = src((ysrc[0][0], 'Value'))[0]; disconnect((mv, 'Y')); connect(raw, (mv, 'Y')); out['v1_product_removed'] = True
if any(tid(p).endswith('|SetCamRecScale') for p in nd.values()): out['setter'] = 'already'
else:
    ed = g.editor()
    eqs = [p for p in nd.values() if 'EnumEquality' in str(obj(p).get_class().get_name()) if obj(p)] if False else []
    sub = g.record(ed.create_node_from_name('MotorAltSistemleri|InputDeviceSubsystemAl', u.Vector2D(0, 0), []))
    hw = g.fn('/Script/Engine.InputDeviceSubsystem:GetMostRecentlyUsedHardwareDevice'); arg(hw, 'self', (sub, 'ReturnValue'))
    arg(hw, 'InUserId', g.pure('/Script/Engine.Pawn:GetPlatformUserId', {}))
    brk = g.record(ed.create_node_from_name('İşlevsellikler|Yapı|BreakHardwareDeviceIdentifier', u.Vector2D(0, 0), []))
    connect((hw, 'ReturnValue'), (brk, 'HardwareDeviceIdentifier'))
    eq = g.record(ed.create_node_from_name('İşlevsellikler|Enum|Eşit(Enum)', u.Vector2D(0, 0), []))
    connect((brk, 'PrimaryDeviceType'), (eq, 'A')); arg(eq, 'B', 'Gamepad')
    scale = g.select((eq, 'ReturnValue'), g.get('GR233_RecPadScale'), g.get('GR233_RecMouseScale'))
    last = [p for p in nd.values() if tid(p).endswith('|SetGR233_MoveLatchYaw')]; assert len(last) == 1, last; last = last[0]
    after = [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0])
             for o in info(last).output_pins if str(o.name) == 'then' for q in o.connected_pins]
    for tn, tp in after: disconnect((tn, tp))
    t_ = g.set('CamRecScale', scale, (last, 'then'), SHC, ct)
    for tn, tp in after: connect(t_, (tn, tp))
    out['setter'] = {'after': [a.rsplit('.', 1)[-1] for a, _ in after]}
st, errs = compile_ok(bp); ch = u.load_asset(CHILD); st2 = compile_ok(ch)[0]
out.update({'status': str(st), 'errs': errs[:4], 'child': str(st2)})
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in str(st2); out['ok'] = ok
if ok and getattr(builtins, 'V233_SAVE', False): save(bp, ch); out['saved'] = True
print('CAMDEV233 ' + json.dumps(out, default=str))
