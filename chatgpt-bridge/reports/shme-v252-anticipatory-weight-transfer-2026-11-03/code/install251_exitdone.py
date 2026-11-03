"""install251_exitdone.py (editor job, write manifest = ABP base + child): V2.51 release the V2.49 turning-start owner where the crop stops
being a Motion Matching candidate (curve SHM251_Exit from add251_exitcurve.py, last 0.32 s of each crop). Knob SHM251_ExitOn (default 0 =
production unchanged). Patch (SHM_Snapshot): SetSHM249_TurnDone value := old OR (SHM251_ExitOn > 0.5 AND GetCurveValue(SHM251_Exit) > 0.5).
TurnDone ends the hold, the database change gives ONE transition; the remaining yaw (< 6 deg) is closed by the SHM251_YawSlew hand-over.
Idempotent (variable SHM251_ExitOn). builtins.V251_SAVE saves. Prints EXITDONE251 {...}."""
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
assert 'SHM249_TurnDone' in V
if 'SHM251_ExitOn' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM251_ExitOn', 'float', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM251_ExitOn': 0.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    st = [p for p in sn if tid(p).endswith('|SetSHM249_TurnDone')]; assert len(st) == 1, st
    old = src((st[0], 'SHM249_TurnDone')); assert len(old) == 1, old
    disconnect((st[0], 'SHM249_TurnDone'))
    ex = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM251_Exit'})
    connect(gs.OR(old[0], gs.AND(gs.within(gs.get('SHM251_ExitOn'), 0.5, 1.0e9), gs.within(ex, 0.5, 1.0e9))), (st[0], 'SHM249_TurnDone'))
    out['wired'] = st[0].rsplit('.', 1)[-1]
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM251_ExitOn'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V251_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('EXITDONE251 ' + json.dumps(out, default=str))
