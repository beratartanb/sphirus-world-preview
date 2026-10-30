"""install238_hold.py (editor job) - V2.38: the authored redirect owns its route until its planned turn is done, and its own speed restore
is not read as a shove afterwards. Behind the V2.38 knob SHM238_Yaw (0 = production unchanged).
Measured (v238c2_j38_c90l_cut1_r1): the jog-lateral ABP tail ends when the velocity is within SHM210_TailAngle (8 deg) of the input; with
the clip-bound heading that happened at clip turn 81 / 90 deg -> SHM_RedirectActive false, SHM_RedirectFrames 0 -> the database hold
dropped mid-cut (PSD_CT_JogSteady) ; 0.2 s later the push memory of the entry speed restore (PerturbState, held up to 0.8 s) routed the
standstill shove recovery (family 6, PSD_SHM_Recovery_R) -> 16-29 cm drag.
SHM_Snapshot patches (W = curve SHM238_W > 0.3 = the clip's turn is not finished; the clips drop W to 0 at 89.5 deg):
  after every SetSHM_RedirectFrames: Frames := 2 while knob & W & Frames < 0.5 (hold alive, never 1 = no bridge re-route)
  after every SetSHM_RedirectActive: Active := Active OR (knob & W)
  every SetSHM238_FamOff (install238_fam.py): LastWT := Now while knob & W; FamOff := knob & (W OR Now - LastWT < SHM238_GuardS) & family 1|6
Idempotent. builtins.V238_SAVE saves. Prints HOLD238 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': names}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
bp = u.load_asset(AP)
ensure_vars(bp, [('SHM238_LastWT', 'float', 'SHM238'), ('SHM238_GuardS', 'float', 'SHM238'), ('SHM238_HoldOn', 'bool', 'SHM238')]); compile_ok(bp)
cdo = u.get_default_object(bp.generated_class())
if abs(float(cdo.get_editor_property('SHM238_GuardS'))) < 1e-6: set_defaults(bp, {'SHM238_GuardS': 0.8}); compile_ok(bp)
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
def after(node, build):
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (node, 'then') in src((p, 'execute'))]
    for x in nxt: disconnect((x, 'execute'))
    tail = build((node, 'then'))
    for x in nxt: connect(tail, (x, 'execute'))
    return [x.rsplit('.', 1)[-1] for x in nxt]
def wok(): return gs.AND(gs.within(gs.get('SHM238_Yaw'), 0.5, 1.0e9), gs.within(gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM238_W'}), 0.3, 1.0e9))
if any('SetSHM238_HoldOn' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    out['frames'] = []; out['active'] = []; out['famoff'] = []
    for f_ in [p for p in sn if tid(p).endswith('SetSHM_RedirectFrames')]:
        def b1(t):
            t = gs.set('SHM238_HoldOn', wok(), t)
            return gs.set('SHM_RedirectFrames', gs.select(gs.AND(gs.get('SHM238_HoldOn'), gs.within(gs.get('SHM_RedirectFrames'), -1.0e9, 0.5)), 2.0, gs.get('SHM_RedirectFrames')), t)
        out['frames'].append(after(f_, b1))
    for a_ in [p for p in sn if tid(p).endswith('SetSHM_RedirectActive')]:
        out['active'].append(after(a_, lambda t: gs.set('SHM_RedirectActive', gs.OR(gs.get('SHM_RedirectActive'), wok()), t)))
    for o_ in [p for p in sn if tid(p).endswith('SetSHM238_FamOff')]:
        ex = src((o_, 'execute')); assert len(ex) == 1, ex
        disconnect((o_, 'execute')); disconnect((o_, 'SHM238_FamOff'))
        now = gs.pure('Now')
        t = gs.set('SHM238_LastWT', gs.select(wok(), now, gs.get('SHM238_LastWT')), ex[0])
        connect(t, (o_, 'execute'))
        fam = gs.get('SHM_Family'); rec = gs.OR(gs.within(fam, 0.5, 1.5), gs.within(fam, 5.5, 6.5))
        recent = gs.within(gs.sub(now, gs.get('SHM238_LastWT')), -1.0e9, gs.get('SHM238_GuardS'))
        on = gs.AND(gs.AND(gs.within(gs.get('SHM238_Yaw'), 0.5, 1.0e9), gs.OR(wok(), recent)), rec)
        connect(on, (o_, 'SHM238_FamOff'))
        out['famoff'].append(o_.rsplit('.', 1)[-1])
    assert out['frames'] and out['active'] and out['famoff'], out
    out['snapshot'] = 'wired'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]
cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM238_Yaw', 'SHM238_GuardS')}
ok = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knobs']['SHM238_Yaw'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V238_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('HOLD238 ' + json.dumps(out, default=str))
