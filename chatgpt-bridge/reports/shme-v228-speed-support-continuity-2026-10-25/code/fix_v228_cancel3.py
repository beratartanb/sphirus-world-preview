"""fix_v228_cancel3.py (editor job): the against-intent safety (fix_v228_cancel2) fired during the BRAKE phase (the designed speed legitimately
opposes the new intent while the body still moves the old way): v228m2 rel - Dead pulsed from 0.08 s after the entry, the hold and the
clip-bound speed dropped, and the release then latched Dead for good (walk stop). Fix: the safety counts only in the PUSH phase - the AND
feeding SetSHM228_AgainstT gets a term (DesV * EntrySign < -1). Idempotent. builtins.V228_SAVE saves. Prints CANCEL228C {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name() in (AP, CP)]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
bp = u.load_asset(AP)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
ag = [p for p in sn if 'SetSHM228_AgainstT' in tid(p)]; assert len(ag) == 1, ag
sel = src((ag[0], 'SHM228_AgainstT')); assert len(sel) == 1 and 'SelectFloat' in tid(sel[0][0]), sel
cond = src((sel[0][0], 'bPickA')); assert len(cond) == 1, cond
marker = 'SHM228_Fix3' in [str(v) for v in B.list_variables(bp)]
if marker:
    out['safety'] = 'already'
else:
    push = gs.within(gs.mul(gs.get('SHM228_DesV'), gs.get('SHM228_EntrySign')), -1.0e9, -1.0)   # designed speed along the EXIT direction = push phase
    disconnect((sel[0][0], 'bPickA')); connect(gs.AND(cond[0], push), (sel[0][0], 'bPickA')); out['safety'] = 'push-phase only'
    ensure_vars(bp, [('SHM228_Fix3', 'bool', 'SHM228')])
out['family'] = 'not changed (consumer scan found none; open item: rerouted clip exit via the family route)'
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child']
out['ok'] = ok
if ok and getattr(builtins, 'V228_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('CANCEL228C ' + json.dumps(out, default=str))
