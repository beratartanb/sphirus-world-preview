"""install240_wall.py (editor job) - V2.40: a REAL obstacle contact that stops the body ends the planned clip at once (behind SHM239_Ext,
which itself only runs with SHM239_Own or SHM240_ExtOn).
Measured (v240g30_j40_wall_ext / _tk, 30 FPS; wall across the new travel of a planned jog right cut, contact at 6.3 s, y = 105):
the residual |measured - commanded| = 98 -> Ext latched on the contact frame, the clip-speed contract stood down and the capsule
stopped (v 0) - but the component redirect episode (SHM_RedirectActive) stayed on until the plan curve ended (6.73) and the
database stayed PSD_SHM238_JogCut until 7.03: the jog cut animation ran on the spot against the wall for 0.7 s (production o is
worse: GR keeps writing the plan velocity into the wall, residual 298, for 0.5 s). The physics already decided: the body is blocked.
  SHM240_Blk := SHM239_Ext AND |pawn velocity| < SHM240_BlkSpd (60 cm/s) AND the selected database is a plan database
                (name contains JogCut / SHM239_Tk / SHM240_E) or the stand database this rule selected
  Update_MotionMatching entry (before the plan owner):
    Blk AND NOT SHM240_BlkDone -> CurrentSelectedDatabase := SHM240_BlkDB (PSD_Dense_Stand_Idles); SetDatabaseToSearch ForceInterrupt;
                                  BlkDone := true                     (ONE forced search per contact - the 120 FPS hop lesson)
    Blk AND BlkDone            -> SetDatabaseToSearch(BlkDB, DoNotInterrupt)   (the episode route cannot re-select the cut DB)
    else                       -> BlkDone := false; the existing chain
No hold, no new clip; the blend from the running pose to the stand is the existing MM blend (no wall-reaction content exists:
content limit, reported). Idempotent (marker SHM240_Blk). builtins.V240_SAVE saves. Prints WALL240 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
BLKDB = '/Game/AAMS/AAMS/Animations/Locomotion/MotionMatchingData/Databases/Dense/PSD_Dense_Stand_Idles'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {'reloaded': names}
bp = u.load_asset(AP); DBC = u.PoseSearchDatabase.static_class()
if 'SHM240_Blk' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    db = u.load_asset(BLKDB); assert db, BLKDB
    ensure_vars(bp, [('SHM240_Blk', 'bool', 'SHM240'), ('SHM240_BlkDone', 'bool', 'SHM240'), ('SHM240_BlkSpd', 'float', 'SHM240'), ('SHM240_BlkDB', DBC, 'SHM240')]); compile_ok(bp)
    set_defaults(bp, {'SHM240_BlkSpd': 60.0, 'SHM240_BlkDB': db}); compile_ok(bp)
    # 1. snapshot (game thread; Update_MotionMatching is thread-safe): the blocked read, spliced after SetSHM240_Yield
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    last = [p for p in sn if tid(p).endswith('SetSHM240_Yield')]; assert len(last) == 1
    lt = (last[0], 'then')
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and lt in src((p, 'execute'))]
    kp = {x: [s_ for s_ in src((x, 'execute')) if s_ != lt] for x in nxt}
    for x in nxt: disconnect((x, 'execute'))
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    spd = gs.pure(M + 'VSize', {'A': gs.pure('/Script/Engine.Actor:GetVelocity', {'self': pawn})})
    nm = gs.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': gs.get('CurrentSelectedDatabase')})
    has = lambda s: gs.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': nm, 'Substring': s, 'bUseCase': False, 'bSearchFromEnd': False})
    plan = gs.OR(gs.OR(has('JogCut'), has('SHM239_Tk')), gs.OR(has('SHM240_E'), has('Stand_Idles')))
    t = gs.set('SHM240_Blk', gs.AND(gs.AND(gs.get('SHM239_Ext'), gs.within(spd, -1.0, gs.get('SHM240_BlkSpd'))), plan), lt)
    for x in nxt:
        connect(t, (x, 'execute'))
        for s_ in kp[x]: connect(s_, (x, 'execute'))
    assert all(len(src((x, 'execute'))) == len(kp[x]) + 1 for x in nxt)
    # 2. Update_MotionMatching entry
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
    entry = nodes['K2Node_FunctionEntry_0']; et = (entry, 'then')
    firsts = [p for p in nodes.values() if any(q.name == 'execute' for q in info(p).input_pins) and et in src((p, 'execute'))]
    assert len(firsts) == 1, firsts
    keep = [s_ for s_ in src((firsts[0], 'execute')) if s_ != et]
    sdb = [p for p in nodes.values() if 'SetDatabaseToSearch' in tid(p)]; mm = src((sdb[0], 'MotionMatchingNode')); assert mm; mm = mm[0]
    disconnect((firsts[0], 'execute'))
    s0 = et
    bt, be = g.branch(g.get('SHM240_Blk'), s0)
    r0 = g.set('SHM240_BlkDone', False, be); connect(r0, (firsts[0], 'execute'))
    for s_ in keep: connect(s_, (firsts[0], 'execute'))
    dt, de = g.branch(g.get('SHM240_BlkDone'), bt)
    sc = g.set('CurrentSelectedDatabase', g.get('SHM240_BlkDB'), de)
    f1 = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(sc, (f1, 'execute')); connect(mm, (f1, 'MotionMatchingNode'))
    connect(g.get('SHM240_BlkDB'), (f1, 'Database')); arg(f1, 'InterruptMode', 'ForceInterrupt')
    g.set('SHM240_BlkDone', True, (f1, 'then'))
    f2 = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(dt, (f2, 'execute')); connect(mm, (f2, 'MotionMatchingNode'))
    connect(g.get('SHM240_BlkDB'), (f2, 'Database')); arg(f2, 'InterruptMode', 'DoNotInterrupt')
    out['patch'] = {'first': firsts[0].rsplit('.', 1)[-1], 'kept_links': len(keep), 'first_in_links': len(src((firsts[0], 'execute')))}
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V240_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('WALL240 ' + json.dumps(out, default=str))
