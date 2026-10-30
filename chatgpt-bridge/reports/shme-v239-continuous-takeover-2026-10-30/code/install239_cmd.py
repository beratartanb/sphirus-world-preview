"""install239_cmd.py (editor job) - V2.39: exact heading map for takeover clips (behind SHM239_Own).
Measured (v239r_j39_rl_tk / rl_l): Opp takeovers ended at -76 deg instead of -90: the V2.38 contract Cmd = Yaw0 + Delta * T / 90 latches
Yaw0 / Delta about 0.1 s after the cut entry (actor yaw already 7, Delta 83) - right for T in 0..90 (it still ends on the requested yaw),
wrong outside it (T = 0 -> 7, T = -90 -> -76). A takeover clip's Turn is the true plan heading (0 = the old travel, -90 = the opposite side),
so while one is in the pose (curve SHM239_Tgt > 500) and SHM239_Own is on:
  Cmd := Yaw0 + Delta + Sign(Delta) * (T - 90)      (T = 90 still lands on the requested yaw Yaw0 + Delta)
Idempotent (marker SHM239_CmdFix). builtins.V239_SAVE saves. Prints CMD239 {...}."""
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
out = {'reloaded': names}
bp = u.load_asset(AP)
if 'SHM239_CmdFix' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM239_CmdFix', 'bool', 'SHM239')]); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    s_ = [p for p in sn if tid(p).endswith('SetSHM238_Cmd')]; assert len(s_) == 1
    old = src((s_[0], 'SHM238_Cmd')); assert len(old) == 1
    cw = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM239_Tgt'})
    on = gs.AND(gs.within(gs.get('SHM239_Own'), 0.5, 1.0e9), gs.within(cw, 500.0, 1.0e9))
    sg_ = gs.pure(M + 'SignOfFloat', {'A': gs.get('SHM238_Delta')})
    alt = gs.math(gs.math(gs.get('SHM238_Yaw0'), gs.get('SHM238_Delta'), 1), gs.mul(sg_, gs.math(gs.get('SHM238_T'), 90.0, -1)), 1)
    disconnect((s_[0], 'SHM238_Cmd')); connect(gs.select(on, alt, old[0]), (s_[0], 'SHM238_Cmd')); out['patch'] = 'takeover exact map'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('CMD239 ' + json.dumps(out, default=str))
