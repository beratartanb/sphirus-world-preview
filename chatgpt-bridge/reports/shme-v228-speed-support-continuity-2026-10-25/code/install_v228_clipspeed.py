"""install_v228_clipspeed.py (editor job) - V2.28 deliverable 1, ABP side: bind the capsule speed to the authored clip's own clock.
Measured (speedclock228.py on v227t5/w20/w60/w120 ph3): Motion Matching enters the SHM226 clips at ct 0.067-0.10 on the request frame while
the capsule has braked for exactly ONE frame (33 / 50 / 17 / 8 ms) -> the clip clock runs 0.035 / -0.008 / 0.056 / 0.065 s ahead of the
capsule's brake clock; the GR friction brake (636 cm/s2) has the design slope, so the difference is a constant speed offset (25 / 0 / 55 / 75
cm/s) whose integral (9 / 0 / 24 / 22 cm) is the planted brake-foot drift (slip 21 / 11 / 35 / 36). The clips carry the designed capsule speed
(root track, now float curve SHM226_V; SHM226_W = blend-weight witness, add_speedcurve228.py).
SHM_Snapshot patch (graph-level, after SetSHM227_Thr): SHM228_DesV = V / W (W > 0.3); SHM228_On = ClipSpeed knob > 0.5 & W > 0.3 &
(last frame's ABP episode OR the component episode) & not Dead; SHM228_Cmd = DesV + LeadFrames * (DesV - PrevDesV) (one-frame look-ahead for
the movement update that consumes it next frame; knob SHM228_LeadFrames, 1.0); then writes the component contract ClipSpeed = Cmd,
ClipSpeedOn = On (BP_GR_Player applies them: install_v228_gr.py). Knob SHM228_ClipSpeed default 0 = production unchanged (installed OFF).
Idempotent (SetSHM228_DesV present). builtins.V228_SAVE saves. Prints CLIPSPEED228 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name() in (AP, CP)]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
bp = u.load_asset(AP)
ensure_vars(bp, [('SHM228_ClipSpeed', 'float', 'SHM228'), ('SHM228_LeadFrames', 'float', 'SHM228'), ('SHM228_DesV', 'float', 'SHM228'), ('SHM228_Cmd', 'float', 'SHM228'), ('SHM228_PrevDesV', 'float', 'SHM228'), ('SHM228_On', 'bool', 'SHM228')]); compile_ok(bp)
cdo = u.get_default_object(bp.generated_class())
if abs(float(cdo.get_editor_property('SHM228_LeadFrames'))) < 1e-6: set_defaults(bp, {'SHM228_LeadFrames': 1.0}); compile_ok(bp)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any('SetSHM228_DesV' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    th = [p for p in sn if 'SetSHM227_Thr' in tid(p) and 'ThrottleT' not in tid(p)]; assert len(th) == 1, th
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'
    hse = [p for p in sn if tid(p).endswith('|GetHumanStateEnabled')]; assert hse, 'HumanStateEnabled getter'
    ct = (comp[0], 'ReturnValue')
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (th[0], 'then') in src((p, 'execute'))]; assert nxt, 'next after Thr'
    for x in nxt: disconnect((x, 'execute'))
    vV = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM226_V'})
    vW = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM226_W'})
    wOK = gs.within(vW, 0.3, 1.0e9)
    desV = gs.select(wOK, gs.pure(M + 'SafeDivide', {'A': vV, 'B': vW}), 0.0)
    tail = gs.set('SHM228_DesV', desV, (th[0], 'then'))
    dv = gs.get('SHM228_DesV'); pv = gs.get('SHM228_PrevDesV')
    rdOn = gs.AND((hse[0], 'HumanStateEnabled'), gs.get('RedirectActive', COMP, ct))
    on = gs.AND(gs.AND(gs.within(gs.get('SHM228_ClipSpeed'), 0.5, 1.0e9), wOK), gs.AND(gs.OR(gs.get('SHM_RedirectActive'), rdOn), gs.NOT(gs.get('SHM227_Dead'))))
    tail = gs.set('SHM228_On', on, tail)
    # Cmd = DesV + Lead * (DesV - PrevDesV)  (PrevDesV is last frame's; when the previous frame had no clip, PrevDesV = 0 -> fall back to DesV)
    prevOK = gs.within(pv, 1.0, 1.0e9)
    prevOKneg = gs.within(pv, -1.0e9, -1.0)
    lead = gs.select(gs.OR(prevOK, prevOKneg), gs.get('SHM228_LeadFrames'), 0.0)
    diff = gs.math(dv, pv, -1)                                  # DesV - PrevDesV
    cmd = gs.math(dv, gs.pure(M + 'MapRangeUnclamped', {'Value': lead, 'InRangeA': 0.0, 'InRangeB': 1.0, 'OutRangeA': 0.0, 'OutRangeB': diff}), 1)   # DesV + lead*diff
    tail = gs.set('SHM228_Cmd', cmd, tail)
    tail = gs.set('SHM228_PrevDesV', dv, tail)
    tail = gs.set('ClipSpeed', gs.get('SHM228_Cmd'), tail, COMP, ct)
    tail = gs.set('ClipSpeedOn', gs.get('SHM228_On'), tail, COMP, ct)
    for x in nxt: connect(tail, (x, 'execute'))
    out['snapshot'] = 'wired'
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM227_RevHold', 'SHM227_FPOff', 'SHM228_ClipSpeed', 'SHM228_LeadFrames')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and out['knobs']['SHM228_ClipSpeed'] == 0.0 and out['knobs']['SHM227_RevHold'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V228_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('CLIPSPEED228 ' + json.dumps(out, default=str))
