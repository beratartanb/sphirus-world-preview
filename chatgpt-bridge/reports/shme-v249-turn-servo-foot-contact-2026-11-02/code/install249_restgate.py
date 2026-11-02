"""install249_restgate.py (editor job, write manifest = ABP base + child): the V2.49 turning-start owner acts only on a START FROM REST.
Measured (v249 i30/k30/l30 j41_rl_p10, 3 of 3 runs): SHM248_TurnStart is also true during a running reversal (jog, request behind the
body, not behind the look); the V2.49 request-frame override at the entry of Update_MotionMatching (any family) then forced the T2 start
database mid-run -> the reversal turned into a TurnL045 start + FwdLeft + shuffle chain (73 cm vs 28 cm production). V2.48 used
TurnStart only inside the family-4 start route, which is why production was unaffected.
Patch:
  SHM_Snapshot (after SetSHM249_TurnDone): SHM249_FromRest := TurnStart AND ((NOT PrevTS AND component Speed < SHM249_RestSpeed 40)
                                                                            OR (PrevTS AND FromRest))
  SetSHM249_Owned input := old AND (FromRest OR PrevOwned)
  Update_MotionMatching entry branch condition := old AND FromRest
Idempotent (variable SHM249_FromRest). builtins.V249_SAVE saves. Prints RESTGATE249 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def succ(p, pin='then'):
    return [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for o in info(p).output_pins if str(o.name) == pin for q in o.connected_pins]
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
assert 'SHM249_TurnDone' in V, 'install249_turndone.py first'
if 'SHM249_FromRest' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM249_FromRest', 'bool', 'SHM'), ('SHM249_RestSpeed', 'float', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM249_RestSpeed': 40.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'; ct = (comp[0], 'ReturnValue')
    td = [p for p in sn if tid(p).endswith('|SetSHM249_TurnDone')]; assert len(td) == 1, td
    nxt = succ(td[0]); assert nxt, 'TurnDone successor'
    for tn, tp in nxt: disconnect((tn, tp))
    rising = gs.AND(gs.NOT(gs.get('SHM248_PrevTS')), gs.within(gs.get('Speed', COMP, ct), -1.0, gs.get('SHM249_RestSpeed')))
    keep = gs.AND(gs.get('SHM248_PrevTS'), gs.get('SHM249_FromRest'))
    s1 = gs.set('SHM249_FromRest', gs.AND(gs.get('SHM248_TurnStart'), gs.OR(rising, keep)), (td[0], 'then'))
    for tn, tp in nxt: connect(s1, (tn, tp))
    so = [p for p in sn if tid(p).endswith('|SetSHM249_Owned')]; assert len(so) == 1, so
    old = src((so[0], 'SHM249_Owned')); assert len(old) == 1, old; disconnect((so[0], 'SHM249_Owned'))
    connect(gs.AND(old[0], gs.OR(gs.get('SHM249_FromRest'), gs.get('SHM249_PrevOwned'))), (so[0], 'SHM249_Owned'))
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); ent = g.entry(); first = succ(ent[0])
    assert len(first) == 1 and 'IfThenElse' in first[0][0], ('entry branch', first); br = first[0][0]
    c0 = src((br, 'Condition')); assert len(c0) == 1, c0; disconnect((br, 'Condition'))
    connect(g.AND(c0[0], g.get('SHM249_FromRest')), (br, 'Condition'))
    out['wired'] = {'turndone_next': [a.rsplit('.', 1)[-1] for a, _ in nxt], 'entry_branch': br.rsplit('.', 1)[-1]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V249_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('RESTGATE249 ' + json.dumps(out, default=str))
