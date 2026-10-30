"""install240_edb.py (editor job) - V2.40: DETERMINISTIC takeover entry (behind SHM239_Own; knob SHM240_Det, 1 = on).
Measured (v240a30 j39_rw tk, after install240_once): one forced search now, but motion matching still chose the entry among all takeovers
of a side / target: a P10 cut at 0.47 entered SHM239_Tk_R_P00_K4_Back at 1.03 (another source, another phase - root-relative running
poses look alike) -> 10 cm slide at the entry. The game state already names the one right clip: the playing cut's source bin (new curve
SHM240_Src on the 48 cut clips: R P00..P23 = 0..23, L = 24..47), the latched target (SHM239_TkTgt) and the next planned contact K
(SHM239_Step). Each (source, target) has its OWN entry database (PSD_SHM240_E_<idx>, build240_edb.py) holding that source's K clips, each
enterable only in [t_(K-1), t_K + 0.05] - at the request exactly one clip covers the current time, and its frame there is identical to
the playing cut.
  SHM240_Src  := curve SHM240_Src;  SHM240_EIdx := 2 * Src + (TkTgt < -45 ? 1 : 0)
  SHM240_EDB  := Det ? <SelectObject tree over SHM240_E00..E95 by EIdx> : (TkTgt < -45 ? SHM239_DB_Opp : SHM239_DB_Back)  (cast)
  Update_MotionMatching takeover branch: CurrentSelectedDatabase := SHM240_EDB; SetDatabaseToSearch(SHM240_EDB, ForceInterrupt...)
(PostSelection still confirms; the play databases are unchanged.) Idempotent (marker SHM240_EDB). builtins.V240_SAVE saves. Prints EDB240 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
V0 = '/Game/GraceRanger/SHME/Animations/V240/'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {'reloaded': names}
bp = u.load_asset(AP); DBC = u.PoseSearchDatabase.static_class(); NE = 96
EV = ['SHM240_E%02d' % i for i in range(NE)]
if 'SHM240_EDB' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [(v, DBC, 'SHM240') for v in EV] + [('SHM240_EDB', DBC, 'SHM240'), ('SHM240_Src', 'float', 'SHM240'), ('SHM240_EIdx', 'float', 'SHM240'), ('SHM240_Det', 'float', 'SHM240')]); compile_ok(bp)
    dfl = {'SHM240_Det': 1.0}
    for i, v in enumerate(EV):
        d = u.load_asset(V0 + 'PSD_SHM240_E%02d' % i); assert d, i; dfl[v] = d
    set_defaults(bp, dfl); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    last = [p for p in sn if tid(p).endswith('SetSHM240_TkT')]; assert len(last) == 1
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (last[0], 'then') in src((p, 'execute'))]
    for x in nxt: disconnect((x, 'execute'))
    t = gs.set('SHM240_Src', gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM240_Src'}), (last[0], 'then'))
    opp = gs.within(gs.get('SHM239_TkTgt'), -1.0e9, -45.0)
    t = gs.set('SHM240_EIdx', gs.math(gs.mul(gs.get('SHM240_Src'), 2.0), gs.select(opp, 1.0, 0.0), 1), t)
    idx = gs.get('SHM240_EIdx')
    def tree(lo, hi):
        if lo == hi: return gs.get(EV[lo])
        mid = (lo + hi) // 2
        return gs.pure(M + 'SelectObject', {'A': tree(lo, mid), 'B': tree(mid + 1, hi), 'bSelectA': gs.within(idx, lo - 0.5, mid + 0.5)})
    det = gs.pure(M + 'SelectObject', {'A': tree(0, NE - 1), 'B': gs.pure(M + 'SelectObject', {'A': gs.get('SHM239_DB_Opp'), 'B': gs.get('SHM239_DB_Back'), 'bSelectA': opp}),
                                       'bSelectA': gs.within(gs.get('SHM240_Det'), 0.5, 1.0e9)})
    ct, cv = gs.cast(det, DBC, t)
    t2 = gs.set('SHM240_EDB', cv, ct)
    cast_node = ct[0]
    for x in nxt: connect(t2, (x, 'execute')); connect((cast_node, 'CastFailed'), (x, 'execute'))
    # Update_MotionMatching: both takeover database setters read SHM240_EDB
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = [pn(n) for n in B.find_nodes(obj(gp))]
    rew = 0
    for p in nodes:
        for q in info(p).input_pins:
            for s_ in src((p, q.name)):
                if tid(s_[0]).endswith('GetSHM239_DB_Opp') or tid(s_[0]).endswith('GetSHM239_DB_Back'):
                    disconnect((p, q.name)); connect(g.get('SHM240_EDB'), (p, q.name)); rew += 1
    assert rew == 4, rew
    out['patch'] = {'tree_leaves': NE, 'umm_rewired': rew}
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V240_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('EDB240 ' + json.dumps(out, default=str))
