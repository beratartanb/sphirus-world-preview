"""install_v231_tipend.py (editor job) - V2.31 slope sprint / camera-180 restart (V2.30 OPEN item C, head pop 175 m/s2): on the frame the
turn-in-place montage ends (ABP SHM_TurnEnd) with the request already back but the body still at rest (HasVelocity false), the ABP still
holds LAST frame's family (0: the component's start family 4 arrives one frame later) -> the original chooser served
PSD_Dense_Stand_Sprint_Pivots and MM played ONE frame of the vendor sprint-turn tail (M_Neutral_Sprint_Turn_L_180_Rfoot @1.10, a crouched
turn exit) before the start database: head 29 cm back / 18 cm sideways / 16 cm down in 0.1 s. A pivot needs momentum - at rest it is never
the right family. Fix: Update_MotionMatching entry -> Branch(SHM231_TipEndHold AND SHM_TurnEnd AND NOT HasVelocity): true ->
SetDatabaseToSearch(CurrentSelectedDatabase = the TIP database, DoNotInterrupt) and return (the standing turn pose continues one frame, the
start route takes over on the next); false -> the unchanged flow. Knob default 0. Idempotent (SHM231_TEFix). builtins.V231_SAVE saves.
Prints TIPEND231 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name() in (AP, CP)]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
bp = u.load_asset(AP)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
if 'SHM231_TEFix' in [str(v) for v in B.list_variables(bp)]:
    out['fn'] = 'already'
else:
    ensure_vars(bp, [('SHM231_TipEndHold', 'float', 'SHM231')]); compile_ok(bp)
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp)
    nodes = [pn(n) for n in B.find_nodes(obj(gp))]
    entry = [p for p in nodes if p.rsplit('.', 1)[-1].startswith('K2Node_FunctionEntry')]; assert len(entry) == 1, entry
    entry = entry[0]
    mmn = [p for p in nodes if 'converttomotionmatchingnode' in tid(p).lower()]
    assert mmn, ('no ConvertToMotionMatchingNode', [tid(p)[-40:] for p in nodes][:60])
    mm = (mmn[0], 'MotionMatchingNode') if any(q.name == 'MotionMatchingNode' for q in info(mmn[0]).output_pins) else (mmn[0], info(mmn[0]).output_pins[-1].name)
    firsts = [p for p in nodes if any(q.name == 'execute' for q in info(p).input_pins) and (entry, 'then') in src((p, 'execute'))]
    assert len(firsts) == 1, ('entry successors', firsts)
    out['first'] = tid(firsts[0])[-50:]; out['mm'] = [mm[0].rsplit('.', 1)[-1], mm[1]]
    disconnect((firsts[0], 'execute'))
    c = g.AND(g.within(g.get('SHM231_TipEndHold'), 0.5, 1.0e9), g.AND(g.get('SHM_TurnEnd'), g.NOT(g.get('HasVelocity'))))
    yt, ye = g.branch(c, (entry, 'then'))
    connect(ye, (firsts[0], 'execute'))
    s1 = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(yt, (s1, 'execute')); connect(mm, (s1, 'MotionMatchingNode'))
    connect(g.get('CurrentSelectedDatabase'), (s1, 'Database')); arg(s1, 'InterruptMode', 'DoNotInterrupt')
    ensure_vars(bp, [('SHM231_TEFix', 'bool', 'SHM231')])
    out['fn'] = {'first_exec_in': [(a.rsplit('.', 1)[-1], b) for a, b in src((firsts[0], 'execute'))]}
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class())
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and float(cdo.get_editor_property('SHM231_TipEndHold')) == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V231_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('TIPEND231 ' + json.dumps(out, default=str))
