"""install239_ext2.py (editor job) - V2.39: the external-effect read runs FIRST in SHM_Snapshot (after install239_ext).
Measured (v239t_j39_push_plan_tk): residual 282 cm/s on the shove frame (planned motion <= 9), Ext latched - but Ext was computed at the
END of the snapshot, after SetClipSpeedOn: GR still wrote the clip velocity on the next tick and erased the shove (vy back to the plan's
+67), so the capsule never carried it and pushRaw never fired. The residual only needs last frame's clip speed (SHM239_CsPrev / ConPrev,
still stored at the end), so SetSHM239_Resid -> SetSHM239_ExtT0 -> SetSHM239_Ext move to the snapshot entry: the same frame's
ClipSpeedOn / SHM238_On / OwnOn / FamOff already yield. Idempotent. builtins.V239_SAVE saves. Prints EXT2_239 {...}."""
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
one = lambda sfx: [p for p in sn if tid(p).endswith(sfx)]
r_, e_ = one('SetSHM239_Resid'), one('SetSHM239_Ext'); assert len(r_) == 1 and len(e_) == 1
entry = [p for p in sn if 'FunctionEntry' in p.rsplit('.', 1)[-1]]; assert len(entry) == 1
if (entry[0], 'then') in src((r_[0], 'execute')): out['patch'] = 'already'
else:
    pre = src((r_[0], 'execute')); assert len(pre) == 1
    post = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (e_[0], 'then') in src((p, 'execute'))]
    first = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (entry[0], 'then') in src((p, 'execute'))]; assert len(first) == 1
    disconnect((r_[0], 'execute'))
    for x in post: disconnect((x, 'execute')); connect(pre[0], (x, 'execute'))          # close the gap where the block was
    disconnect((first[0], 'execute')); connect((entry[0], 'then'), (r_[0], 'execute')); connect((e_[0], 'then'), (first[0], 'execute'))
    out['patch'] = {'moved_after_entry': True, 'gap_closed_to': [x.rsplit('.', 1)[-1] for x in post]}
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('EXT2_239 ' + json.dumps(out, default=str))
