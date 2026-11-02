"""install248_turnbind3.py (editor job, write manifest = ABP base + child; after install248_turnbind2.py): the capsule turns the way the
turning-start CLIP turns. The V2.38 heading contract latches Delta = NormalizeAxis(request yaw - actor yaw) on its rising edge and drives
Cmd = Yaw0 + Delta * T / 90; a 180 request has no sign (v248tereal j45_sl2 ts r3: TurnL180 with Delta +180 -> 85 cm slide, LS re-selection).
With the V2.48 Turn curves now SIGNED by the clip (add248_turncurves v2: L clips -90, R clips +90):
  SHM238_Delta := SHM248_TurnStart ? |Delta| : Delta     (wrapped around the existing rising-edge Select)
so a left clip ends at Yaw0 - |Delta|, a right clip at Yaw0 + |Delta| (= the request heading when the clip direction matches it).
Idempotent (variable SHM248_Bind3). builtins.V248_SAVE saves. Prints TURNBIND248C {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
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
assert 'SHM248_ReleaseT' in V and 'SHM238_Delta' in V, 'prerequisites'
if 'SHM248_Bind3' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM248_Bind3', 'bool', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM248_Bind3': True}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    sd = [p for p in sn if tid(p).endswith('|SetSHM238_Delta')]; assert len(sd) == 1, sd
    old = src((sd[0], 'SHM238_Delta')); assert len(old) == 1, old; disconnect((sd[0], 'SHM238_Delta'))
    connect(gs.select(gs.get('SHM248_TurnStart'), gs.pure(M + 'Abs', {'A': old[0]}), old[0]), (sd[0], 'SHM238_Delta')); out['delta'] = old[0][0].rsplit('.', 1)[-1]
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: str(cdo.get_editor_property(k)) for k in ('SHM248_On', 'SHM238_Yaw')}
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knobs']['SHM248_On'] == '0.0'
if out['ok'] and getattr(builtins, 'V248_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('TURNBIND248C ' + json.dumps(out, default=str))
