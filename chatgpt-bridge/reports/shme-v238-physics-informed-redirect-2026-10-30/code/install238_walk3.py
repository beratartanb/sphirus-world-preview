"""install238_walk3.py (editor job) - V2.38: the walk guard only acts while the COMPONENT has an episode (after install238_walk2.py).
Measured (v238fin, clean reopen, o vs pre238): the speed-only walk guard (component RedirectSpeed0 < 220) also skipped
  - the backpedal -> forward reversal (class 2, start speed 206 / 205): j35_rev 6.1 -> 34.4 cm, j30_rel_3450 7.3 -> 26.2 (loop + family 6),
  - the re-latch inside the sprint 90 cut of e29_chain (class 0, 194 cm/s, episode already active): 6.4 -> 43.9 (vendor sprint 180).
Patch: SHM238_WalkSkip := old condition AND component RedirectClass <= 1.5 (lateral, not reversal) AND NOT SHM_RedirectActive (only the
episode start is skipped; an episode already running is never cut off). The walk 90 (class 0, 123 cm/s, not yet active) stays skipped.
Measured (v238fin3, o vs pre238, first divergent frame): outside any episode the walk2 guard was still TRUE (stale RedirectSpeed0 from
the last episode or 0 after a start, class 0, not active) -> SHM_RdLatSkip stuck True between episodes changed loop entries and the capsule
path (w38_c90r 0 -> 5.1, j36_stop 0 -> 9.0, mt_jog capsule 9.5 cm off at 4.63 s, j30_rel_3450 loop entry half a cycle away).
Patch: SHM238_WalkSkip := component RedirectActive AND <walk2 condition> - outside a component episode SHM_RdLatSkip is exactly V2.37.
Idempotent (the value source becomes AND(RedirectActive, walk2)). builtins.V238_SAVE saves. Prints WALK238C {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': names}
def isand(t): return 'ANDBoolean' in t or 'BooleanAND' in t   # localized editor: 'Matematik|Boolean|ANDBoolean'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
bp = u.load_asset(AP)
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
ws = [p for p in sn if tid(p).endswith('SetSHM238_WalkSkip')]; assert ws, 'SetSHM238_WalkSkip (install238_walk.py first)'
out['patched'] = []
for s_ in ws:
    old = src((s_, 'SHM238_WalkSkip')); assert len(old) == 1, old
    o0 = old[0]; assert isand(tid(o0[0])), 'walk2 not installed'
    a_src = src((o0[0], 'A'))
    if a_src and tid(a_src[0][0]).endswith('GetRedirectActive'): out['patched'].append('already'); continue
    b_src = src((o0[0], 'B')); assert a_src and isand(tid(a_src[0][0])), 'walk2 structure (AND(AND(lat, new), old))'
    disconnect((s_, 'SHM238_WalkSkip'))
    connect(gs.AND(gs.get('RedirectActive', COMP, ct), o0), (s_, 'SHM238_WalkSkip'))
    out['patched'].append(s_.rsplit('.', 1)[-1])
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]
cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
ok = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
out['ok'] = ok
if ok and getattr(builtins, 'V238_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('WALK238C ' + json.dumps(out, default=str))
