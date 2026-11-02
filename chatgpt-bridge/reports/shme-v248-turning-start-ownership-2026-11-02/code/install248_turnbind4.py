"""install248_turnbind4.py (editor job, write manifest = ABP base + child; after install248_turnbind3.py): the clip-bound contract on a
turning-start clip is owned by SHM248_TurnStart ALONE. Measured (v248th60 j45_sl2 ts): the ABP's own redirect episode (SHM_RedirectActive)
is alive during the turning start, so after the V2.48 hold released (turn done, T = -90) the V2.28 term (knob AND SHM226_W AND
RedirectActive) kept ClipSpeedOn true through the clip's run-up strides (1.2-1.9 s: 20-31 cm planted-foot drags against the stride /
orientation warping that a free CMC capsule would get). Patch (SHM_Snapshot, SetSHM228_On data input only):
  inTurn = SHM248_On > 0.5 AND name(Phase27_SelectedObject) contains 'Jog_Start_Turn'
  SHM228_On := (NOT inTurn AND old) OR (inTurn AND SHM248_TurnStart AND SHM226_W > 0.3)
Production (knob off) unchanged. Idempotent (variable SHM248_Bind4). builtins.V248_SAVE saves. Prints TURNBIND248D {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
assert 'SHM248_Bind3' in V, 'install248_turnbind3.py first'
if 'SHM248_Bind4' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM248_Bind4', 'bool', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM248_Bind4': True}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    so = [p for p in sn if tid(p).endswith('|SetSHM228_On')]; assert len(so) == 1, so
    old = src((so[0], 'SHM228_On')); assert len(old) == 1, old; disconnect((so[0], 'SHM228_On'))
    inturn = gs.AND(gs.within(gs.get('SHM248_On'), 0.5, 1.0e9), gs.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': gs.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': gs.get('Phase27_SelectedObject')}), 'Substring': 'Jog_Start_Turn', 'bUseCase': False, 'bSearchFromEnd': False}))
    vW = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM226_W'})
    own = gs.AND(gs.get('SHM248_TurnStart'), gs.within(vW, 0.3, 1.0e9))
    connect(gs.OR(gs.AND(gs.NOT(inturn), old[0]), gs.AND(inturn, own)), (so[0], 'SHM228_On')); out['gate'] = old[0][0].rsplit('.', 1)[-1]
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: str(cdo.get_editor_property(k)) for k in ('SHM248_On',)}
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knobs']['SHM248_On'] == '0.0'
if out['ok'] and getattr(builtins, 'V248_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('TURNBIND248D ' + json.dumps(out, default=str))
