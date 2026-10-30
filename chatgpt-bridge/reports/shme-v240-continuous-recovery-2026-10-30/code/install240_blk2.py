"""install240_blk2.py (editor job) - V2.40 (after install240_wall + install240_head): two measured corrections.
1. Wall stop at 30 FPS (v240h30_j40_wall_tk: Ext 6.3 .. 6.9, |v| < 60 from 6.4, but the stand search never ran - the cut clip played
   on the spot until 7.03; at 120 FPS the same rule switched on the contact frame 6.533). The V2.39 trap again: during the redirect
   hold the MM node does not search and a ForceInterrupt from SetDatabaseToSearch does not override SearchThrottleTime.
   AnimGraph MM SearchThrottleTime Select pick := <old: Own AND TkOn> OR SHM240_Blk       (throttle 0 while the body is blocked)
2. Head priority during a planned clip (v240h30_j38_c90r_hd vs _o: same clips, but without the vendor aim offset the pelvis turned
   3-6 deg and the chest 6-22 deg further toward the travel inside the authored cut, and the planted left ball moved 3 cm on one
   frame (5.97 s) -> slide 0 -> 10 cm). The aim offset also carries the pelvis / chest; the authored plan clip owns that relation
   while it plays. The head fade therefore waits for the plan curve:
   SHM240_AOFadeT := <head240 target> * (1 - clamp(SHM239_W))       (SHM239_W = the plan curve SHM238_W, blended)
Idempotent (markers: the throttle pick reads GetSHM240_Blk; the AOFadeT input reads GetSHM239_W). builtins.V240_SAVE saves.
Prints BLK2_240 {...}."""
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
def reads(ep, suffix, depth=3):
    """does the value feeding ep (directly or through <= depth pure nodes) read a getter ending with suffix"""
    for s_ in src(ep):
        if tid(s_[0]).endswith(suffix): return True
        if depth and any(reads((s_[0], q.name), suffix, depth - 1) for q in info(s_[0]).input_pins if q.name not in ('execute', 'self')): return True
    return False
out = {'reloaded': names}
bp = u.load_asset(AP)
# 1. throttle
ag = pn(graph(bp, 'AnimGraph')); ga = G(ag)
mm = [pn(n) for n in B.find_nodes(obj(ag)) if n.get_class().get_name() == 'AnimGraphNode_MotionMatching']; assert len(mm) == 1
sel = src((mm[0], 'SearchThrottleTime')); assert len(sel) == 1 and 'Select' in tid(sel[0][0]), sel
pk = ['bPickA']; assert src((sel[0][0], 'bPickA')), 'throttle Select pick unbound'
if reads((sel[0][0], pk[0]), 'GetSHM240_Blk'): out['throttle'] = 'already'
else:
    old = src((sel[0][0], pk[0])); assert len(old) == 1
    disconnect((sel[0][0], pk[0])); connect(ga.OR(old[0], ga.get('SHM240_Blk')), (sel[0][0], pk[0])); out['throttle'] = 'pick OR SHM240_Blk'
# 2. head fade waits for the plan curve
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
ft = [p for p in sn if tid(p).endswith('SetSHM240_AOFadeT')]; assert len(ft) == 1
if reads((ft[0], 'SHM240_AOFadeT'), 'GetSHM239_W', 1): out['head'] = 'already'
else:
    old = src((ft[0], 'SHM240_AOFadeT')); assert len(old) == 1
    disconnect((ft[0], 'SHM240_AOFadeT')); connect(gs.mul(old[0], gs.map(gs.get('SHM239_W'), 0.0, 1.0, 1.0, 0.0)), (ft[0], 'SHM240_AOFadeT')); out['head'] = 'fade * (1 - W)'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V240_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('BLK2_240 ' + json.dumps(out, default=str))
