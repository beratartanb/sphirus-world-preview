"""install239_srch.py (editor job) - V2.39: the takeover latch may search (after install239_own/_tkon/_req/_thr/_play).
Measured (v239l_j39_rl_tk, call counter SHM239_UmmN): Update_MotionMatching ran every frame and called SetDatabaseToSearch(takeover,
ForceInterruptAndInvalidateContinuingPose) for the 7 latched frames, yet the cut clip kept playing - the AnimGraph MM node's bShouldSearch
is bound to SHM220_Search (V2.20/V2.21 search gate: off while an authored clip holds), so no search ran until that gate reopened
(0.6-0.73 s after the cut entry in every run) and the takeover landed one contact late (K3 instead of K2).
Patch: AnimGraph MM bShouldSearch := SHM220_Search OR (SHM239_Own > 0.5 AND SHM239_TkOn) - only the takeover latch (<= 7 frames) opens
the gate; everything else unchanged. Idempotent. builtins.V239_SAVE saves. Prints SRCH239 {...}."""
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
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {'reloaded': names}
bp = u.load_asset(AP); ag = pn(graph(bp, 'AnimGraph')); ga = G(ag)
mm = [pn(n) for n in B.find_nodes(obj(ag)) if n.get_class().get_name() == 'AnimGraphNode_MotionMatching']; assert len(mm) == 1
old = src((mm[0], 'bShouldSearch')); assert len(old) == 1, old
if not tid(old[0][0]).endswith('GetSHM220_Search'): out['patch'] = 'already' if 'OR' in tid(old[0][0]) else ('unexpected ' + tid(old[0][0]))
else:
    disconnect((mm[0], 'bShouldSearch'))
    connect(ga.OR(old[0], ga.AND(ga.within(ga.get('SHM239_Own'), 0.5, 1.0e9), ga.get('SHM239_TkOn'))), (mm[0], 'bShouldSearch')); out['patch'] = 'search OR takeover latch'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and not out['patch'].startswith('unexpected')
if out['ok'] and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('SRCH239 ' + json.dumps(out, default=str))
