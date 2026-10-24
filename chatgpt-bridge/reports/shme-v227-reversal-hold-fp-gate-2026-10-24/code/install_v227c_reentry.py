"""install_v227c_reentry.py (editor job) - V2.27 candidate, third pass (t2 j24_dbl, 115 cm): the component ended its episode while the body
was nearly stopped (speed 3 cm/s, forward request) and did NOT start a new one; the hold kept the F_B database and Motion Matching RE-ENTERED
clip starts every few frames (the remaining-time curve jumped back to ~1.9 s each time -> the hold never released, 5.5 s). A hold is only valid
for the clip instance the component's episode entered: a RE-ENTRY (curve value rising by > 0.05 s between frames while the component episode
is over) kills the hold (SHM227_Dead latch) until the component starts an episode again. SHM_Snapshot: SetSHM227_Dead before SetSHM227_Hold
(hold AND NOT (Dead OR revUp)); SetSHM227_PrevRev after SetSHM227_PrevRdT. Idempotent. builtins.V227_SAVE saves. Prints RH227C {...}."""
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
ensure_vars(bp, [('SHM227_Dead', 'bool', 'SHM227'), ('SHM227_PrevRev', 'float', 'SHM227')]); compile_ok(bp)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any('SetSHM227_Dead' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    rv = [p for p in sn if 'SetSHM227_Rev' in tid(p) and 'PrevRev' not in tid(p)]; assert len(rv) == 1, rv
    hd = [p for p in sn if 'SetSHM227_Hold' in tid(p)]; assert len(hd) == 1, hd
    pt = [p for p in sn if 'SetSHM227_PrevRdT' in tid(p)]; assert len(pt) == 1, pt
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'
    hse = [p for p in sn if tid(p).endswith('|GetHumanStateEnabled')]; assert hse, 'HumanStateEnabled getter'
    ct = (comp[0], 'ReturnValue')
    assert (rv[0], 'then') in src((hd[0], 'execute')), 'Hold does not follow Rev'
    revg = gs.get('SHM227_Rev')
    thr = gs.pure('MapRangeUnclamped', {'Value': gs.get('SHM227_PrevRev'), 'InRangeA': 0.0, 'InRangeB': 1.0, 'OutRangeA': 0.05, 'OutRangeB': 1.05})   # prev + 0.05
    revUp = gs.within(revg, thr, 1.0e9)                                   # remaining time went UP = Motion Matching re-entered a clip
    rdOn = gs.AND((hse[0], 'HumanStateEnabled'), gs.get('RedirectActive', COMP, ct))
    prevAct = gs.get('SHM_RedirectActive')
    dead = gs.OR(gs.AND(gs.get('SHM227_Dead'), gs.NOT(rdOn)), gs.AND(gs.AND(prevAct, gs.NOT(rdOn)), revUp))
    disconnect((hd[0], 'execute'))
    t1 = gs.set('SHM227_Dead', dead, (rv[0], 'then')); connect(t1, (hd[0], 'execute'))
    ho = src((hd[0], 'SHM227_Hold')); assert len(ho) == 1 and 'ANDBoolean' in tid(ho[0][0]), ho
    disconnect((hd[0], 'SHM227_Hold')); connect(gs.AND(ho[0], gs.NOT(gs.OR(gs.get('SHM227_Dead'), revUp))), (hd[0], 'SHM227_Hold'))
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (pt[0], 'then') in src((p, 'execute'))]; assert nxt
    for x in nxt: disconnect((x, 'execute'))
    t2 = gs.set('SHM227_PrevRev', gs.get('SHM227_Rev'), (pt[0], 'then'))
    for x in nxt: connect(t2, (x, 'execute'))
    out['snapshot'] = 'wired'
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM227_RevHold', 'SHM227_FPOff', 'SHM227_HoldExit', 'SHM227_FlatMax')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and out['knobs']['SHM227_RevHold'] == 0.0 and out['knobs']['SHM227_FPOff'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V227_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('RH227C ' + json.dumps(out, default=str))
