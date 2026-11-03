"""install252_yawtau.py (editor job, write manifest = ABP base + child): V2.52 owner of the 180 deg crop-end 60 FPS pop.
Measured frame by frame (v251f60 jstart, bone second differences in the root frame): the spike is NOT on the clip transition frame (15.000)
but two frames later (15.033, shoulder -2.0 cm, pelvis -0.65 / -0.50 cm) - the frame where the V2.51 yaw hand-over (SHM251_YawSlew,
constant 150 deg/s) reaches its target and the body's yaw rate drops from 150 deg/s to ~0 in one frame (orientation warping then
re-poses pelvis / chest in that one frame). A turning body decelerates, it does not stop dead.
Patch: the hand-over step becomes an exponential approach capped by the rate: step = FClamp(err * dt / (SHM252_YawTau + dt), +-rate*dt).
SHM252_YawTau default 0 -> dt / dt = 1 -> exactly the V2.51 behaviour; 0.08 s -> the yaw rate decays smoothly to zero.
Idempotent (variable SHM252_YawTau). builtins.V252_SAVE saves. Prints YAWTAU252 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
assert 'SHM251_YawSlew' in V
if 'SHM252_YawTau' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM252_YawTau', 'float', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM252_YawTau': 0.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    cand = []
    for p in sn:
        try: names = [str(q.name) for q in info(p).input_pins]
        except Exception: continue
        if 'Value' in names and 'Min' in names and 'Max' in names:
            s_ = src((p, 'Value'))
            if len(s_) == 1 and 'NormalizeAxis' in tid(s_[0][0]): cand.append((p, s_[0]))
    assert len(cand) == 1, [c_[0].rsplit('.', 1)[-1] for c_ in cand]
    cl, err = cand[0]
    disconnect((cl, 'Value'))
    dt = gs.pure('/Script/Engine.GameplayStatics:GetWorldDeltaSeconds', {})
    alpha = gs.pure(M + 'SafeDivide', {'A': dt, 'B': gs.math(gs.get('SHM252_YawTau'), dt, 1)})
    connect(gs.pure('MapRangeUnclamped', {'Value': err, 'InRangeA': 0, 'InRangeB': 1, 'OutRangeA': 0, 'OutRangeB': alpha}), (cl, 'Value'))
    out['wired'] = {'clamp': cl.rsplit('.', 1)[-1], 'err': err[0].rsplit('.', 1)[-1]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM252_YawTau'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V252_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('YAWTAU252 ' + json.dumps(out, default=str))
