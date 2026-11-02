"""install248_turnbind.py (editor job, write manifest = ABP base + child; after install248_turnstart.py and add248_turncurves.py):
V2.48 step 2 - the turning start owns the capsule while it plays.
  1. SHM_Snapshot: SHM228_On (V2.28 clip-speed contract gate) := old OR (SHM248_TurnStart AND SHM226_W > 0.3): while a turning-start clip
     carrying the V2.48 curves is in the pose, the capsule speed follows the clip root speed (ClipSpeed / ClipSpeedOn -> BP_GR_Player) and,
     through SHM238_On (= SHM238_Yaw knob AND SHM238_W AND SHM228_On), the capsule heading follows the normalised root yaw progress
     (Yaw0 + Delta * Turn/90 -> ends at the requested heading). No new pawn code: the V2.28/V2.38 movement-side writers are production.
  2. SHM_Snapshot: SHM248_TurnStart hold := old OR (SHM248_TurnStart AND name(CurrentSelectedDatabase) contains 'SHM248_JogStartT'):
     the route and the contract hold exactly while Motion Matching is inside the turning-start database (the 1.0 s timer alone let the
     body-relative test drop at 0.6 s).
  3. Update_MotionMatching: the LS lateral-start route (InRange 65-115 on the body-relative direction, K2Node_CallFunction_60) is blocked
     while SHM248_TurnStart holds: Value := Select(SHM248_TurnStart, 999, old)  (v248tsreal r2/r3: LS_CoreLateralStart hijacked the turn at
     0.63 s when the turning body passed through the lateral sector).
All under the SHM248_On knob (TurnStart is false with the knob off) -> production unchanged. Idempotent (marker variable SHM248_Bind).
builtins.V248_SAVE saves. Prints TURNBIND248 {...}."""
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
assert 'SHM248_TurnStart' in V and 'SHM228_On' in V and 'SHM238_On' in V, 'prerequisites (V2.28, V2.38, install248_turnstart)'
if 'SHM248_Bind' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM248_Bind', 'bool', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM248_Bind': True}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    # 1. contract gate
    so = [p for p in sn if tid(p).endswith('|SetSHM228_On')]; assert len(so) == 1, so
    old = src((so[0], 'SHM228_On')); assert len(old) == 1, old; disconnect((so[0], 'SHM228_On'))
    vW = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM226_W'})
    term = gs.AND(gs.get('SHM248_TurnStart'), gs.within(vW, 0.3, 1.0e9))
    connect(gs.OR(old[0], term), (so[0], 'SHM228_On')); out['gate'] = old[0][0].rsplit('.', 1)[-1]
    # 2. hold while inside the turning-start database
    st = [p for p in sn if tid(p).endswith('|SetSHM248_TurnStart')]; assert len(st) == 1, st
    old2 = src((st[0], 'SHM248_TurnStart')); assert len(old2) == 1, old2; disconnect((st[0], 'SHM248_TurnStart'))
    indb = gs.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': gs.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': gs.get('CurrentSelectedDatabase')}), 'Substring': 'SHM248_JogStartT', 'bUseCase': False, 'bSearchFromEnd': False})
    connect(gs.OR(old2[0], gs.AND(gs.get('SHM248_TurnStart'), indb)), (st[0], 'SHM248_TurnStart')); out['hold'] = True
    # 3. LS lateral route blocked during the hold
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
    cf60 = nodes['K2Node_CallFunction_60']
    assert any(q.name == 'Min' and abs(float(str(q.value)) - 65.0) < 1e-3 for q in info(cf60).input_pins), 'not the LS lateral InRange node'
    old3 = src((cf60, 'Value')); assert len(old3) == 1, old3; disconnect((cf60, 'Value'))
    connect(g.select(g.get('SHM248_TurnStart'), 999.0, old3[0]), (cf60, 'Value')); out['ls_block'] = old3[0][0].rsplit('.', 1)[-1]
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: str(cdo.get_editor_property(k)) for k in ('SHM248_On', 'SHM228_ClipSpeed', 'SHM238_Yaw')}
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knobs']['SHM248_On'] == '0.0'
if out['ok'] and getattr(builtins, 'V248_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('TURNBIND248 ' + json.dumps(out, default=str))
