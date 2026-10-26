"""install_v229_resume.py (editor job) - V2.29 release -> re-press of the authored jog reversal (V2.28 open: 32-34 cm vendor start).
Measured (v228fin j24_rel): S released 0.27 s into the brake -> V2.28 RelHold held the clip to the designed zero crossing (ct 0.43,
5.43 s), the hold ended in the SAME frame the re-pressed S reached the CMC (5.47 s: HasIntent is read from the component's last tick)
-> Motion Matching searched the standing-start database and played Jog_Bwd_Start_AAMS from a brake stance (slide 32-34 cm), although
the reversal clip was in its push phase in exactly the requested direction.
Change (SHM_Snapshot, graph level): SHM229_PostT = time since SHM228_Brake fell (0 while braking, += component DeltaTime after);
every place the V2.28 RelHold gate reads SHM228_Brake (the hold's lost-intent term and IntentEnd's relKeep) reads
OR(Brake, PostT < SHM229_ResumeWin) instead: a released brake keeps the clip for ResumeWin past its zero crossing; a re-press along the
push phase inside that window simply continues the same clip instance (clip-bound capsule, V2.28) = the push from the current support;
no re-press -> the hold ends after ResumeWin as before. Knob SHM229_ResumeWin default 0 = V2.28 behaviour. Idempotent (SetSHM229_PostT).
builtins.V229_SAVE saves the ABPs. Prints RESUME229 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg, value
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name() in (AP, CP)]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
bp = u.load_asset(AP)
ensure_vars(bp, [('SHM229_ResumeWin', 'float', 'SHM229'), ('SHM229_PostT', 'float', 'SHM229')]); compile_ok(bp)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def step(s): out['step'] = s; print('RESUME229 step ' + s)
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any('SetSHM229_PostT' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    step('find')
    bset = [p for p in sn if 'SetSHM228_Brake' in tid(p)]; assert len(bset) == 1, bset
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'
    ct = (comp[0], 'ReturnValue')
    # consumers of 'get SHM228_Brake' that sit in an AND together with within(SHM228_RelHold)
    bgets = [p for p in sn if tid(p).endswith('|GetSHM228_Brake') or (tid(p).endswith('SHM228_Brake') and 'Set' not in tid(p))]
    def relhold_and(nd):
        if 'ANDBoolean' not in tid(nd): return False
        for q in info(nd).input_pins:
            for s in src((nd, q.name)):
                if 'InRange' in tid(s[0]) and any('SHM228_RelHold' in tid(z[0]) for z in src((s[0], 'Value'))): return True
                if 'ANDBoolean' in tid(s[0]) and relhold_and(s[0]): return True
        return False
    targets = []
    for g_ in bgets:
        for nd in [pn(n) for n in B.find_nodes(obj(sg))]:
            for q in info(nd).input_pins:
                if (g_, 'SHM228_Brake') in src((nd, q.name)) and relhold_and(nd): targets.append((nd, q.name, g_))
    out['targets'] = [(a.rsplit('.', 1)[-1], b) for a, b, c in targets]
    assert len(targets) >= 2, ('expected the hold term and relKeep', out['targets'], [tid(p)[-30:] for p in bgets])
    step('postT')
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (bset[0], 'then') in src((p, 'execute'))]; assert nxt, 'next after Brake'
    for x in nxt: disconnect((x, 'execute'))
    dt = gs.get('DeltaTime', COMP, ct)
    acc = gs.pure('/Script/Engine.KismetMathLibrary:FInterpTo_Constant', {'Current': gs.get('SHM229_PostT'), 'Target': 1.0e9, 'DeltaTime': dt, 'InterpSpeed': 1.0})   # PostT + dt (no promotable operator in the AnimBP)
    post = gs.select(gs.get('SHM228_Brake'), 0.0, acc)
    tail = gs.set('SHM229_PostT', post, (bset[0], 'then'))
    for x in nxt: connect(tail, (x, 'execute'))
    step('rewire')
    for nd, pin, g_ in targets:
        win = gs.AND(gs.within(gs.get('SHM229_PostT'), -1.0, gs.get('SHM229_ResumeWin')), gs.within(gs.get('SHM229_ResumeWin'), 0.001, 1.0e9))
        disconnect((nd, pin)); connect(gs.OR((g_, 'SHM228_Brake'), win), (nd, pin))
    out['snapshot'] = 'wired'
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = float(cdo.get_editor_property('SHM229_ResumeWin'))
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and out['knob'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V229_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('RESUME229 ' + json.dumps(out, default=str))
