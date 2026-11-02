"""install249_rm.py (editor job, write manifest = BP_SHM_HumanMotionComponent, ABP base + child, BP_GR_Player + BP_PBI_Player):
V2.49 ENGINE ROOT MOTION owns the capsule during a turning start (the V2.28/V2.38 velocity/heading contracts were an estimate of it).
Measured (turn249.py on v248prod60): capsule 0.2-5.5 cm / -5..+8 deg off the clip root path because (a) the contract engages 0.1 s late
(curve witness W read one frame late + blend), (b) Motion Matching plays the clip at 0.72-1.25x while the contract writes the 1x curve
speed, (c) a one-frame Dense_Stand_Run_Loops shuffle is selected on the request frame (family 4 is raised one frame late) -> entry blend
pose error 15 cm on the planted foot; after the turn the hold (any T2 DB clip) chained 4 clips in 0.3 s (60 FPS pops).
Patch (knob SHM249_RM, default 0 = production unchanged):
  component : RootMotionOwned (bool)
  ABP SHM_Snapshot, after SetSHM248_PrevTS:
     crop  = name(Phase27_SelectedObject) contains '_crop'
     owned = RM>0.5 AND (SHM248_TurnStart OR PrevOwned) AND (crop OR NOT PrevOwned)    (starts on the request frame, lasts while the
             cropped turn clip plays, incl. its push-off tail)
     SHM249_Owned, component RootMotionOwned := owned; SHM249_PrevOwned := owned
     if RM>0.5: SetRootMotionMode(owned ? RootMotionFromEverything : RootMotionFromMontagesOnly)
  ABP SHM_Snapshot, SHM248_TurnStart hold term: AND(TurnStart, inT2DB) -> AND(TurnStart, RM>0.5 ? crop : inT2DB)
  ABP Update_MotionMatching entry: Branch(RM>0.5 AND TurnStart AND NOT name(CurrentSelectedDatabase) contains 'SHM248_JogStartT')
     true -> SetDatabaseToSearch(StartSide ? SHM248_DB_TurnStart_L : _R) and nothing else this frame (request-frame selection)
  BP_GR_Player GR_Impl_CP_PhysicalRedirect entry: Branch(component RootMotionOwned) true -> return (no velocity / rotation writes while
     the engine applies the clip's root motion; CharacterMovement uses the extracted root motion for both)
Idempotent (variable SHM249_RM). builtins.V249_SAVE saves. Prints RM249 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, op, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMPP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent'; COMP = COMPP + '.BP_SHM_HumanMotionComponent_C'
PB = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def succ(p, pin='then'):
    return [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for o in info(p).output_pins if str(o.name) == pin for q in o.connected_pins]
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if any(k in p.get_name() for k in ('ABP_GR_MotionMatching', 'BP_GR_Player', 'BP_PBI_Player', 'BP_SHM_HumanMotionComponent'))]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
assert 'SHM248_Loco' in V, 'V2.48 chain first'
if 'SHM249_RM' in V: out['patch'] = 'already'
else:
    cb = u.load_asset(COMPP); ensure_vars(cb, [('RootMotionOwned', 'bool', 'SHM|V249')]); st, errs = compile_ok(cb); out['comp'] = [str(st), errs[:3]]
    ensure_vars(bp, [('SHM249_RM', 'float', 'SHM'), ('SHM249_Owned', 'bool', 'SHM'), ('SHM249_PrevOwned', 'bool', 'SHM')]); compile_ok(bp)
    set_defaults(bp, {'SHM249_RM': 0.0}); compile_ok(bp)
    # ---- snapshot
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'; ct = (comp[0], 'ReturnValue')
    rm = lambda: gs.within(gs.get('SHM249_RM'), 0.5, 1.0e9)
    crop = lambda: gs.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': gs.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': gs.get('Phase27_SelectedObject')}), 'Substring': '_crop', 'bUseCase': False, 'bSearchFromEnd': False})
    # hold term: the Contains(..., 'SHM248_JogStartT') node feeding the SHM248_TurnStart OR
    hold_c = [p for p in sn if p.rsplit('.', 1)[-1].startswith('K2Node_CallFunction') and 'Contains' in tid(p) and any(q.name == 'Substring' and 'SHM248_JogStartT' in str(q.value) for q in info(p).input_pins)]
    assert len(hold_c) == 1, ('hold Contains', [h.rsplit('.', 1)[-1] for h in hold_c])
    users = [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for o in info(hold_c[0]).output_pins if o.name == 'ReturnValue' for q in o.connected_pins]
    assert len(users) == 1, users
    disconnect(users[0]); newc = gs.OR(gs.AND(rm(), crop()), gs.AND(gs.NOT(rm()), (hold_c[0], 'ReturnValue'))); connect(newc, users[0]); out['hold'] = users[0][0].rsplit('.', 1)[-1]
    pts = [p for p in sn if tid(p).endswith('|SetSHM248_PrevTS')]; assert len(pts) == 1, pts
    nxt = succ(pts[0]); assert nxt, 'PrevTS successor'
    for tn, tp in nxt: disconnect((tn, tp))
    owned = gs.AND(gs.AND(rm(), gs.OR(gs.get('SHM248_TurnStart'), gs.get('SHM249_PrevOwned'))), gs.OR(crop(), gs.NOT(gs.get('SHM249_PrevOwned'))))
    t1 = gs.set('SHM249_Owned', owned, (pts[0], 'then')); t2 = gs.set('RootMotionOwned', gs.get('SHM249_Owned'), t1, COMP, ct); t3 = gs.set('SHM249_PrevOwned', gs.get('SHM249_Owned'), t2)
    b1t, b1f = gs.branch(rm(), t3); b2t, b2f = gs.branch(gs.get('SHM249_Owned'), b1t)
    fe = gs.fn('/Script/Engine.AnimInstance:SetRootMotionMode'); arg(fe, 'Value', 'RootMotionFromEverything'); connect(b2t, (fe, 'execute'))
    mo = gs.fn('/Script/Engine.AnimInstance:SetRootMotionMode'); arg(mo, 'Value', 'RootMotionFromMontagesOnly'); connect(b2f, (mo, 'execute'))
    for tn, tp in nxt: connect((fe, 'then'), (tn, tp)); connect((mo, 'then'), (tn, tp)); connect(b1f, (tn, tp))
    out['snapshot'] = {'next': [a.rsplit('.', 1)[-1] for a, _ in nxt], 'fe_value': [str(q.value) for q in info(fe).input_pins if q.name == 'Value'], 'mo_value': [str(q.value) for q in info(mo).input_pins if q.name == 'Value']}
    # ---- Update_MotionMatching entry override
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
    c254 = N['K2Node_CallFunction_254']; assert 'SetDatabaseToSearch' in tid(c254), tid(c254)
    mm = src((c254, 'MotionMatchingNode'))[0]; mode = [str(x.value) for x in info(c254).input_pins if str(x.name) == 'InterruptMode'][0]
    side = (N['K2Node_CallFunction_297'], 'ReturnValue'); assert 'InRange' in tid(side[0]), tid(side[0])
    ent = g.entry(); en = succ(ent[0]); assert en, 'entry successor'
    for tn, tp in en: disconnect((tn, tp))
    inT2 = g.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': g.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': g.get('CurrentSelectedDatabase')}), 'Substring': 'SHM248_JogStartT', 'bUseCase': False, 'bSearchFromEnd': False})
    cond = g.AND(g.AND(g.within(g.get('SHM249_RM'), 0.5, 1.0e9), g.get('SHM248_TurnStart')), g.NOT(inT2))
    bt, bf = g.branch(cond, ent)
    for tn, tp in en: connect(bf, (tn, tp))
    sbt, sbf = g.branch(side, bt)
    for br_, var in ((sbt, 'SHM248_DB_TurnStart_L'), (sbf, 'SHM248_DB_TurnStart_R')):
        s = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(br_, (s, 'execute'))
        connect(mm, (s, 'MotionMatchingNode')); connect(g.get(var), (s, 'Database')); arg(s, 'InterruptMode', mode)
    out['entry'] = {'old_first': [a.rsplit('.', 1)[-1] for a, _ in en], 'mode': mode}
    # ---- pawn
    g2 = G(op(PB) + ':GR_Impl_CP_PhysicalRedirect'); ent2 = g2.entry(); en2 = succ(ent2[0]); assert en2, 'redirect entry successor'
    for tn, tp in en2: disconnect((tn, tp))
    compn = g2.pure('/Script/Engine.Actor:GetComponentByClass', {'ComponentClass': COMP})
    pt, pf = g2.branch(g2.get('RootMotionOwned', COMP, compn), ent2)
    for tn, tp in en2: connect(pf, (tn, tp))
    out['pawn'] = [a.rsplit('.', 1)[-1] for a, _ in en2]
    for name, a in (('abp', bp), ('abp_child', u.load_asset(CPA)), ('pawn', u.load_asset(PB)), ('pawn_child', u.load_asset(CHILD))):
        st, errs = compile_ok(a); out[name] = [str(st), errs[:4]]
    out['ok'] = all('UP_TO_DATE' in out[k][0] and not out[k][1] for k in ('comp', 'abp', 'abp_child', 'pawn', 'pawn_child'))
    if out['ok'] and getattr(builtins, 'V249_SAVE', False): save(cb, bp, u.load_asset(CPA), u.load_asset(PB), u.load_asset(CHILD)); out['saved'] = True
cdo = u.get_default_object(u.load_asset(AP).generated_class()); out['knobs'] = {k: str(cdo.get_editor_property(k)) for k in ('SHM249_RM', 'SHM248_On')}
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('RM249 ' + json.dumps(out, default=str))
