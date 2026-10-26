"""install_v230_idleguard.py (editor job) - V2.30 release -> re-press inside the authored jog reversal: idle entry must not take over.
Measured (v230fin j24_rel vs v230t1 j24_rel, same inputs): S released 0.15 s inside the held reversal (SHM227_Hold, capsule ~0 cm/s at the
designed zero crossing). One run planted the left heel one frame earlier (pose difference 2-3 mm), SHM_IdleWait (feet moving / settling)
fell, idleNow became true -> SHM_IdleEntry / SHM_IdleHold at 5.40 s -> the reversal hold ended at 5.50 s although S was pressed again at
5.47 s -> Motion Matching played Jog_Bwd_Start_AAMS from the brake stance (right foot slide 33.8 cm). The V2.29 release-resume window
(SHM229_ResumeWin, PostT) never got the chance: idle entry is a separate path.
Change (SHM_Snapshot, graph level): idleNow -> AND(idleNow, NOT(knob AND SHM227_Hold AND (SHM228_Brake OR PostT < SHM229_ResumeWin))) for
every consumer of idleNow (IdleEntry and IdlePrev both read it, so idle is entered normally once the window is over). Knob SHM230_IdleGuard
default 0 = V2.29 behaviour. Idempotent (SHM230_IGFix). builtins.V230_SAVE saves. Prints IDLEGUARD230 {...}."""
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
vars_ = [str(v) for v in B.list_variables(bp)]
assert 'SHM229_PostT' in vars_ and 'SHM227_Hold' in vars_, 'V2.29 resume / V2.27 hold variables missing'
if 'SHM230_IGFix' in vars_:
    out['snapshot'] = 'already'
else:
    ensure_vars(bp, [('SHM230_IdleGuard', 'float', 'SHM230')]); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    ie = [p for p in sn if 'SetSHM_IdleEntry' in tid(p)]; assert len(ie) == 1, [tid(p)[-40:] for p in ie]
    a = src((ie[0], 'SHM_IdleEntry')); assert len(a) == 1 and 'ANDBoolean' in tid(a[0][0]), tid(a[0][0])
    andn = a[0][0]; sa, sb = src((andn, 'A')), src((andn, 'B')); assert len(sa) == 1 and len(sb) == 1
    def is_not_prev(s): return 'NOTBoolean' in tid(s[0][0]) and any('SHM_IdlePrev' in tid(z[0]) for z in src((s[0][0], 'A')))
    idle = sa[0] if is_not_prev(sb) else (sb[0] if is_not_prev(sa) else None); assert idle, 'idleNow term not found'
    cons = []
    for p in sn:
        try: ins = info(p).input_pins
        except Exception: continue
        for q in ins:
            if idle in src((p, q.name)): cons.append((p, q.name))
    out['consumers'] = [(c[0].rsplit('.', 1)[-1], c[1]) for c in cons]; assert len(cons) >= 2, out['consumers']
    win = gs.OR(gs.get('SHM228_Brake'), gs.AND(gs.within(gs.get('SHM229_PostT'), -1.0, gs.get('SHM229_ResumeWin')), gs.within(gs.get('SHM229_ResumeWin'), 0.001, 1.0e9)))
    block = gs.AND(gs.within(gs.get('SHM230_IdleGuard'), 0.5, 1.0e9), gs.AND(gs.get('SHM227_Hold'), win))
    guarded = gs.AND(idle, gs.NOT(block))
    for c in cons: disconnect(c); connect(guarded, c)
    ensure_vars(bp, [('SHM230_IGFix', 'bool', 'SHM230')])
    out['snapshot'] = 'wired'
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = float(cdo.get_editor_property('SHM230_IdleGuard'))
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and out['knob'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V230_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('IDLEGUARD230 ' + json.dumps(out, default=str))
