"""install249_servo2.py (editor job, write manifest = ABP base + child; after install249_servo.py): FEED-FORWARD servo.
Measured (v249c60 rm): the position servo vel = (target - pos)/dt with a 2-frame lead amplified Motion Matching's play-rate jitter
(clip time steps 0.013-0.020 s per 1/60 frame: MM adapts the rate 0.7-1.2 to the trajectory speed, which the servo itself sets) ->
capsule speed alternating 78 / 206 cm/s, pops. New law (breaks the loop, keeps the path lock):
  vel = Fwd(target yaw) * V + Right(target yaw) * VL  +  Kp * (target - pos) / dt         (V, VL = the clip's own root velocity curves
  SHM226_V / SHM226_VL normalised by W; Kp = SHM249_Kp 0.35; SHM249_Lead := 1)
Rewires the X / Y inputs of the servo's velocity MakeVector (the one feeding the Dot -> SetClipSpeed of the V2.49 servo block).
Idempotent (variable SHM249_Kp). builtins.V249_SAVE saves. Prints SERVO249B {...}."""
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
bp = u.load_asset(AP); Vs = [str(v) for v in B.list_variables(bp)]
assert 'SHM249_Lead' in Vs, 'install249_servo.py first'
if 'SHM249_Kp' in Vs: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM249_Kp', 'float', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM249_Kp': 0.35, 'SHM249_Lead': 1.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    def dot_set(var):
        for p in sn:
            if not tid(p).endswith('|Set' + var): continue
            s_ = src((p, var))
            if s_ and 'Dot' in tid(s_[0][0]): return p, s_[0][0]
        return None, None
    sc, dsc = dot_set('ClipSpeed'); sl, dsl = dot_set('ClipSpeedLat'); assert sc and sl, ('servo set nodes', sc, sl)
    mv = src((dsc, 'A'))[0][0]; assert 'MakeVector' in tid(mv), tid(mv)
    fT = src((dsc, 'B'))[0]; rT = src((dsl, 'B'))[0]
    xs = src((mv, 'X'))[0]; ys = src((mv, 'Y'))[0]
    disconnect((mv, 'X')); disconnect((mv, 'Y'))
    W = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM226_W'})
    Vc = gs.pure(M + 'SafeDivide', {'A': gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM226_V'}), 'B': W})
    VLc = gs.pure(M + 'SafeDivide', {'A': gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM226_VL'}), 'B': W})
    bf = gs.fn('BreakVector', {'InVec': fT}); br = gs.fn('BreakVector', {'InVec': rT})
    ffx = gs.math(gs.mul((bf, 'X'), Vc), gs.mul((br, 'X'), VLc), 1); ffy = gs.math(gs.mul((bf, 'Y'), Vc), gs.mul((br, 'Y'), VLc), 1)
    connect(gs.math(ffx, gs.mul(xs, gs.get('SHM249_Kp')), 1), (mv, 'X')); connect(gs.math(ffy, gs.mul(ys, gs.get('SHM249_Kp')), 1), (mv, 'Y'))
    out['servo2'] = {'make_vector': mv.rsplit('.', 1)[-1], 'x_old': xs[0].rsplit('.', 1)[-1]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: str(cdo.get_editor_property(k)) for k in ('SHM249_RM', 'SHM249_Lead', 'SHM249_Kp')}
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knobs']['SHM249_RM'] == '0.0'
if out['ok'] and getattr(builtins, 'V249_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('SERVO249B ' + json.dumps(out, default=str))
