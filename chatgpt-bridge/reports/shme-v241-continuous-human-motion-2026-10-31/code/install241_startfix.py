"""install241_startfix.py (editor job, write manifest = ABP_GR_MotionMatchingBase + child) - V2.41 start heading contract fix: the
clip-yaw curve is BLENDED with the next clip on the way out (v241g30b_jstart_st: SW 0.95 -> 0.62 -> 0.18 while SYaw 36 -> 27 -> 8, the
command followed and turned the body back 36 -> 18 deg). The contract now reads the clip's own value SYaw / max(SW, 0.01) (as V2.38's
Turn / W). Every reader of the SHM241_SYaw curve node in SHM_Snapshot is re-pointed. Idempotent (marker: a Divide node fed by the curve).
builtins.V241_SAVE saves. Prints SFIX241 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
bp = u.load_asset(AP); sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
def curve_nodes(name): return [p for p in sn if 'GetCurveValue' in tid(p) and any(q.name == 'CurveName' and str(q.value) == name for q in info(p).input_pins)]
cy = curve_nodes('SHM241_SYaw'); cw = curve_nodes('SHM241_SW'); assert len(cy) == 1 and len(cw) == 1, (cy, cw)
cy = cy[0]; cw = cw[0]
users = []
for p in sn:
    for q in info(p).input_pins:
        if (cy, 'ReturnValue') in src((p, q.name)): users.append((p, q.name))
if any('Divide' in tid(p) or 'SafeDiv' in tid(p) for p, _ in users): out['patch'] = 'already'
else:
    div = gs.pure(M + 'SafeDivide', {'A': (cy, 'ReturnValue'), 'B': gs.pure(M + 'FMax', {'A': (cw, 'ReturnValue'), 'B': 0.01})})
    for p, q in users: disconnect((p, q)); connect(div, (p, q))
    out['patch'] = {'rewired': len(users)}
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:4]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V241_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('SFIX241 ' + json.dumps(out, default=str))
