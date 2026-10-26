"""fix_v231_exitpush_c.py (editor job): repair of install_v231_exitpush_b.py's exec wiring. B located the V2.14 swap branch from the Set
SHM211_DB_Push node (= IfThenElse_10, an inner branch) instead of the window branch IfThenElse_8 that install_v231_exitpush.py rewired, so
the new branch's ELSE skipped IfThenElse_8 (its PushRestore else path) = production path changed. Restores: IfThenElse_8.then ->
IfThenElse_10.execute, new branch (IfThenElse_25).else -> IfThenElse_8.execute. Prints the exec neighbourhood before/after.
builtins.V231_SAVE saves. Prints EXITPUSH231C {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
bp = u.load_asset(AP); eg = pn(graph(bp, 'EventGraph')); en = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(eg))}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def srcs(p, pin): return [(a.rsplit('.', 1)[-1], b) for a, b in src((p, pin))]
def cond(p):
    s_ = src((p, 'Condition')); return tid(s_[0][0])[-50:] if s_ else None
N8, N10, N25 = en['K2Node_IfThenElse_8'], en['K2Node_IfThenElse_10'], en['K2Node_IfThenElse_25']
out = {'before': {k: {'exec_in': srcs(v, 'execute'), 'cond': cond(v)} for k, v in (('n8', N8), ('n10', N10), ('n25', N25))}}
connect((N25, 'else'), (N8, 'execute'))
connect((N8, 'then'), (N10, 'execute'))
out['after'] = {k: {'exec_in': srcs(v, 'execute'), 'cond': cond(v)} for k, v in (('n8', N8), ('n10', N10), ('n25', N25))}
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child']
out['ok'] = ok
if ok and getattr(builtins, 'V231_SAVE', False): save(bp, cpb); out['saved'] = True
print('EXITPUSH231C ' + json.dumps(out, default=str))
