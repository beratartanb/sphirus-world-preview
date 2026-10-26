"""install_v231_exitpush.py (editor job) - V2.31 authored-reversal exit: the V2.14 post-reversal push window (SHM214_PushRevOn -> SHM211_DB_Push
:= PSD_SHM214_RevPush, push clips that ENTER AT THEIR PUSH STANCE 1.45-1.65 s) was designed for the end of a VENDOR run pivot (no push of its own).
After an AUTHORED reversal clip (SHM226 / SHM231 families: brake + first step + push already in the clip) the window sent every sprint exit
into a second push stance at another foot phase (fin3 / h20 / h60 / h120: 12-42 cm planted slides at the exit, and at 60 / 120 FPS the next
reversal crossfaded from that pose: e29_load 31 / 37 cm). Fix: SHM231_RevAuth = an authored clip was in the pose when the window opened
(latched for the window: RevAuth := (PushRevOn AND RevAuth) OR SHM227_Rev > 0.001); with SHM231_ExitAuth the window does not swap the push
database while RevAuth (DB_Push stays the gait push = PSD_SHM212_GaitPush, the normal jog -> sprint route). Vendor pivots unchanged.
EventGraph: MontTick.then -> Set SHM231_RevAuth -> [PushRevOn AND NOT(ExitAuth AND RevAuth)] branch (the V2.14 swap). Knob SHM231_ExitAuth
default 0 = V2.30 behaviour. Idempotent (SHM231_EPFix). builtins.V231_SAVE saves. Prints EXITPUSH231 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
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
def srcnode(p, pin):
    s = src((p, pin)); return s[0][0] if s else None
if 'SHM231_EPFix' in [str(v) for v in B.list_variables(bp)]:
    out['eg'] = 'already'
else:
    ensure_vars(bp, [('SHM231_ExitAuth', 'float', 'SHM231'), ('SHM231_RevAuth', 'bool', 'SHM231')]); compile_ok(bp)
    eg = pn(graph(bp, 'EventGraph')); ge = G(eg); en = [pn(n) for n in B.find_nodes(obj(eg))]
    br = [p for p in en if 'IfThenElse' in p and 'SHM214_PushRevOn' in tid(srcnode(p, 'Condition') or '')]
    assert len(br) == 1, ('PushRevOn branch', br)
    br = br[0]; ins = src((br, 'execute')); assert len(ins) >= 1, 'branch exec source'
    out['exec_sources'] = [(tid(a_)[-40:], b_) for a_, b_ in ins]
    disconnect((br, 'execute')); disconnect((br, 'Condition'))
    cur = ge.within(ge.get('SHM227_Rev'), 0.001, 1.0e9)
    t0 = ge.set('SHM231_RevAuth', ge.OR(ge.AND(ge.get('SHM214_PushRevOn'), ge.get('SHM231_RevAuth')), cur), ins[0])
    for s_ in ins[1:]: connect(s_, (t0[0], 'execute'))
    connect(t0, (br, 'execute'))
    cond = ge.AND(ge.get('SHM214_PushRevOn'), ge.NOT(ge.AND(ge.within(ge.get('SHM231_ExitAuth'), 0.5, 1.0e9), ge.get('SHM231_RevAuth'))))
    connect(cond, (br, 'Condition'))
    ensure_vars(bp, [('SHM231_EPFix', 'bool', 'SHM231')])
    out['eg'] = {'branch': br.rsplit('.', 1)[-1]}
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: str(cdo.get_editor_property(k)) for k in ('SHM231_ExitAuth', 'SHM214_PushRevWin', 'SHM214_RevTurnMode')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and float(cdo.get_editor_property('SHM231_ExitAuth')) == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V231_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('EXITPUSH231 ' + json.dumps(out, default=str))
