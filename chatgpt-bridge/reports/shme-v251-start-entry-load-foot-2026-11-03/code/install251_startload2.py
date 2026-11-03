"""install251_startload2.py (editor job, write manifest = ABP base + child): V2.51 load-aware start foot, step 2 - the RELAXED leg.
The rawSide input of the start latch (patched by install251_startload.py into Select(gate, byCOMLoad, rawSide)) is wrapped once more:
  idleSup := GetCurveValue(SHM251_IdleSupport)   (weighted idle clips, add251_idlesupport.py; 0 on every other clip)
  side    := (SHM251_StartLoad > 0.5 AND idleSup > 0.5) ? 1 (right foot is free -> it steps)
           : (SHM251_StartLoad > 0.5 AND idleSup < -0.5) ? 0 : the step-1 value.
Idempotent (marker variable SHM251_RelaxedLeg). builtins.V251_SAVE saves. Prints STARTLOAD2_251 {...}."""
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
assert 'SHM251_StartLoad' in V, 'install251_startload.py first'
if 'SHM251_RelaxedLeg' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM251_RelaxedLeg', 'bool', 'SHM')]); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    ss = [p for p in sn if tid(p).endswith('|SetSHM_StartSideL')]; assert len(ss) == 1, ss
    sel = src((ss[0], 'SHM_StartSideL')); assert len(sel) == 1, sel; selp = sel[0][0]
    cur = src((selp, 'B')); assert len(cur) == 1, cur
    disconnect((selp, 'B'))
    on = gs.within(gs.get('SHM251_StartLoad'), 0.5, 1.0e9)
    sup = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM251_IdleSupport'})
    side = gs.select(gs.AND(on, gs.within(sup, 0.5, 1.0e9)), 1.0, gs.select(gs.AND(on, gs.within(sup, -1.0e9, -0.5)), 0.0, cur[0]))
    connect(side, (selp, 'B'))
    out['wired'] = {'select': selp.rsplit('.', 1)[-1], 'wrapped': cur[0][0].rsplit('.', 1)[-1]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V251_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('STARTLOAD2_251 ' + json.dumps(out, default=str))
