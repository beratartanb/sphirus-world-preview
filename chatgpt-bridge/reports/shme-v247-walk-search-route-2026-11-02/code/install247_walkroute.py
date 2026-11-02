"""install247_walkroute.py (editor job, write manifest = ABP base + child): V2.47 walk identity by SEARCH-ROUTE ownership.
After every walk start MM picks a Dense (Ranger/Neutral) FORWARD walk loop for ~1.45 s before the LB loop (SHM245_Walk_Fwd) wins
(V2.46: pose costs on the Dense clips cannot fix this - direct-entry ModifyCost is in-session only, the chooser rows are not scriptable
and PoseSearchDatabase has no entry API). This hook, spliced right after the chooser's SetDatabasesToSearch (K2Node_CallFunction_2) in
Update_MotionMatching, exactly like the V2.42 idle hook:
  Branch( SHM247_WalkOn > 0.5 AND name(CurrentSelectedDatabase) contains 'Dense_Stand_Walk_Loops' AND name(Phase27_SelectedObject) contains 'Walk_Loop_F' )
     true -> SetDatabaseToSearch(mm, SHM247_WalkDB, InterruptOnDatabaseChangeAndInvalidateContinuingPose) -> <old successor>
     false -> <old successor>
so whenever MM lands on a Dense forward loop, the next search is restricted to the LB family loop database (default PSD_LB_WalkLoops) for one
frame; once an LB loop is selected the condition is false and the chooser's full list (stops, links, pivots, start transfers) is searched
again with the LB loop as the continuing pose. Defaults WalkOn 0 (production unchanged). Idempotent (variable marker). builtins.V247_SAVE.
Prints WALKROUTE247 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
LB = '/Game/GraceRanger/Animations/LocomotionBehavior/PSD_LB_WalkLoops'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP)
if 'SHM247_WalkOn' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    lb = u.load_asset(LB); assert lb, 'LB walk DB'
    ensure_vars(bp, [('SHM247_WalkOn', 'float', 'SHM'), ('SHM247_WalkDB', u.PoseSearchDatabase.static_class(), 'SHM')]); compile_ok(bp)
    set_defaults(bp, {'SHM247_WalkOn': 0.0, 'SHM247_WalkDB': lb}); compile_ok(bp)
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
    cf2 = nodes['K2Node_CallFunction_2']; assert 'SetDatabasesToSearch' in tid(cf2), tid(cf2)
    sdb = [p for p in nodes.values() if 'SetDatabaseToSearch' in tid(p) and 'SetDatabasesToSearch' not in tid(p)]; mm = src((sdb[0], 'MotionMatchingNode')); assert mm; mm = mm[0]
    nxt = [p for p in nodes.values() if any(q.name == 'execute' for q in info(p).input_pins) and (cf2, 'then') in src((p, 'execute'))]
    assert len(nxt) == 1, ('CallFunction_2 successors', [p.rsplit('.', 1)[-1] for p in nxt]); tgt = nxt[0]; out['successor'] = tgt.rsplit('.', 1)[-1]
    keep = [s_ for s_ in src((tgt, 'execute')) if s_ != (cf2, 'then')]; out['kept_links'] = len(keep)
    disconnect((tgt, 'execute'))
    for s_ in keep: connect(s_, (tgt, 'execute'))
    nm = g.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': g.get('CurrentSelectedDatabase')})
    an = g.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': g.get('Phase27_SelectedObject')})
    has = lambda s_, v: g.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': s_, 'Substring': v, 'bUseCase': False, 'bSearchFromEnd': False})
    cond = g.AND(g.within(g.get('SHM247_WalkOn'), 0.5, 10.0), g.AND(has(nm, 'Dense_Stand_Walk_Loops'), has(an, 'Walk_Loop_F')))
    bt, be = g.branch(cond, (cf2, 'then'))
    f1 = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(bt, (f1, 'execute')); connect(mm, (f1, 'MotionMatchingNode'))
    connect(g.get('SHM247_WalkDB'), (f1, 'Database')); arg(f1, 'InterruptMode', 'InterruptOnDatabaseChangeAndInvalidateContinuingPose')
    connect((f1, 'then'), (tgt, 'execute')); connect(be, (tgt, 'execute'))
    out['target_in_links'] = len(src((tgt, 'execute'))); assert out['target_in_links'] == len(keep) + 2
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V247_SAVE', False): save(bp, cpb); out['saved'] = True
cdo = u.get_default_object(bp.generated_class()); out['defaults'] = {'WalkOn': cdo.get_editor_property('SHM247_WalkOn'), 'WalkDB': str(cdo.get_editor_property('SHM247_WalkDB')).split('/')[-1][:30]}
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('WALKROUTE247 ' + json.dumps(out, default=str))
