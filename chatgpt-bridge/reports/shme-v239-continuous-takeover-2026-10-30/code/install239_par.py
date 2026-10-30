"""install239_par.py (editor job) - V2.39: the takeover force is an alternating EDGE, the latch outlasts the entry blend (after _srch).
Measured (v239l / v239m j39_rl*, j39_rw): a forced SetDatabaseToSearch(takeover, ForceInterruptAndInvalidateContinuingPose) repeated on 7
consecutive frames never switched; every successful switch happened on the FIRST forced frame after a non-forced frame (rl 6.133, rl_e
5.93, v239l 6.133), and none earlier than ~0.5 s after the cut entry (MM BlendTime 0.5 s).
Patch: SHM239_TkPar := TkOn AND NOT TkPar (true, false, true, ... while latched); the Update_MotionMatching takeover branch reads
TkOn AND TkPar (odd frames take the hold path = one non-forced frame between forces); the latch lasts up to 16 frames (was 6).
Idempotent (marker SHM239_TkPar). builtins.V239_SAVE saves. Prints PAR239 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
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
if 'SHM239_TkPar' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM239_TkPar', 'bool', 'SHM239')]); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    on = [p for p in sn if tid(p).endswith('SetSHM239_TkOn')]; assert len(on) == 1
    # latch length: the InRange(TkN, -1, 6) under SetSHM239_TkOn -> Max 16
    seen, stack, rng = set(), [on[0]], []
    while stack:
        n_ = stack.pop()
        if n_ in seen: continue
        seen.add(n_)
        for q in info(n_).input_pins:
            if q.name in ('execute', 'then', 'self'): continue
            for s_ in src((n_, q.name)):
                if 'InRange' in tid(s_[0]) and any(tid(v[0]).endswith('GetSHM239_TkN') for v in src((s_[0], 'Value'))): rng.append(s_[0])
                elif not tid(s_[0]).startswith('|Get'): stack.append(s_[0])
    rng = sorted(set(rng)); assert len(rng) == 1, rng; arg(rng[0], 'Max', '16.0'); out['latch'] = 16
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (on[0], 'then') in src((p, 'execute'))]
    for x in nxt: disconnect((x, 'execute'))
    t = gs.set('SHM239_TkPar', gs.AND(gs.get('SHM239_TkOn'), gs.NOT(gs.get('SHM239_TkPar'))), (on[0], 'then'))
    for x in nxt: connect(t, (x, 'execute'))
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = [pn(n) for n in B.find_nodes(obj(gp))]
    br = [p for p in nodes if any(q.name == 'Condition' for q in info(p).input_pins) and any(tid(s[0]).endswith('GetSHM239_TkOn') for s in src((p, 'Condition')))]
    assert len(br) == 1, br
    disconnect((br[0], 'Condition')); connect(g.AND(g.get('SHM239_TkOn'), g.get('SHM239_TkPar')), (br[0], 'Condition')); out['patch'] = 'force on TkOn AND TkPar'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('PAR239 ' + json.dumps(out, default=str))
