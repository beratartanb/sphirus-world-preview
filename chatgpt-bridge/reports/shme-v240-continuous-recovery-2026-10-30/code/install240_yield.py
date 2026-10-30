"""install240_yield.py (editor job) - V2.40: a running TAKEOVER plan yields to a THIRD request at its momentum low (behind SHM239_Own).
Measured (v240f30_j40_rlw_tk, 30 FPS): R90 -> L mid-brake takeover (SHM239_Tk_R_P21_K2_Opp, target -90) -> W (0 deg) at 6.33 s. The
takeover braked the body to 14 cm/s at 6.37 (support building) but the plan owner only takes over a SOURCE cut (TkReq needs TgtC < 500),
so the clip kept its own plan: re-push to -88 deg at 6.63, then the regular system turned back to 0 - an S-shaped -90 detour against the
player's intent. The momentum to keep was already spent: the right owner of a near-standstill body with a new intent is the normal
start / push routing (it starts from the real pose and velocity), not the old plan's re-push. Decision order on the takeover clip:
  continue the plan          intent within SHM239_TkThr (35) of the plan target, or the body still carries momentum (>= SHM240_YSpd)
  yield (new plan = start)   SHM240_Yield := Own AND OwnOn AND HasIn AND playing a takeover (curve SHM239_Tgt > 500)
                               AND |Rel - PT| > TkThr AND |v| < SHM240_YSpd (80 cm/s)
                             latched while the plan curve runs (SHM239_W > 0.3) and input is held
  while Yield                SHM239_OwnOn / SHM238_On / component ClipSpeedOn are AND NOT Yield (the same stand-down the external
                             effect uses; FamOff unchanged - a yield is not a shove); the V2.40 exit hand-off (install240_exit2) gives
                             the body frame the actor heading on that frame. No hold, no delay, no new clip.
Splice: the next nodes keep ALL their other incoming exec links (V2.40 exec-splice trap). Idempotent (marker SHM240_Yield).
builtins.V240_SAVE saves. Prints YIELD240 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
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
bp = u.load_asset(AP)
if 'SHM240_Yield' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM240_Yield', 'bool', 'SHM240'), ('SHM240_YSpd', 'float', 'SHM240')]); compile_ok(bp)
    set_defaults(bp, {'SHM240_YSpd': 80.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    last = [p for p in sn if tid(p).endswith('SetSHM239_PrevStep')]; assert len(last) == 1
    lt = (last[0], 'then')
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and lt in src((p, 'execute'))]
    keep = {x: [s_ for s_ in src((x, 'execute')) if s_ != lt] for x in nxt}
    for x in nxt: disconnect((x, 'execute'))
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    spd = gs.pure(M + 'VSize', {'A': gs.pure('/Script/Engine.Actor:GetVelocity', {'self': pawn})})
    diff = gs.pure(M + 'Abs', {'A': gs.sub(gs.get('SHM239_Rel'), gs.get('SHM239_PT'))})
    playtk = gs.within(gs.get('SHM239_TgtC'), 500.0, 1.0e9)
    now = gs.AND(gs.AND(gs.AND(gs.within(gs.get('SHM239_Own'), 0.5, 1.0e9), gs.get('SHM239_OwnOn')), gs.AND(gs.get('SHM239_HasIn'), playtk)),
                 gs.AND(gs.within(diff, gs.get('SHM239_TkThr'), 1.0e9), gs.within(spd, -1.0, gs.get('SHM240_YSpd'))))
    held = gs.AND(gs.get('SHM240_Yield'), gs.AND(gs.within(gs.get('SHM239_W'), 0.3, 1.0e9), gs.get('SHM239_HasIn')))
    t = gs.set('SHM240_Yield', gs.OR(now, held), lt)
    for x in nxt:
        connect(t, (x, 'execute'))
        for s_ in keep[x]: connect(s_, (x, 'execute'))
    out['splice'] = {x.rsplit('.', 1)[-1]: len(src((x, 'execute'))) for x in nxt}
    assert all(len(src((x, 'execute'))) == len(keep[x]) + 1 for x in nxt), out['splice']
    pt = {}
    for suffix, pin in (('SetSHM239_OwnOn', 'SHM239_OwnOn'), ('SetSHM238_On', 'SHM238_On'), ('SetClipSpeedOn', 'ClipSpeedOn')):
        ss = [p for p in sn if tid(p).endswith(suffix)]; assert ss, suffix
        for s_ in ss:
            old = src((s_, pin)); assert len(old) == 1, (suffix, old)
            disconnect((s_, pin)); connect(gs.AND(old[0], gs.NOT(gs.get('SHM240_Yield'))), (s_, pin))
        pt[suffix] = len(ss)
    out['patch'] = pt
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V240_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('YIELD240 ' + json.dumps(out, default=str))
