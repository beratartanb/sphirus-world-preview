"""install_v231_exitpush_b.py (editor job) - revision of install_v231_exitpush.py (A1: suppressing the V2.14 swap left SHM212_DB_PushStand =
PSD_RR_Start, so the post-reversal push route served a STAND START clip mid-stride: 14-24 cm). After an AUTHORED reversal the body is in the
jog loop at ~300 cm/s with sprint requested = exactly the jog -> sprint push (the V2.17/V2.30 J2S links in PSD_SHM218_JogPush). New branch
right after Set SHM231_RevAuth: PushRevOn AND ExitAuth AND RevAuth -> SHM211_DB_Push := SHM231_DB_AuthPush, SHM212_DB_PushStand :=
SHM231_DB_AuthPush -> the montage join; else -> the V2.14 branch (unchanged, its condition keeps NOT(ExitAuth AND RevAuth)).
Knob SHM231_ExitAuth (0 = V2.30). Idempotent (SHM231_EPFixB). builtins.V231_SAVE saves. Prints EXITPUSH231B {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
JP = '/Game/GraceRanger/SHME/Animations/V218/PSD_SHM218_JogPush'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name() in (AP, CP)]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
jp = u.load_asset(JP); assert jp, JP
bp = u.load_asset(AP)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def srcnode(p, pin):
    s = src((p, pin)); return s[0][0] if s else None
vs = [str(v) for v in B.list_variables(bp)]
if 'SHM231_EPFixB' in vs:
    out['eg'] = 'already'
else:
    assert 'SHM231_EPFix' in vs, 'exitpush A not installed'
    DBC = u.PoseSearchDatabase.static_class()
    ensure_vars(bp, [('SHM231_DB_AuthPush', DBC, 'SHM231')]); compile_ok(bp); set_defaults(bp, {'SHM231_DB_AuthPush': jp}); compile_ok(bp)
    eg = pn(graph(bp, 'EventGraph')); ge = G(eg); en = [pn(n) for n in B.find_nodes(obj(eg))]
    ra = [p for p in en if tid(p).endswith('SetSHM231_RevAuth')]; assert len(ra) == 1, ra
    rev = [p for p in en if tid(p).endswith('SetSHM211_DB_Push') and 'SHM214_DB_RevPush' in tid(srcnode(p, 'SHM211_DB_Push') or '')]
    assert len(rev) == 1, ('V2.14 rev set', rev)
    br = [srcnode(rev[0], 'execute')]; assert br[0] and 'IfThenElse' in br[0], ('V2.14 branch', br)
    out['v214_branch'] = br[0].rsplit('.', 1)[-1]   # = the branch exitpush A rewired (K2Node_IfThenElse_8 on 2026-10-26)
    joins = [p for p in en if 'IfThenElse' in p and 'SHM213_MontStartNow' in tid(srcnode(p, 'Condition') or '')]; assert len(joins) == 1, joins
    disconnect((br[0], 'execute'))
    c = ge.AND(ge.get('SHM214_PushRevOn'), ge.AND(ge.within(ge.get('SHM231_ExitAuth'), 0.5, 1.0e9), ge.get('SHM231_RevAuth')))
    y, n = ge.branch(c, (ra[0], 'then'))
    connect(n, (br[0], 'execute'))
    t1 = ge.set('SHM211_DB_Push', ge.get('SHM231_DB_AuthPush'), y)
    t2 = ge.set('SHM212_DB_PushStand', ge.get('SHM231_DB_AuthPush'), t1)
    connect(t2, (joins[0], 'execute'))
    ensure_vars(bp, [('SHM231_EPFixB', 'bool', 'SHM231')])
    out['eg'] = {'branch': y[0].rsplit('.', 1)[-1], 'join': joins[0].rsplit('.', 1)[-1]}
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class())
out['knobs'] = {k: str(cdo.get_editor_property(k))[:90] for k in ('SHM231_ExitAuth', 'SHM231_DB_AuthPush')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and float(cdo.get_editor_property('SHM231_ExitAuth')) == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V231_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('EXITPUSH231B ' + json.dumps(out, default=str))
