"""install254_v4.py (editor job, write manifest = ABP base + child): V2.54 intent cancel leaves the turn-around clip at once.
Measured (v254f60 s54_tap rvc): with the cancel (yaw + clip-speed contracts off) the capsule kept its sprint (min 419 cm/s) but Motion
Matching kept PLAYING SHM254_Rev_R_T186 for 1.45 s (brake / pivot pose on a 488 cm/s capsule): the old flow searches with DoNotInterrupt
and the turn-around database's continuing-pose bias (-25) keeps the clip's own continuation cheapest.
Patch (Update_MotionMatching entry, before the V2.54 hold branch):
  Branch(SHM254_Turn > 0.5 AND SHM254_Cancel AND SHM228_DesV > 50 AND SHM28_Speed > SHM254_CancelMinV AND DB name contains 'SHM254')
    true  -> SetDatabaseToSearch(PSD_SHM233_SprintCalm, InterruptOnDatabaseChangeAndInvalidateContinuingPose)  (the clips' own loop)
    false -> the V2.54 hold branch / old flow.
A release (no intent) or a slow cancel keeps the old flow (stop / start families). Knob SHM254_CancelMinV (250). Idempotent (variable
SHM254_CancelMinV). builtins.V254_SAVE saves. Prints V4254 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
LOOPDB = '/Game/GraceRanger/SHME/Animations/V233/SprintCalm/PSD_SHM233_SprintCalm'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def succ(p, pin='then'):
    return [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for o in info(p).output_pins if str(o.name) == pin for q in o.connected_pins]
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
assert u.EditorAssetLibrary.does_asset_exist(LOOPDB), LOOPDB
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
assert 'SHM254_V3' in V and 'SHM28_Speed' in V and 'SHM228_DesV' in V, 'install254_v3 first / speed vars'
if 'SHM254_CancelMinV' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM254_CancelMinV', 'float', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM254_CancelMinV': 250.0}); compile_ok(bp)
    mg = pn(graph(bp, 'Update_MotionMatching')); g = G(mg); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(mg))}
    entry = N['K2Node_FunctionEntry_0']; first = succ(entry); assert len(first) == 1 and 'IfThenElse' in first[0][0], first
    ref = [p for p in N.values() if 'SetDatabaseToSearch' in tid(p) and src((p, 'MotionMatchingNode'))][0]; mm = src((ref, 'MotionMatchingNode'))[0]
    disconnect((first[0][0], first[0][1]))
    dbn = g.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': g.get('CurrentSelectedDatabase')})
    mine = g.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': dbn, 'Substring': 'SHM254', 'bUseCase': False, 'bSearchFromEnd': False})
    cond = g.AND(g.AND(g.within(g.get('SHM254_Turn'), 0.5, 1.0e9), g.get('SHM254_Cancel')),
                 g.AND(g.AND(g.within(g.get('SHM228_DesV'), 50.0, 1.0e9), g.within(g.get('SHM28_Speed'), g.get('SHM254_CancelMinV'), 1.0e9)), mine))
    bt, bf = g.branch(cond, (entry, 'then'))
    connect(bf, first[0])
    s = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(bt, (s, 'execute'))
    connect(mm, (s, 'MotionMatchingNode')); arg(s, 'Database', LOOPDB + '.' + LOOPDB.split('/')[-1]); arg(s, 'InterruptMode', 'InterruptOnDatabaseChangeAndInvalidateContinuingPose')
    out['wired'] = {'before': first[0][0].rsplit('.', 1)[-1], 'db': str(info(s).input_pins[[p.name for p in info(s).input_pins].index('Database')].value)[:90]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM254_Turn'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V254_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('V4254 ' + json.dumps(out, default=str))
