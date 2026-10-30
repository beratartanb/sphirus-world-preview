"""install239_play.py (editor job) - V2.39: entry database != play database for takeovers (after install239_thr).
Measured (v239j_j39_rl_tk / rw_tk): prefix-only BranchIn windows (entry databases) made the entry exact (P10_K3_Opp@0.73 while the cut
was at 0.70), but at the end of the window the node searched again despite SearchThrottleTime (the engine only holds a pose that can
continue INSIDE the sampled range) and re-entered other prefixes in a loop (K1_Opp@0.23 -> P21_K1@0.43 -> P10_K3@0.67 ...).
Now, as soon as a takeover clip is in the pose (SHM239_TkPlay), Update_MotionMatching switches to the PLAY database of its target
(PSD_SHM239_TkP_Back / _Opp: the same clips, FULL windows) with InterruptOnDatabaseChange (the continuing pose stays a candidate and is
inside the play database's sampled range; continuing bias -25) - the throttle then holds it to the end of its planned turn.
Target from the clip curve: SHM239_Tgt < 950 -> Opp (910), else Back (1000).
Idempotent (marker variable SHM239_DBP_Back). builtins.V239_SAVE saves. Prints PLAY239 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
V9 = '/Game/GraceRanger/SHME/Animations/V239'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': names}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
bp = u.load_asset(AP)
if 'SHM239_DBP_Back' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    DBC = u.PoseSearchDatabase.static_class()
    ensure_vars(bp, [('SHM239_DBP_Back', DBC, 'SHM239'), ('SHM239_DBP_Opp', DBC, 'SHM239')]); compile_ok(bp)
    set_defaults(bp, {'SHM239_DBP_Back': u.load_asset(V9 + '/PSD_SHM239_TkP_Back'), 'SHM239_DBP_Opp': u.load_asset(V9 + '/PSD_SHM239_TkP_Opp')}); compile_ok(bp)
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = [pn(n) for n in B.find_nodes(obj(gp))]
    hold = [p for p in nodes if 'SetDatabaseToSearch' in tid(p) and any(tid(s[0]).endswith('GetCurrentSelectedDatabase') for s in src((p, 'Database')))
            and any(s[1] == 'else' for s in src((p, 'execute')))]
    hold = [p for p in hold if any(any(tid(v[0]).endswith('GetSHM239_TkOn') for v in src((s[0], 'Condition'))) for s in src((p, 'execute')))]
    assert len(hold) == 1, hold
    ex = src((hold[0], 'execute')); assert len(ex) == 1; disconnect((hold[0], 'execute'))
    mm = src((hold[0], 'MotionMatchingNode'))[0]
    pt, pe = g.branch(g.get('SHM239_TkPlay'), ex[0])
    connect(pe, (hold[0], 'execute'))
    ot, oe = g.branch(g.within(g.get('SHM239_TgtC'), 500.0, 950.0), pt)
    for tt, var in ((ot, 'SHM239_DBP_Opp'), (oe, 'SHM239_DBP_Back')):
        sc = g.set('CurrentSelectedDatabase', g.get(var), tt)
        s1 = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(sc, (s1, 'execute')); connect(mm, (s1, 'MotionMatchingNode'))
        connect(g.get(var), (s1, 'Database')); arg(s1, 'InterruptMode', 'InterruptOnDatabaseChange')
    out['patch'] = 'TkPlay -> play database (InterruptOnDatabaseChange)'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]
cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
def rd(b, k):
    v = u.get_default_object(b.generated_class()).get_editor_property(k); return v.get_name() if hasattr(v, 'get_name') else v
out['defaults'] = {k: rd(cpb, k) for k in ('SHM239_DBP_Back', 'SHM239_DBP_Opp')}
ok = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['defaults']['SHM239_DBP_Opp'] == 'PSD_SHM239_TkP_Opp'
out['ok'] = ok
if ok and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('PLAY239 ' + json.dumps(out, default=str))
