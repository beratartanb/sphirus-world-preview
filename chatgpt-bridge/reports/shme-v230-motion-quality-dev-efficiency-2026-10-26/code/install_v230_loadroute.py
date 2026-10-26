"""install_v230_loadroute.py (editor job) - V2.30 effort -> body: when the short-term effort is high, the authored reversal route searches the
LOADED family (PSD_SHM230L_JogRevBwd / _Fwd: longer brake, later first step, deeper absorb, smaller re-push) instead of the production pair.
EventGraph: after the V2.24 JR database choice (SHM_RedirectDB_JR from SHM224_RevIntent) and before SetSHM221_PivWin, two branches:
LoadedOn & EffortEUse > SHM230_LoadedE & RevIntent 2 -> JR := SHM230_DB_JRBwdL; ... & RevIntent < 1.5 -> JR := SHM230_DB_JRFwdL (lateral
RevIntent 3 untouched). The V2.28 clip-bound capsule then follows the loaded clip's own designed speed (SHM226_V curves). Knob
SHM230_LoadedOn default 0 = V2.29 behaviour. Idempotent (SHM230_LRFix). builtins.V230_SAVE saves. Prints LOADROUTE230 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
V = '/Game/GraceRanger/SHME/Animations/V230L/'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name() in (AP, CP)]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
bwdL = u.load_asset(V + 'PSD_SHM230L_JogRevBwd'); fwdL = u.load_asset(V + 'PSD_SHM230L_JogRevFwd'); assert bwdL and fwdL, 'loaded DBs missing'
bp = u.load_asset(AP)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
if 'SHM230_LRFix' in [str(v) for v in B.list_variables(bp)]:
    out['eg'] = 'already'
else:
    DBC = u.PoseSearchDatabase.static_class()
    ensure_vars(bp, [('SHM230_LoadedOn', 'float', 'SHM230'), ('SHM230_LoadedE', 'float', 'SHM230'), ('SHM230_DB_JRBwdL', DBC, 'SHM230'), ('SHM230_DB_JRFwdL', DBC, 'SHM230')]); compile_ok(bp)
    set_defaults(bp, {'SHM230_LoadedE': 0.45, 'SHM230_DB_JRBwdL': bwdL, 'SHM230_DB_JRFwdL': fwdL}); compile_ok(bp)
    eg = pn(graph(bp, 'EventGraph')); ge = G(eg); en = [pn(n) for n in B.find_nodes(obj(eg))]
    piv = [p for p in en if 'SetSHM221_PivWin' in tid(p)]; assert len(piv) == 1, piv
    ins = src((piv[0], 'execute'))
    jr_sets = [s_ for s_ in ins if 'SetSHM_RedirectDB_JR' in tid(s_[0])]
    assert len(ins) == 3 and len(jr_sets) == 2, ('PivWin exec sources changed', [(tid(a)[-30:], b) for a, b in ins])
    # own SHME component getter (EventGraph's first GetComponentByClass is another class); class pin = path string (V2.28 trap)
    pawn = ge.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    cget = ge.pure('/Script/Engine.Actor:GetComponentByClass', {'self': pawn, 'ComponentClass': COMP})
    ct = cget if isinstance(cget, tuple) else (cget, 'ReturnValue')
    disconnect((piv[0], 'execute'))
    # a sequence entry: one branch node fed by the three old sources
    loaded = ge.AND(ge.within(ge.get('SHM230_LoadedOn'), 0.5, 1.0e9), ge.within(ge.get('EffortEUse', COMP, ct), ge.get('SHM230_LoadedE'), 1.0e9))
    ri = ge.get('SHM224_RevIntent')
    y1, n1 = ge.branch(ge.AND(loaded, ge.within(ri, 1.5, 2.5)), ins[0])
    for s_ in ins[1:]: connect(s_, (y1[0], 'execute'))
    t1 = ge.set('SHM_RedirectDB_JR', ge.get('SHM230_DB_JRBwdL'), y1)
    y2, n2 = ge.branch(ge.AND(loaded, ge.within(ri, -1.0, 1.5)), n1)
    t2 = ge.set('SHM_RedirectDB_JR', ge.get('SHM230_DB_JRFwdL'), y2)
    for s_ in (t1, t2, n2): connect(s_, (piv[0], 'execute'))
    ensure_vars(bp, [('SHM230_LRFix', 'bool', 'SHM230')])
    out['eg'] = 'wired'
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: str(cdo.get_editor_property(k)) for k in ('SHM230_LoadedOn', 'SHM230_LoadedE', 'SHM230_DB_JRBwdL', 'SHM230_DB_JRFwdL')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and float(cdo.get_editor_property('SHM230_LoadedOn')) == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V230_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('LOADROUTE230 ' + json.dumps(out, default=str))
