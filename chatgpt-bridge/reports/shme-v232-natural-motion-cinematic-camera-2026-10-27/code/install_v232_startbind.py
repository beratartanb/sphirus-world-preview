"""install_v232_startbind.py (editor job) - V2.32 C, ABP side: the V2.28 clip-bound capsule contract (SHM_Snapshot: SHM228_On -> component
ClipSpeedOn, ClipSpeed = the clip's designed speed; BP_GR_Player applies it) gets a START term: SHM228_On = existing OR (SHM232_StartBind >
0.5 AND curve SHM232_SW > 0.3 (an owned start clip carrying the witness is in the pose) AND component HasIntent AND the intent points
backward along the body (dot(Facing, DesiredDir) < -0.7: the player still asks for the backward start; any other request releases the
capsule to the CMC the same frame). Knob SHM232_StartBind default 0 = production unchanged. Idempotent (SHM232_StartBind getter in the
graph). V2.31 exec rule: the Set node's data input only is rewired (no exec change). builtins.V232_SAVE saves. Prints SB232 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
bp = u.load_asset(AP); out = {}
ensure_vars(bp, [('SHM232_StartBind', 'float', 'SHM232')]); compile_ok(bp)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any(tid(p).endswith('|GetSHM232_StartBind') for p in sn): out['snapshot'] = 'already'
else:
    son = [p for p in sn if tid(p).endswith('SetSHM228_On')]; assert len(son) == 1, son
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'
    ct = (comp[0], 'ReturnValue')
    old = src((son[0], 'SHM228_On')); assert len(old) == 1, old
    sw = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM232_SW'})
    back = gs.within(gs.pure(M + 'Dot_VectorVector', {'A': gs.get('Facing', COMP, ct), 'B': gs.get('DesiredDir', COMP, ct)}), -1.0e9, -0.7)
    term = gs.AND(gs.AND(gs.within(gs.get('SHM232_StartBind'), 0.5, 1.0e9), gs.within(sw, 0.3, 1.0e9)), gs.AND(gs.get('HasIntent', COMP, ct), back))
    disconnect((son[0], 'SHM228_On')); connect(gs.OR(old[0], term), (son[0], 'SHM228_On'))
    out['snapshot'] = 'wired'; out['on_src'] = [(a.rsplit('.', 1)[-1], tid(a).split('|')[-1]) for a, b in src((son[0], 'SHM228_On'))]
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = float(cdo.get_editor_property('SHM232_StartBind'))
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and out['knob'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V232_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('SB232 ' + json.dumps(out, default=str))
