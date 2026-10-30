"""install239_thr.py (editor job) - V2.39: a takeover clip, once entered, plays without re-search (after install239_own/_tkon/_req).
Measured (v239h_j39_rl_tk / rw_tk, v239i_*_tk2): motion matching ranks frames by their future trajectory, so a frame that already runs to
the new side beats the physically planned frame whose future brakes first (entries K1_Opp@0.20 instead of K2_Opp@0.74; hops P10_K1 ->
P21_K4 -> P21_K3 under the 6-frame force latch; one shared cut+takeover database picked a takeover clip at the CUT ENTRY = a turn-back
nobody asked for - rejected). Entry is therefore CONSTRAINED, not weighted:
  * takeover databases: each clip's BranchIn window = its PREFIX only (0 .. t_K + 0.05 s, build239_tkdb 'wins'): the only enterable
    frames are before the divergence, where the current cut frame exists identically;
  * SHM239_TkPlay := SHM239_Own AND curve SHM239_Tgt > 500 (a takeover clip is in the pose) AND curve SHM238_W > 0.3 -> AnimGraph MM node
    SearchThrottleTime = FMax(old, Select(TkPlay, SHM239_ThrT 3.0 s, 0)): the clip continues past its window without a re-search (the
    V2.25 entry-window trap only bites when a search runs) until its planned turn is done (W -> 0);
  * the force latch SHM239_TkOn stops as soon as the takeover's target curve starts to blend in (SHM239_Tgt > 20, was > 500).
Idempotent (marker SHM239_ThrT). builtins.V239_SAVE saves. Prints THR239 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
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
if 'SHM239_ThrT' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM239_ThrT', 'float', 'SHM239'), ('SHM239_TkPlay', 'bool', 'SHM239')]); compile_ok(bp)
    set_defaults(bp, {'SHM239_ThrT': 3.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    last = [p for p in sn if tid(p).endswith('SetSHM239_TkOn')]; assert len(last) == 1
    # the latch's 'takeover clip not yet in the pose' test: InRange(TgtC, 500, ..) under SetSHM239_TkOn -> Min 20
    seen, stack, rng = set(), [last[0]], []
    while stack:
        n_ = stack.pop()
        if n_ in seen: continue
        seen.add(n_)
        for q in info(n_).input_pins:
            if q.name in ('execute', 'then', 'self'): continue          # data pins only (not back along the exec chain)
            for s_ in src((n_, q.name)):
                if 'InRange' in tid(s_[0]) and any(tid(v[0]).endswith('GetSHM239_TgtC') for v in src((s_[0], 'Value'))): rng.append(s_[0])
                elif not tid(s_[0]).startswith('|Get'): stack.append(s_[0])
    rng = sorted(set(rng)); assert len(rng) == 1, rng; arg(rng[0], 'Min', '20.0'); out['latch'] = 'TgtC > 20'
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (last[0], 'then') in src((p, 'execute'))]
    for x in nxt: disconnect((x, 'execute'))
    play = gs.AND(gs.AND(gs.within(gs.get('SHM239_Own'), 0.5, 1.0e9), gs.within(gs.get('SHM239_TgtC'), 500.0, 1.0e9)), gs.within(gs.get('SHM239_W'), 0.3, 1.0e9))
    t = gs.set('SHM239_TkPlay', play, (last[0], 'then'))
    for x in nxt: connect(t, (x, 'execute'))
    ag = pn(graph(bp, 'AnimGraph')); ga = G(ag)
    mm = [pn(n) for n in B.find_nodes(obj(ag)) if n.get_class().get_name() == 'AnimGraphNode_MotionMatching']; assert len(mm) == 1, mm
    old = src((mm[0], 'SearchThrottleTime')); assert len(old) == 1, old
    nm = ga.pure(M + 'FMax', {'A': old[0], 'B': ga.select(ga.get('SHM239_TkPlay'), ga.get('SHM239_ThrT'), 0.0)})
    disconnect((mm[0], 'SearchThrottleTime')); connect(nm, (mm[0], 'SearchThrottleTime')); out['graph'] = 'wired'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]
cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
ok = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
out['ok'] = ok
if ok and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('THR239 ' + json.dumps(out, default=str))
