"""install_v227d_throttle.py (editor job) - V2.27 candidate, fourth pass (60 FPS sweep: ph0 68 cm): the Motion Matching node searches every
frame; one frame after entering SHM226_JogRev_F_B_P14 (ct 0.10) it re-selected P30 (ct 0.03, the opposite foot phase) -> the loop's planted
left foot had to blend 50 cm forward at floor level. Neighbouring 32-bin phase clips start near-identical, so a second search near the entry
(or mid-clip, P14->P15 in t2 rhX1) can jump bins. New: while an authored clip is in the pose inside a held episode (SHM227_Thr = RevHold>0.5
& SHM227_Rev>0 & last frame's SHM_RedirectActive & not Dead) the AnimGraph MM node's SearchThrottleTime = FMax(old, SHM227_ThrottleT (2.5 s)):
no re-search while the pose can continue; the clip end / the hold release (database change, interrupt) / a restart (bridge database change)
still search. Same pattern as the V2.21 recovery throttle. Knob off (RevHold 0) = unchanged. Idempotent. builtins.V227_SAVE saves. Prints RH227D {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', ''); M = '/Script/Engine.KismetMathLibrary:'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name() in (AP, CP)]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
bp = u.load_asset(AP)
ensure_vars(bp, [('SHM227_Thr', 'bool', 'SHM227'), ('SHM227_ThrottleT', 'float', 'SHM227')]); compile_ok(bp)
cdo = u.get_default_object(bp.generated_class())
if abs(float(cdo.get_editor_property('SHM227_ThrottleT'))) < 1e-6: set_defaults(bp, {'SHM227_ThrottleT': 2.5}); compile_ok(bp)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
# ---- snapshot: SetSHM227_Thr after SetSHM227_Hold
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any('SetSHM227_Thr' in tid(p) and 'ThrottleT' not in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    hd = [p for p in sn if 'SetSHM227_Hold' in tid(p)]; assert len(hd) == 1, hd
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (hd[0], 'then') in src((p, 'execute'))]; assert nxt
    for x in nxt: disconnect((x, 'execute'))
    thr = gs.AND(gs.AND(gs.within(gs.get('SHM227_RevHold'), 0.5, 1.0e9), gs.within(gs.get('SHM227_Rev'), 0.001, 1.0e9)), gs.AND(gs.get('SHM_RedirectActive'), gs.NOT(gs.get('SHM227_Dead'))))
    tail = gs.set('SHM227_Thr', thr, (hd[0], 'then'))
    for x in nxt: connect(tail, (x, 'execute'))
    out['snapshot'] = 'wired'
# ---- AnimGraph MM node: SearchThrottleTime = FMax(old, Select(Thr, ThrottleT, 0))
ag = pn(graph(bp, 'AnimGraph')); ga = G(ag)
mm = [pn(n) for n in B.find_nodes(obj(ag)) if n.get_class().get_name() == 'AnimGraphNode_MotionMatching']; assert len(mm) == 1, mm
old = src((mm[0], 'SearchThrottleTime')); out['old'] = [x[0].rsplit('.', 1)[-1] + ' ' + tid(x[0])[-30:] for x in old]
already = any(tid(x[0]).endswith('Max(Float)') and any('SHM227_ThrottleT' in tid(y[0]) for k in ('A', 'B') for y in src((x[0], k))) for x in old)
if len(old) == 1 and not already:
    hold = ga.select(ga.get('SHM227_Thr'), ga.get('SHM227_ThrottleT'), 0.0)
    nm = ga.pure(M + 'FMax', {'A': old[0], 'B': hold})
    disconnect((mm[0], 'SearchThrottleTime')); connect(nm, (mm[0], 'SearchThrottleTime')); out['graph'] = 'wired'
else: out['graph'] = 'already' if already else 'unexpected'
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM227_RevHold', 'SHM227_FPOff', 'SHM227_HoldExit', 'SHM227_FlatMax', 'SHM227_ThrottleT')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and out['knobs']['SHM227_RevHold'] == 0.0 and out['knobs']['SHM227_FPOff'] == 0.0 and out['graph'] in ('wired', 'already')
out['ok'] = ok
if ok and getattr(builtins, 'V227_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('RH227D ' + json.dumps(out, default=str))
