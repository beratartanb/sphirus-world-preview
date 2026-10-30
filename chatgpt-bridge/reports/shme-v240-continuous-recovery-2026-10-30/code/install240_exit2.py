"""install240_exit2.py (editor job) - V2.40: the takeover exit enters the component's OWN exploration state (after install240_exit).
Measured (v240d30_j39_lr_tk): writing LocoYaw / LocoState at the plan end did nothing - the component recomputes its body-frame state
every tick (shm_src.py V2.34 rule): state 0 = the camera input frame (a held lateral input then strafes), state 1 = exploration (frame =
the input's world direction, 'the body decides to walk that way and the camera follows'), and a RUNNING exploration is kept while the
input does not jump (LocoExplore AND |input - LocoInYaw| < LocoExploreKeep). A physical takeover IS that decision, so the exit sets
the state the rule keeps: component LocoExplore := true, LocoInYaw := the input's world yaw (DesiredVelocity), LocoYaw := actor yaw.
Idempotent (marker SHM240_Exit2). builtins.V240_SAVE saves. Prints EXIT2_240 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {'reloaded': names}
bp = u.load_asset(AP)
if 'SHM240_Exit2' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM240_Exit2', 'bool', 'SHM240')]); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    ls_ = [p for p in sn if tid(p).endswith('SetLocoState')]; assert len(ls_) == 1, len(ls_)
    nx = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (ls_[0], 'then') in src((p, 'execute'))]; assert len(nx) == 1
    disconnect((nx[0], 'execute'))
    db = gs.fn('BreakVector', {'InVec': gs.get('DesiredVelocity', COMP, ct)})
    t = gs.set('LocoExplore', True, (ls_[0], 'then'), COMP, ct)
    t = gs.set('LocoInYaw', gs.pure(M + 'DegAtan2', {'Y': (db, 'Y'), 'X': (db, 'X')}), t, COMP, ct)
    connect(t, (nx[0], 'execute')); out['patch'] = 'exit -> component exploration (LocoExplore, LocoInYaw)'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V240_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('EXIT2_240 ' + json.dumps(out, default=str))
