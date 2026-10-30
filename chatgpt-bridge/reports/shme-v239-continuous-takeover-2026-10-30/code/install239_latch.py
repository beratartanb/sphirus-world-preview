"""install239_latch.py (editor job) - V2.39: a running plan's heading / speed contract survives a new request (behind SHM239_Own).
Measured (v239c_j39_rl_tk_r1, 30 FPS): at the left request mid-cut (5.867 s) the V2.28 contract dropped SHM228_On for ONE frame (its
episode restart on the new intent) -> SHM238_On fell and rose -> the V2.38 yaw latch re-read Yaw0 := actor yaw (42) and Delta := the NEW
request (-132) while the SAME cut clip kept playing -> Cmd = 42 - 132 * T / 90 with the cut's turn T ~ 37 -> actor yaw 42 -> -81 deg in
0.2 s (1400 deg/s), the plan's frame was lost and the takeover request (measured against that frame) was cleared after one frame.
Owner rule: the plan's frame belongs to the plan (the clip's own SHM238_W), not to the V2.28 episode. While SHM239_Own is on and the
plan was already running in the previous frame (SHM239_W, stored by install239_own at the end of the snapshot, > 0.3) and still runs
(curve SHM238_W > 0.3):
  SetSHM238_Yaw0 / SetSHM238_Delta: their rising-edge Select is masked (no re-latch);
  SetSHM238_On, component SetClipSpeedOn: OR the hold (a one-frame V2.28 dropout does not hand the capsule back to GR / CMC).
Idempotent (marker variable SHM239_LatchFix). builtins.V239_SAVE saves. Prints LATCH239 {...}."""
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
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
bp = u.load_asset(AP)
already = 'SHM239_LatchFix' in [str(v) for v in B.list_variables(bp)]
if already: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM239_LatchFix', 'bool', 'SHM239')]); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    def one(suffix):
        x = [p for p in sn if tid(p).endswith(suffix)]; assert len(x) == 1, (suffix, len(x)); return x[0]
    def hold():
        cw = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM238_W'})
        return gs.AND(gs.AND(gs.within(gs.get('SHM239_Own'), 0.5, 1.0e9), gs.within(gs.get('SHM239_W'), 0.3, 1.0e9)), gs.within(cw, 0.3, 1.0e9))
    out['patch'] = {}
    for suffix, pin in (('SetSHM238_Yaw0', 'SHM238_Yaw0'), ('SetSHM238_Delta', 'SHM238_Delta')):
        s_ = one(suffix); sel = src((s_, pin)); assert len(sel) == 1 and 'Select' in tid(sel[0][0]), (suffix, [tid(q[0]) for q in sel])
        sp = [q.name for q in info(sel[0][0]).input_pins]; bpin = 'bPickA' if 'bPickA' in sp else sp[-1]
        r_ = src((sel[0][0], bpin)); assert len(r_) == 1, (suffix, bpin)
        disconnect((sel[0][0], bpin)); connect(gs.AND(r_[0], gs.NOT(hold())), (sel[0][0], bpin)); out['patch'][suffix] = bpin
    for suffix, pin in (('SetSHM238_On', 'SHM238_On'), ('SetClipSpeedOn', 'ClipSpeedOn')):
        s_ = one(suffix); old = src((s_, pin)); assert len(old) == 1, (suffix, old)
        disconnect((s_, pin)); connect(gs.OR(old[0], hold()), (s_, pin)); out['patch'][suffix] = 'or-hold'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]
cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
ok = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
out['ok'] = ok
if ok and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('LATCH239 ' + json.dumps(out, default=str))
