"""install253_walkhold.py (editor job, write manifest = ABP base + child): V2.53 REQUEST-FRAME HOLD (knob SHM253_WalkHold, default 0).
The V2.53 walk entry (install253_walkentry.py: search the start-transfer database on the request frame) removed the stray vendor sample from
every walk start from rest (stance ball travel 16-24 -> 0.2-4 cm) but overrode the component's tap gate: for a 0.12 s tap the family route
stays 0 for ~8 frames on purpose (tap vocabulary), the request-frame start clip then cut to the release micro-step -> head pop 62 -> 88.
Hold variant: on the REQUEST FRAME ONLY (GroundSpeed < 5 cm/s = the first frame(s) of motion: 1 frame at 30/60, 2-3 at 120, none at 20 FPS; GetWorldDeltaSeconds is not thread safe here) Motion Matching searches
the database it is already in (CurrentSelectedDatabase, InterruptMode DoNotInterrupt) - the standing pose simply continues one frame, no
stray sample enters the blend stack, and the next frame the normal route (start transfer, tap micro-step, ...) decides as before.
Inserted in front of the V2.53 walk entry branch on the false path of the V2.49 entry branch IfThenElse_84. Idempotent (SHM253_WalkHold).
builtins.V253_SAVE saves. Prints WALKHOLD253 {...}."""
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
def db_var_of(p):
    s_ = src((p, 'Database'))
    return str(info(s_[0][0]).type_id).rsplit('|', 1)[-1] if s_ else ''
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
need = ['SHM253_WalkEntry', 'SHM251_StartEntry', 'SHM249_RestSpeed', 'SHM_StartGait', 'SHM_StartTransferDB_L', 'SHM_StartTransferDB_R', 'GroundSpeed', 'HasAcceleration', 'SHM_StartSide']
out['missing'] = [v for v in need if v not in V]; assert not out['missing'], out['missing']
if 'SHM253_WalkHold' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM253_WalkHold', 'float', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM253_WalkHold': 0.0}); compile_ok(bp)
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
    br84 = N['K2Node_IfThenElse_84']; assert 'IfThenElse' in br84
    old_else = succ(br84, 'else'); assert len(old_else) == 1, old_else
    disconnect((old_else[0][0], old_else[0][1]))
    dbn = g.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': g.get('CurrentSelectedDatabase')})
    notWalkStart = g.NOT(g.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': dbn, 'Substring': 'StartTransfer', 'bUseCase': False, 'bSearchFromEnd': False}))
    cond = g.AND(g.AND(g.within(g.get('SHM253_WalkHold'), 0.5, 1.0e9), g.within(g.get('GroundSpeed'), -1.0, 5.0)),
                 g.AND(g.AND(g.get('HasAcceleration'), g.within(g.get('SHM_StartGait'), -0.5, 0.5)), notWalkStart))
    bt, bf = g.branch(cond, (br84, 'else'))
    connect(bf, old_else[0])
    ref = [p for p in N.values() if 'SetDatabaseToSearch' in tid(p) and db_var_of(p).endswith('SHM_StartTransferDB_L')][0]; mm = src((ref, 'MotionMatchingNode'))[0]
    s = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(bt, (s, 'execute'))
    connect(mm, (s, 'MotionMatchingNode')); connect(g.get('CurrentSelectedDatabase'), (s, 'Database')); arg(s, 'InterruptMode', 'DoNotInterrupt')
    out['entry'] = {'else_was': old_else[0][0].rsplit('.', 1)[-1]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM253_WalkHold'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V253_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('WALKHOLD253 ' + json.dumps(out, default=str))
