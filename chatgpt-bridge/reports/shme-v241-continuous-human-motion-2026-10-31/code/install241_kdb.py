"""install241_kdb.py (editor job, write manifest = ABP_GR_MotionMatchingBase + child) - V2.41: the takeover entry database is chosen by
(source, target, next contact K) - one clip per database (build241_kdb.py), behind knob SHM241_KOn (default 0 = V2.40 behaviour).
  K       := 1..4 from the curve SHM239_Step at the selection frame (contacts already made; Step 2.0 at cut time 0.44 of P10 -> K2)
  KIdx    := 4 * SHM240_EIdx + (K - 1)
  SHM241_KDB := KOn ? <SelectObject tree over SHM241_K000..K383 (missing (source, K) slots hold the V2.40 E database)> : SHM240_EDB
  Update_MotionMatching: every reader of SHM240_EDB reads SHM241_KDB (the V2.40 entry-confirmation / obstacle name tests still match:
  the new databases are named PSD_SHM240_E<eidx>_K<k>).
Splice: inserted between SetSHM240_EDB and its single exec successor; every other incoming exec link of that successor is kept and
re-pointed to the chain start (V2.40 exec-splice trap). Idempotent (marker SHM241_KDB). builtins.V241_SAVE saves. Prints KDB241I {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
V41 = '/Game/GraceRanger/SHME/Animations/V241/'; V40 = '/Game/GraceRanger/SHME/Animations/V240/'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
ok_dirty = DAS | {AP, CPA, V40 + 'PSD_SHM240_E21'}
assert all(n in ok_dirty for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {'reloaded': names}
bp = u.load_asset(AP); DBC = u.PoseSearchDatabase.static_class(); NK = 384
KV = ['SHM241_K%03d' % i for i in range(NK)]
if 'SHM241_KDB' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [(v, DBC, 'SHM241') for v in KV] + [('SHM241_KDB', DBC, 'SHM241'), ('SHM241_KIdx', 'float', 'SHM241'), ('SHM241_KOn', 'float', 'SHM241')]); compile_ok(bp)
    dfl = {'SHM241_KOn': 0.0}; nk = 0
    for i, v in enumerate(KV):
        e, k = i // 4, i % 4 + 1; p = V41 + 'PSD_SHM240_E%02d_K%d' % (e, k)
        if u.EditorAssetLibrary.does_asset_exist(p): dfl[v] = u.load_asset(p); nk += 1
        else: dfl[v] = u.load_asset(V40 + 'PSD_SHM240_E%02d' % e)
        assert dfl[v], (i, p)
    set_defaults(bp, dfl); compile_ok(bp); out['k_slots'] = nk
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    last = [p for p in sn if tid(p).endswith('SetSHM240_EDB')]; assert len(last) == 1, last; last = last[0]
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (last, 'then') in src((p, 'execute'))]
    assert len(nxt) == 1, nxt; x = nxt[0]; xsrc = list(src((x, 'execute'))); out['succ'] = [x.split('.')[-1], [s[0].split('.')[-1] + ':' + s[1] for s in xsrc]]
    disconnect((x, 'execute'))   # drops ALL predecessors of x - re-pointed below
    step = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM239_Step'})
    kf = gs.select(gs.within(step, -1.0e9, 1.999), 0.0, gs.select(gs.within(step, -1.0e9, 2.999), 1.0, gs.select(gs.within(step, -1.0e9, 3.999), 2.0, 3.0)))
    t = gs.set('SHM241_KIdx', gs.math(gs.mul(gs.get('SHM240_EIdx'), 4.0), kf, 1), (last, 'then'))
    first = t[0]
    idx = gs.get('SHM241_KIdx')
    def tree(lo, hi):
        if lo == hi: return gs.get(KV[lo])
        mid = (lo + hi) // 2
        return gs.pure(M + 'SelectObject', {'A': tree(lo, mid), 'B': tree(mid + 1, hi), 'bSelectA': gs.within(idx, lo - 0.5, mid + 0.5)})
    sel = gs.pure(M + 'SelectObject', {'A': tree(0, NK - 1), 'B': gs.get('SHM240_EDB'), 'bSelectA': gs.within(gs.get('SHM241_KOn'), 0.5, 1.0e9)})
    ct, cv = gs.cast(sel, DBC, t)
    t2 = gs.set('SHM241_KDB', cv, ct)
    connect(t2, (x, 'execute')); connect((ct[0], 'CastFailed'), (x, 'execute'))
    for s_ in xsrc:
        if tuple(s_) == (last, 'then'): continue
        connect(tuple(s_), (first, 'execute'))   # other predecessors of x now enter the new chain (it ends at x)
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = [pn(n) for n in B.find_nodes(obj(gp))]; rew = 0
    for p in nodes:
        for q in info(p).input_pins:
            for s_ in src((p, q.name)):
                if tid(s_[0]).endswith('GetSHM240_EDB'):
                    disconnect((p, q.name)); connect(g.get('SHM241_KDB'), (p, q.name)); rew += 1
    out['patch'] = {'tree_leaves': NK, 'umm_rewired': rew}
    assert rew >= 1, rew
    # census: x keeps every old predecessor (through the chain) and the chain is reachable
    xs2 = [s[0].split('.')[-1] + ':' + s[1] for s in src((x, 'execute'))]; fs = [s[0].split('.')[-1] + ':' + s[1] for s in src((first, 'execute'))]
    out['census'] = {'x_sources_now': xs2, 'chain_sources': fs}
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V241_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('KDB241I ' + json.dumps(out, default=str))
