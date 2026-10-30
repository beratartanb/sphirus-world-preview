"""install238_walk2.py (editor job) - V2.38: narrow the walk guard of install238_walk.py to NEW lateral episodes.
Measured (v238fin, clean reopen, o vs pre238): the speed-only walk guard (component RedirectSpeed0 < 220) also skipped
  - the backpedal -> forward reversal (class 2, start speed 206 / 205): j35_rev 6.1 -> 34.4 cm, j30_rel_3450 7.3 -> 26.2 (loop + family 6),
  - the re-latch inside the sprint 90 cut of e29_chain (class 0, 194 cm/s, episode already active): 6.4 -> 43.9 (vendor sprint 180).
Patch: SHM238_WalkSkip := old condition AND component RedirectClass <= 1.5 (lateral, not reversal) AND NOT SHM_RedirectActive (only the
episode start is skipped; an episode already running is never cut off). The walk 90 (class 0, 123 cm/s, not yet active) stays skipped.
Idempotent (the value pin source becomes AND(AND(..), old)). builtins.V238_SAVE saves. Prints WALK238B {...}."""
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
    o0 = old[0]
    a_src = src((o0[0], 'A')) if 'BooleanAND' in tid(o0[0]) else []
    if a_src and 'BooleanAND' in tid(a_src[0][0]): out['patched'].append('already'); continue
    disconnect((s_, 'SHM238_WalkSkip'))
    lat = gs.within(gs.get('RedirectClass', COMP, ct), -1.0, 1.5)
    new = gs.NOT(gs.get('SHM_RedirectActive'))
    connect(gs.AND(gs.AND(lat, new), o0), (s_, 'SHM238_WalkSkip'))
    out['patched'].append(s_.rsplit('.', 1)[-1])
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]
cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
ok = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
out['ok'] = ok
if ok and getattr(builtins, 'V238_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('WALK238B ' + json.dumps(out, default=str))
