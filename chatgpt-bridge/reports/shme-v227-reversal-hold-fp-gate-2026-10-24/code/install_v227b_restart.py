"""install_v227b_restart.py (editor job) - V2.27 candidate, second pass (t1 findings):
 (a) j24_dbl: a NEW component episode that starts on the frame the previous one ends (rdOn stays true) never resets the ABP frame counter
     (cStart = rdOn AND NOT PrevCompOn), so no bridge frame -> with the hold the Motion Matching stays in the OLD family database for the
     whole hold (5.5 s cycling through F_B clip starts, 118 cm). New: SHM227_Restart = holdOn AND rdOn AND component RedirectTime < last
     frame's (SHM227_PrevRdT) -> OR'ed into the cStart condition (frames back to 1 -> the bridge fires again with the new intent's database).
     Only while SHM227_RevHold > 0.5 (production unchanged).
 (b) j24_rel: FootPlacement off during the stop blend after a release let the foot slide 21 cm. New: SHM_FootPlaceOff also requires last
     frame's SHM_RedirectActive (FootPlacement returns the frame after the episode / hold ends).
Idempotent (SetSHM227_Restart present). builtins.V227_SAVE saves. Prints RH227B {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
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
ensure_vars(bp, [('SHM227_Restart', 'bool', 'SHM227'), ('SHM227_PrevRdT', 'float', 'SHM227')]); compile_ok(bp)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any('SetSHM227_Restart' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    hs = [p for p in sn if 'SetSHM227_Hold' in tid(p)]; assert len(hs) == 1, hs
    fpo = [p for p in sn if 'SetSHM_FootPlaceOff' in tid(p)]; assert len(fpo) == 1, fpo
    rf = [p for p in sn if 'SetSHM_RedirectFrames' in tid(p)]; assert len(rf) == 1, rf
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'
    ct = (comp[0], 'ReturnValue')
    # cStart = Select(reroute).B -> Select(cStart).bPickA
    s1 = src((rf[0], 'SHM_RedirectFrames')); assert len(s1) == 1 and 'SelectFloat' in tid(s1[0][0]), s1
    s2 = src((s1[0][0], 'B')); assert len(s2) == 1 and 'SelectFloat' in tid(s2[0][0]), s2
    cs = src((s2[0][0], 'bPickA')); assert len(cs) == 1 and 'ANDBoolean' in tid(cs[0][0]), cs
    out['cstart_and'] = cs[0][0].rsplit('.', 1)[-1]
    # (a) restart flag after SetSHM227_Hold
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (hs[0], 'then') in src((p, 'execute'))]; assert nxt
    for x in nxt: disconnect((x, 'execute'))
    rdt = gs.get('RedirectTime', COMP, ct)
    holdOn = gs.within(gs.get('SHM227_RevHold'), 0.5, 1.0e9)
    hse = [p for p in sn if tid(p).endswith('|GetHumanStateEnabled')]; assert hse, 'HumanStateEnabled getter'
    rdOn = gs.AND((hse[0], 'HumanStateEnabled'), gs.get('RedirectActive', COMP, ct))
    prevm = gs.pure('MapRangeUnclamped', {'Value': gs.get('SHM227_PrevRdT'), 'InRangeA': 0.0, 'InRangeB': 1.0, 'OutRangeA': -0.0005, 'OutRangeB': 0.9995})   # prev - 0.0005 (no promotable operator nodes)
    dropped = gs.within(rdt, -1.0e9, prevm)      # RedirectTime went DOWN = the component restarted its episode
    tail = gs.set('SHM227_Restart', gs.AND(gs.AND(holdOn, rdOn), dropped), (hs[0], 'then'))
    tail = gs.set('SHM227_PrevRdT', rdt, tail)
    for x in nxt: connect(tail, (x, 'execute'))
    disconnect((s2[0][0], 'bPickA')); connect(gs.OR(cs[0], gs.get('SHM227_Restart')), (s2[0][0], 'bPickA'))
    # (b) FootPlaceOff also needs last frame's ABP episode
    fo = src((fpo[0], 'SHM_FootPlaceOff')); assert len(fo) == 1 and 'ANDBoolean' in tid(fo[0][0]), fo
    disconnect((fpo[0], 'SHM_FootPlaceOff')); connect(gs.AND(fo[0], gs.get('SHM_RedirectActive')), (fpo[0], 'SHM_FootPlaceOff'))
    out['snapshot'] = 'wired'
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM227_RevHold', 'SHM227_FPOff', 'SHM227_HoldExit', 'SHM227_FlatMax')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and out['knobs']['SHM227_RevHold'] == 0.0 and out['knobs']['SHM227_FPOff'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V227_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('RH227B ' + json.dumps(out, default=str))
