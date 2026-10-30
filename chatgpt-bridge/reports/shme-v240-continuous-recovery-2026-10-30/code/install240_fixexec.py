"""install240_fixexec.py (editor job) - V2.40 REPAIR of the SHM_Snapshot exec chain (after install240_exit2).
install240_exit2 spliced the exploration hand-off in front of SetSHM240_WasTk with disconnect((node, 'execute')) - which removes ALL
incoming exec links: the exit branch's ELSE path and the deterministic-entry cast's CastFailed path no longer reached SetSHM240_WasTk,
so on every frame without a takeover exit the snapshot stopped there and the rest of SHM_Snapshot (incl. the redirect-episode logic)
never ran - the V2.38 cut route failed for EVERY run, production included (v240e30_*_o: SHM_RedirectActive never true).
Repair: reconnect <exit branch>.else and <cast>.CastFailed to SetSHM240_WasTk.execute; then a census: SetSHM240_WasTk must have 3
incoming exec links (exit path, else, CastFailed). Idempotent. builtins.V240_SAVE saves. Prints FIX240 {...}."""
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
bp = u.load_asset(AP); sg = pn(graph(bp, 'SHM_Snapshot')); sn = [pn(n) for n in B.find_nodes(obj(sg))]
w = [p for p in sn if tid(p).endswith('SetSHM240_WasTk')]; assert len(w) == 1; w = w[0]
ly = [p for p in sn if tid(p).endswith('SetLocoYaw')]; assert len(ly) == 1
br = src((ly[0], 'execute')); assert len(br) == 1 and br[0][1] == 'then', br; brn = br[0][0]
edb = [p for p in sn if tid(p).endswith('SetSHM240_EDB')]; assert len(edb) == 1
cast = src((edb[0], 'execute')); assert len(cast) == 1; castn = cast[0][0]
have = src((w, 'execute')); out['before'] = [(s[0].rsplit('.', 1)[-1], s[1]) for s in have]
for need in ((brn, 'else'), (castn, 'CastFailed')):
    if need not in have: connect(need, (w, 'execute'))
after = src((w, 'execute')); out['after'] = [(s[0].rsplit('.', 1)[-1], s[1]) for s in after]
assert len(after) == 3, out['after']
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V240_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('FIX240 ' + json.dumps(out, default=str))
