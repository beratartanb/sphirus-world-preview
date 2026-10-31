"""install241_blk.py (editor job, write manifest = ABP_GR_MotionMatchingBase + child) - V2.41 wall stop: release the search throttle
for the ONE forced obstacle search only (knob SHM241_BlkOnce, default 0 = V2.40 behaviour).
Measured (V2.40 v240j120_j40_wall_wst: the stop database's phase bins hopped P01 -> P14 -> P02 frame by frame at 120 FPS, not at 30):
install240_blk2 made the MM SearchThrottleTime pick `old OR SHM240_Blk`, i.e. the throttle is 0 for the WHOLE blocked period, so the
stop database is re-searched every frame - 4x as many chances to hop at 120 FPS (the V2.37 stop-entry hop had the same shape; its
continuing bias only hid it). The forced search needs the release on its own frame, nothing more:
  SHM_Snapshot (game thread, before Update_MotionMatching): SHM241_BlkPrev := SHM240_BlkDone (last frame's value)
  AnimGraph MM throttle pick: old OR (Blk AND (NOT BlkPrev OR BlkOnce < 0.5))
Idempotent (marker SHM241_BlkOnce). builtins.V241_SAVE saves. Prints BLK241 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
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
out = {}
bp = u.load_asset(AP)
if 'SHM241_BlkOnce' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM241_BlkOnce', 'float', 'SHM241'), ('SHM241_BlkPrev', 'bool', 'SHM241')]); compile_ok(bp); set_defaults(bp, {'SHM241_BlkOnce': 0.0}); compile_ok(bp)
    ag = pn(graph(bp, 'AnimGraph')); ga = G(ag)
    mm = [pn(n) for n in B.find_nodes(obj(ag)) if n.get_class().get_name() == 'AnimGraphNode_MotionMatching']; assert len(mm) == 1
    sel = src((mm[0], 'SearchThrottleTime')); assert len(sel) == 1
    orn = src((sel[0][0], 'bPickA')); assert len(orn) == 1 and 'OR' in tid(orn[0][0]).upper(), [tid(x[0]) for x in orn]
    orn = orn[0][0]; bin_ = [q.name for q in info(orn).input_pins if any(tid(s[0]).endswith('GetSHM240_Blk') for s in src((orn, q.name)))]
    assert len(bin_) == 1, bin_
    disconnect((orn, bin_[0]))
    term = ga.AND(ga.get('SHM240_Blk'), ga.OR(ga.NOT(ga.get('SHM241_BlkPrev')), ga.NOT(ga.within(ga.get('SHM241_BlkOnce'), 0.5, 1.0e9))))
    connect(term, (orn, bin_[0]))
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    last = [p for p in sn if tid(p).endswith('SetGR241_StartOn')]; assert len(last) == 1; lt = (last[0], 'then')
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and lt in src((p, 'execute'))]
    keep = {x: [s_ for s_ in src((x, 'execute')) if s_ != lt] for x in nxt}
    for x in nxt: disconnect((x, 'execute'))
    t = gs.set('SHM241_BlkPrev', gs.get('SHM240_BlkDone'), lt)
    for x in nxt:
        connect(t, (x, 'execute'))
        for s_ in keep[x]: connect(s_, (x, 'execute'))
    out['splice'] = {x.rsplit('.', 1)[-1]: len(src((x, 'execute'))) for x in nxt}
    assert all(len(src((x, 'execute'))) == len(keep[x]) + 1 for x in nxt), out['splice']
    out['patch'] = {'or_pin': bin_[0]}
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:4]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V241_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('BLK241 ' + json.dumps(out, default=str))
