"""install239_blend.py (editor job) - V2.39: a takeover entry blends in short (after install239_par).
Measured (v239m/n j39_rl*): the takeover asset became the reported selection ~0.26 s after the request with the takeover clip time
= request time + 0.26 (rl: request 0.47 -> shown at 6.13 with clip time 0.73): the MM node blends every new selection over BlendTime 0.5 s
(HermiteCubic, MaxActiveBlends 4) and the old cut kept the larger weight. A takeover entry is pose-identical to the playing cut frame
(prefix clips), so the long blend only delays the physical takeover (it landed one contact late, K3 instead of K2).
Patch: AnimGraph MM BlendTime := Select(SHM239_Own > 0.5 AND SHM239_TkOn, SHM239_TkBlend (0.05 s), <existing 0.5>).
Idempotent (marker SHM239_TkBlend). builtins.V239_SAVE saves. Prints BLEND239 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': names}
bp = u.load_asset(AP)
if 'SHM239_TkBlend' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM239_TkBlend', 'float', 'SHM239')]); compile_ok(bp); set_defaults(bp, {'SHM239_TkBlend': 0.05}); compile_ok(bp)
    ag = pn(graph(bp, 'AnimGraph')); ga = G(ag)
    mm = [pn(n) for n in B.find_nodes(obj(ag)) if n.get_class().get_name() == 'AnimGraphNode_MotionMatching']; assert len(mm) == 1
    old = src((mm[0], 'BlendTime')); assert not old, ('BlendTime already bound', old)
    cur = [q.value for q in info(mm[0]).input_pins if q.name == 'BlendTime'][0]; out['blend_default'] = cur
    sel = ga.select(ga.AND(ga.within(ga.get('SHM239_Own'), 0.5, 1.0e9), ga.get('SHM239_TkOn')), ga.get('SHM239_TkBlend'), float(cur))
    connect(sel, (mm[0], 'BlendTime')); out['patch'] = 'BlendTime := takeover ? TkBlend : %s' % cur
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('BLEND239 ' + json.dumps(out, default=str))
