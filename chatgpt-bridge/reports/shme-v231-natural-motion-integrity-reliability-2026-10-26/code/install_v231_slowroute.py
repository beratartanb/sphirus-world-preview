"""install_v231_slowroute.py (editor job) - V2.31 low-speed reversal route: when the component's reversal episode STARTED slow (RedirectSpeed0 =
the speed latched at the episode start, < SHM231_SlowV), the authored reversal route searches the LOW-SPEED family (PSD_SHM231S_SlowRevBwd /
_Fwd: walk entry pose, short brake, first step, push) instead of the jog pair. Latched -> no database change inside an episode.
EventGraph: after the V2.24 JR choice and the V2.30 loaded branches, before SetSHM221_PivWin, two branches:
SlowOn & RedirectSpeed0 < SlowV & RevIntent 2 -> JR := SHM231_DB_JRBwdS; ... & RevIntent < 1.5 -> JR := SHM231_DB_JRFwdS (lateral 3 untouched).
Knob SHM231_SlowOn default 0 = V2.30 behaviour. Idempotent (SHM231_SRFix). builtins.V231_SAVE saves. Prints SLOWROUTE231 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
V = '/Game/GraceRanger/SHME/Animations/V231/'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name() in (AP, CP)]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
bwdS = u.load_asset(V + 'PSD_SHM231S_SlowRevBwd'); fwdS = u.load_asset(V + 'PSD_SHM231S_SlowRevFwd'); assert bwdS and fwdS, 'slow DBs missing'
bp = u.load_asset(AP)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
if 'SHM231_SRFix' in [str(v) for v in B.list_variables(bp)]:
    out['eg'] = 'already'
else:
    DBC = u.PoseSearchDatabase.static_class()
    ensure_vars(bp, [('SHM231_SlowOn', 'float', 'SHM231'), ('SHM231_SlowV', 'float', 'SHM231'), ('SHM231_DB_JRBwdS', DBC, 'SHM231'), ('SHM231_DB_JRFwdS', DBC, 'SHM231')]); compile_ok(bp)
    set_defaults(bp, {'SHM231_SlowV': 90.0, 'SHM231_DB_JRBwdS': bwdS, 'SHM231_DB_JRFwdS': fwdS}); compile_ok(bp)
    eg = pn(graph(bp, 'EventGraph')); ge = G(eg); en = [pn(n) for n in B.find_nodes(obj(eg))]
    piv = [p for p in en if 'SetSHM221_PivWin' in tid(p)]; assert len(piv) == 1, piv
    ins = src((piv[0], 'execute'))
    assert len(ins) == 3, ('PivWin exec sources changed', [(tid(a)[-40:], b) for a, b in ins])
    pawn = ge.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    cget = ge.pure('/Script/Engine.Actor:GetComponentByClass', {'self': pawn, 'ComponentClass': COMP})
    ct = cget if isinstance(cget, tuple) else (cget, 'ReturnValue')
    disconnect((piv[0], 'execute'))
    slow = ge.AND(ge.within(ge.get('SHM231_SlowOn'), 0.5, 1.0e9), ge.within(ge.get('RedirectSpeed0', COMP, ct), -1.0, ge.get('SHM231_SlowV')))
    ri = ge.get('SHM224_RevIntent')
    y1, n1 = ge.branch(ge.AND(slow, ge.within(ri, 1.5, 2.5)), ins[0])
    for s_ in ins[1:]: connect(s_, (y1[0], 'execute'))
    t1 = ge.set('SHM_RedirectDB_JR', ge.get('SHM231_DB_JRBwdS'), y1)
    y2, n2 = ge.branch(ge.AND(slow, ge.within(ri, -1.0, 1.5)), n1)
    t2 = ge.set('SHM_RedirectDB_JR', ge.get('SHM231_DB_JRFwdS'), y2)
    for s_ in (t1, t2, n2): connect(s_, (piv[0], 'execute'))
    ensure_vars(bp, [('SHM231_SRFix', 'bool', 'SHM231')])
    out['eg'] = 'wired'
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: str(cdo.get_editor_property(k)) for k in ('SHM231_SlowOn', 'SHM231_SlowV', 'SHM231_DB_JRBwdS', 'SHM231_DB_JRFwdS')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and float(cdo.get_editor_property('SHM231_SlowOn')) == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V231_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('SLOWROUTE231 ' + json.dumps(out, default=str))
