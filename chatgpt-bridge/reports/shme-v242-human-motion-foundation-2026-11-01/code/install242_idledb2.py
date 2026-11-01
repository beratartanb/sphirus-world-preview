"""install242_idledb2.py (editor job, write manifest = ABP_GR_MotionMatchingBase + child): V2.42 idle hook, second placement.
The first placement (install242_idledb.py, Update_MotionMatching ENTRY) never won: in the standing state the chain ends with
K2Node_CallFunction_2 = SetDatabasesToSearch(Databases <- K2Node_EvaluateChooser2_0 output array) which replaces the search list with the
chooser's PSD_Dense_Stand_Idles every frame, and PostSelection writes CurrentSelectedDatabase after the search. This splice goes AFTER
CallFunction_2 (its only exec successor is K2Node_IfThenElse_29, which has ~33 other incoming exec links that must be kept):
  CallFunction_2.then -> Branch( SHM242_IdleOn > 0.5 AND (name(CurrentSelectedDatabase) contains 'Stand_Idles' OR contains 'SHM242_Idle') )
     true  -> CurrentSelectedDatabase := SHM242_IdleDB -> SetDatabaseToSearch(mm, SHM242_IdleDB, InterruptOnDatabaseChangeAndInvalidateContinuingPose) -> IfThenElse_29
     false -> IfThenElse_29
The 'SHM242_Idle' term keeps the override alive once PostSelection has written the new database (the V2.40 wall patch tested its own
stand DB for the same reason). The entry patch of install242_idledb.py stays (inert once the new DB is selected). Defaults unchanged
(IdleOn 0 / IdleDB None = production). Idempotent (marker: a GetObjectName node fed by the new Contains 'SHM242_Idle'). builtins.V242_SAVE saves.
Prints IDLEDB242B {...}."""
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
if dirty: out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); assert 'SHM242_IdleOn' in [str(v) for v in B.list_variables(bp)], 'run install242_idledb.py first (variables)'
gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
marker = [p for p in nodes.values() if 'Contains' in tid(p) and any(q.name == 'Substring' and 'SHM242_Idle' in str(q.value) for q in info(p).input_pins)]
if marker: out['patch'] = 'already'
else:
    cf2s = [p for k, p in nodes.items() if 'SetDatabasesToSearch' in tid(p)]
    # two plural calls exist: K2Node_CallFunction_2 (grounded chain end, Databases <- the chooser) and K2Node_CallFunction_8 (airborne-owned route)
    cf2 = [p for p in cf2s if p.rsplit('.', 1)[-1] == 'K2Node_CallFunction_2']; assert len(cf2) == 1, ('SetDatabasesToSearch nodes', [p.rsplit('.', 1)[-1] for p in cf2s]); cf2 = cf2[0]
    out['plural_calls'] = [p.rsplit('.', 1)[-1] for p in cf2s]
    out['cf2'] = cf2.rsplit('.', 1)[-1]
    sdb = [p for p in nodes.values() if 'SetDatabaseToSearch' in tid(p) and 'SetDatabasesToSearch' not in tid(p)]; mm = src((sdb[0], 'MotionMatchingNode')); assert mm; mm = mm[0]
    nxt = [p for p in nodes.values() if any(q.name == 'execute' for q in info(p).input_pins) and (cf2, 'then') in src((p, 'execute'))]
    assert len(nxt) == 1, ('CallFunction_2 successors', [p.rsplit('.', 1)[-1] for p in nxt]); tgt = nxt[0]; out['successor'] = tgt.rsplit('.', 1)[-1]
    keep = [s_ for s_ in src((tgt, 'execute')) if s_ != (cf2, 'then')]; out['kept_links'] = len(keep)
    disconnect((tgt, 'execute'))
    for s_ in keep: connect(s_, (tgt, 'execute'))
    assert len(src((tgt, 'execute'))) == len(keep), ('re-wire', len(src((tgt, 'execute'))), len(keep))
    nm = g.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': g.get('CurrentSelectedDatabase')})
    has = lambda s: g.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': nm, 'Substring': s, 'bUseCase': False, 'bSearchFromEnd': False})
    cond = g.AND(g.within(g.get('SHM242_IdleOn'), 0.5, 10.0), g.OR(has('Stand_Idles'), has('SHM242_Idle')))
    bt, be = g.branch(cond, (cf2, 'then'))
    sc = g.set('CurrentSelectedDatabase', g.get('SHM242_IdleDB'), bt)
    f1 = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(sc, (f1, 'execute')); connect(mm, (f1, 'MotionMatchingNode'))
    connect(g.get('SHM242_IdleDB'), (f1, 'Database')); arg(f1, 'InterruptMode', 'InterruptOnDatabaseChangeAndInvalidateContinuingPose')
    connect((f1, 'then'), (tgt, 'execute')); connect(be, (tgt, 'execute'))
    out['target_in_links'] = len(src((tgt, 'execute'))); assert out['target_in_links'] == len(keep) + 2
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V242_SAVE', False): save(bp, cpb); out['saved'] = True
cdo = u.get_default_object(bp.generated_class()); out['defaults'] = {'IdleOn': cdo.get_editor_property('SHM242_IdleOn'), 'IdleDB': str(cdo.get_editor_property('SHM242_IdleDB'))}
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('IDLEDB242B ' + json.dumps(out, default=str))
