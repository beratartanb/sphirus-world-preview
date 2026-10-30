"""diag239_umm.py (editor job) - V2.39 diagnostic: a call counter SHM239_UmmN (+1 at the entry of Update_MotionMatching) and the
owner-branch outcome SHM239_UmmOwn (set to 1 on the takeover path, 2 on the hold path, 0 else). Tests whether the MM node's update
function runs every frame (the takeover switch was missed for 7 latched frames in v239k_j39_rl_tk). Idempotent. Prints DIAG239 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
bp = u.load_asset(AP)
if 'SHM239_UmmN' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM239_UmmN', 'float', 'SHM239')]); compile_ok(bp)
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
    entry = nodes['K2Node_FunctionEntry_0']
    f = [p for p in nodes.values() if any(q.name == 'execute' for q in info(p).input_pins) and (entry, 'then') in src((p, 'execute'))]; assert len(f) == 1
    disconnect((f[0], 'execute'))
    t = g.set('SHM239_UmmN', g.math(g.get('SHM239_UmmN'), 1.0, 1), (entry, 'then')); connect(t, (f[0], 'execute')); out['patch'] = 'counter'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1]
if out['ok'] and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
print('DIAG239 ' + json.dumps(out, default=str))
