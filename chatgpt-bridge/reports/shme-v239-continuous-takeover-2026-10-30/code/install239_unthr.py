"""install239_unthr.py (editor job) - V2.39: the takeover latch releases the search throttle (after install239_blend).
Measured (v239m/n/o j39_rl / rw / rl_e / rl_l: identical numbers with the search gate, the alternating force and the short blend):
every successful takeover switch came exactly one frame after the ABP episode class changed (rl 6.10 -> 6.13, rw 5.97 -> 6.00, ...).
A class change restarts the ABP episode (SHM_RedirectFrames -> 1) and releases the redirect-hold search throttle for that frame; while
the hold runs the MM node does not search, and a ForceInterrupt from SetDatabaseToSearch does not override SearchThrottleTime.
Patch: AnimGraph MM SearchThrottleTime := Select(SHM239_Own > 0.5 AND SHM239_TkOn, 0, <existing FMax chain>).
Idempotent. builtins.V239_SAVE saves. Prints UNTHR239 {...}."""
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
old = src((mm[0], 'SearchThrottleTime')); assert len(old) == 1, old
if 'Select' in tid(old[0][0]) and any(tid(v[0]).endswith('GetSHM239_TkOn') for k in ('bPickA', 'PickA') for v in src((old[0][0], k)) ): out['patch'] = 'already'
else:
    disconnect((mm[0], 'SearchThrottleTime'))
    connect(ga.select(ga.AND(ga.within(ga.get('SHM239_Own'), 0.5, 1.0e9), ga.get('SHM239_TkOn')), 0.0, old[0]), (mm[0], 'SearchThrottleTime')); out['patch'] = 'throttle 0 while TkOn'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('UNTHR239 ' + json.dumps(out, default=str))
