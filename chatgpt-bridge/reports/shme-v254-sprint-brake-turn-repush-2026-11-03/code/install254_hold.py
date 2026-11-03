"""install254_hold.py (editor job, write manifest = ABP base + child): V2.54 ROUTE HOLD for the planned turn-around (knob SHM254_Turn).
Measured (v254b60 s54_rev rv): the SHM254 sprint turn-around clip was entered on the request frame, but at +0.73 s (speed below the
sprint class) the family route re-searched the JOG reversal database (SHM236_JogRev_F_B, back-run) and at +1.67 s (re-push) the push
link database (SHM218_W2S, upright): the plan lost its own body mid-action.
Patch (Update_MotionMatching entry, the V2.49 precedent: one branch at the entry, nothing else this frame):
  Branch(SHM254_Turn > 0.5 AND curve SHM254_Own > 0.3 AND name(CurrentSelectedDatabase) contains 'SHM254')
    true  -> SetDatabaseToSearch(CurrentSelectedDatabase, DoNotInterrupt)   (the plan keeps its database through brake, pivot and re-push)
    false -> the old flow.
Idempotent (variable SHM254_Hold). builtins.V254_SAVE saves. Prints HOLD254 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
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
assert 'SHM254_Turn' in V, 'install254_turn.py first'
if 'SHM254_Hold' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM254_Hold', 'bool', 'SHM')]); compile_ok(bp)
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
    entry = N['K2Node_FunctionEntry_0']; first = succ(entry); assert len(first) == 1, first
    ref = [p for p in N.values() if 'SetDatabaseToSearch' in tid(p) and src((p, 'MotionMatchingNode'))][0]; mm = src((ref, 'MotionMatchingNode'))[0]
    disconnect((first[0][0], first[0][1]))
    dbn = g.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': g.get('CurrentSelectedDatabase')})
    mine = g.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': dbn, 'Substring': 'SHM254', 'bUseCase': False, 'bSearchFromEnd': False})
    own = g.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM254_Own'})
    cond = g.AND(g.AND(g.within(g.get('SHM254_Turn'), 0.5, 1.0e9), g.within(own, 0.3, 1.0e9)), mine)
    bt, bf = g.branch(cond, (entry, 'then'))
    connect(bf, first[0])
    s = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(bt, (s, 'execute'))
    connect(mm, (s, 'MotionMatchingNode')); connect(g.get('CurrentSelectedDatabase'), (s, 'Database')); arg(s, 'InterruptMode', 'DoNotInterrupt')
    out['wired'] = {'first_was': first[0][0].rsplit('.', 1)[-1]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM254_Turn'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V254_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('HOLD254 ' + json.dumps(out, default=str))
