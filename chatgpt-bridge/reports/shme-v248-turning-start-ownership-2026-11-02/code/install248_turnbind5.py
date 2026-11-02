"""install248_turnbind5.py (editor job, write manifest = ABP base + child; after install248_turnbind4.py):
 1. REVERT turnbind4: releasing the clip-bound contract mid-clip handed the heading to the pawn's own yaw logic while the ABP redirect episode
    was alive -> yaw swung -47 / +23 / -30 / +20 (v248ti60: 60 cm drag, pop 72, SHM216_RevTurn selected). SetSHM228_On gets its turnbind3
    source back (the contract holds through the turning-start clip; T saturates at +-90 = the request heading).
 2. POST-TURN LOOP OWNERSHIP: after the turn (SHM248_TurnStart falling edge) the start-family search keeps asking the start database for the
    rest of the 2.3 s clip and then picks ANOTHER start clip (SHM237_JogStart_F at 11.8 s -> 30-47 cm hand-over drags, v248threal). While
    SHM248_PostTurn holds (set on the falling edge, cleared when the input stops), the jog start-database search is replaced by the jog LOOP
    database (SHM248_DB_Loops = PSD_CT_JogSteady): Motion Matching leaves the turn clip into a phase-matched run loop by its own cost.
    SHM_Snapshot (after SetSHM248_TT): PostTurn := SHM248_On > 0.5 AND HasAcceleration AND (PostTurn OR (PrevTS AND NOT TurnStart)); PrevTS := TurnStart
    Update_MotionMatching: in each V2.48 route branch, else -> Branch(PostTurn): true -> SetDatabaseToSearch(DB_Loops), false -> the start call.
Idempotent (variable SHM248_PostTurn). builtins.V248_SAVE saves. Prints TURNBIND248E {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]; PSD = u.PoseSearchDatabase.static_class()
assert 'SHM248_Bind4' in V, 'install248_turnbind4.py first'
if 'SHM248_PostTurn' in V: out['patch'] = 'already'
else:
    ar = u.AssetRegistryHelpers.get_asset_registry()
    loops = [a for a in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/PoseSearch', 'PoseSearchDatabase'), True) if str(a.asset_name) == 'PSD_CT_JogSteady']
    assert len(loops) == 1, ('PSD_CT_JogSteady', [str(a.package_name) for a in loops]); dbl = u.load_asset(str(loops[0].package_name)); out['loops_db'] = str(loops[0].package_name)
    ensure_vars(bp, [('SHM248_PostTurn', 'bool', 'SHM'), ('SHM248_PrevTS', 'bool', 'SHM'), ('SHM248_DB_Loops', PSD, 'SHM')]); compile_ok(bp)
    set_defaults(bp, {'SHM248_DB_Loops': dbl}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    # 1. revert turnbind4 on SetSHM228_On: source = OR(AND(NOT inTurn, old), AND(inTurn, own)) -> old
    so = [p for p in sn if tid(p).endswith('|SetSHM228_On')]; assert len(so) == 1, so
    orn = src((so[0], 'SHM228_On')); assert len(orn) == 1, orn; orn = orn[0][0]
    old = None
    for q in info(orn).input_pins:
        if q.name not in ('A', 'B'): continue
        for n_, _ in src((orn, q.name)):
            ins = [src((n_, r.name)) for r in info(n_).input_pins if r.name in ('A', 'B')]
            flat = [s_[0] for s_ in ins if s_]
            nots = [x for x in flat if 'NOT' in tid(x[0]).upper()]
            if len(flat) == 2 and len(nots) == 1: old = [x for x in flat if x not in nots][0]
    assert old, 'turnbind4 structure not found'
    disconnect((so[0], 'SHM228_On')); connect(old, (so[0], 'SHM228_On')); out['reverted_v4'] = old[0].rsplit('.', 1)[-1]
    # 2. post-turn latch after SetSHM248_TT
    tt = [p for p in sn if tid(p).endswith('|SetSHM248_TT')]; assert len(tt) == 1, tt
    nxt = [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for o in info(tt[0]).output_pins if str(o.name) == 'then' for q in o.connected_pins]
    for tn, tp in nxt: disconnect((tn, tp))
    on = gs.within(gs.get('SHM248_On'), 0.5, 1.0e9)
    fall = gs.AND(gs.get('SHM248_PrevTS'), gs.NOT(gs.get('SHM248_TurnStart')))
    val = gs.AND(gs.AND(on, gs.get('HasAcceleration')), gs.OR(gs.get('SHM248_PostTurn'), fall))
    s1 = gs.set('SHM248_PostTurn', val, (tt[0], 'then')); s2 = gs.set('SHM248_PrevTS', gs.get('SHM248_TurnStart'), s1)
    for tn, tp in nxt: connect(s2, (tn, tp))
    # 3. route: else of each V2.48 branch -> Branch(PostTurn)
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = [pn(n) for n in B.find_nodes(obj(gp))]
    brs = [p for p in nodes if 'K2Node_IfThenElse' in p and any('SHM248_TurnStart' in tid(s_[0]) for s_ in src((p, 'Condition')))]
    assert len(brs) == 2, ('V2.48 route branches', [b.rsplit('.', 1)[-1] for b in brs]); done = []
    for br in brs:
        els = [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for o in info(br).output_pins if str(o.name) == 'else' for q in o.connected_pins]
        assert len(els) == 1, els; call = els[0][0]; assert 'SetDatabaseToSearch' in tid(call), tid(call)
        mm = src((call, 'MotionMatchingNode'))[0]; mode = [str(x.value) for x in info(call).input_pins if str(x.name) == 'InterruptMode'][0]
        disconnect((call, 'execute'))
        bt, bf = g.branch(g.get('SHM248_PostTurn'), (br, 'else')); connect(bf, (call, 'execute'))
        s = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(bt, (s, 'execute'))
        connect(mm, (s, 'MotionMatchingNode')); connect(g.get('SHM248_DB_Loops'), (s, 'Database')); arg(s, 'InterruptMode', mode)
        done.append([br.rsplit('.', 1)[-1], call.rsplit('.', 1)[-1], mode])
    out['route'] = done
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: str(cdo.get_editor_property(k)).split('/')[-1][:40] for k in ('SHM248_On', 'SHM248_DB_Loops')}
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knobs']['SHM248_On'] == '0.0'
if out['ok'] and getattr(builtins, 'V248_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('TURNBIND248E ' + json.dumps(out, default=str))
