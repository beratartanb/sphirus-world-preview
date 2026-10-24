"""install_v227_revhold.py (editor job) - V2.27 candidate: while an AUTHORED reversal clip (SHM226_JogRev_*, marker curve SHM226_Rev =
remaining clip seconds, add_revcurve227.py) is in the pose:
  (1) the ABP redirect episode (SHM_RedirectActive, frame counter SHM_RedirectFrames) is HELD past the component's episode end until the
      clip has SHM227_HoldExit s left (default 0.25) or the intent is released / a new component episode starts (knob SHM227_RevHold > 0.5).
      V2.26 measured: the component ends the episode at ~0.70 s, the ABP leaves the reversal database and Motion Matching jumps into the
      loop at another phase (12-13 cm planted-foot jump) about 0.9 s into a 1.8-2.0 s clip.
  (2) SHM_FootPlaceOff (already OR'ed into the FeetIK FootPlacement bypass since V1) is raised while the clip is in the pose, on flat ground
      only (|TerrainSlope| < SHM227_FlatMax deg, default 6; swing lifts < 2 cm) (knob SHM227_FPOff > 0.5). V2.26 measured: with FootPlacement
      off the designed foot path is realised within 6 cm; with it on the pinned brake foot is driven 23 cm backward and returned.
SHM_Snapshot (game thread) patch, graph-level (no DSL rebuild): after SetSHM_FootPlaceOff -> SetSHM227_Rev (GetCurveValue SHM226_Rev) ->
SetSHM227_Hold (hold condition, uses LAST frame's SHM_RedirectActive, i.e. the hold only continues an episode the component started);
SetSHM_FootPlaceOff value = fpOff expression; SetSHM_RedirectActive value = OR(old, SHM227_Hold); the frame counter's (or rdOn tailNow)
condition = OR(old, SHM227_Hold). Knobs default 0 = production behaviour unchanged (installed, OFF). Idempotent (SetSHM227_Rev present).
builtins.V227_SAVE saves. Prints RH227 {...}."""
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
ensure_vars(bp, [('SHM227_RevHold', 'float', 'SHM227'), ('SHM227_FPOff', 'float', 'SHM227'), ('SHM227_HoldExit', 'float', 'SHM227'), ('SHM227_FlatMax', 'float', 'SHM227'), ('SHM227_Rev', 'float', 'SHM227'), ('SHM227_Hold', 'bool', 'SHM227')]); compile_ok(bp)
cdo = u.get_default_object(bp.generated_class()); dfl = {}
if abs(float(cdo.get_editor_property('SHM227_HoldExit'))) < 1e-6: dfl['SHM227_HoldExit'] = 0.25
if abs(float(cdo.get_editor_property('SHM227_FlatMax'))) < 1e-6: dfl['SHM227_FlatMax'] = 6.0
if dfl: set_defaults(bp, dfl); compile_ok(bp)
out['defaults_set'] = dfl
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any('SetSHM227_Rev' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    fpo = [p for p in sn if 'SetSHM_FootPlaceOff' in tid(p)]; assert len(fpo) == 1, fpo
    ra = [p for p in sn if 'SetSHM_RedirectActive' in tid(p)]; assert len(ra) == 1, ra
    rf = [p for p in sn if 'SetSHM_RedirectFrames' in tid(p)]; assert len(rf) == 1, rf
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'
    ct = (comp[0], 'ReturnValue')
    assert not src((fpo[0], 'SHM_FootPlaceOff')), 'FootPlaceOff already driven'
    # --- frame counter: Set <- Select(reroute) .B <- Select(cStart) .B <- Select((or rdOn tailNow)) .bPickA <- OR
    s1 = src((rf[0], 'SHM_RedirectFrames')); assert len(s1) == 1 and 'SelectFloat' in tid(s1[0][0]), s1
    s2 = src((s1[0][0], 'B')); assert len(s2) == 1 and 'SelectFloat' in tid(s2[0][0]), s2
    s3 = src((s2[0][0], 'B')); assert len(s3) == 1 and 'SelectFloat' in tid(s3[0][0]), s3
    orn = src((s3[0][0], 'bPickA')); assert len(orn) == 1 and 'ORBoolean' in tid(orn[0][0]), orn
    out['frames_or'] = orn[0][0].rsplit('.', 1)[-1]
    rao = src((ra[0], 'SHM_RedirectActive')); assert len(rao) == 1 and 'ORBoolean' in tid(rao[0][0]), rao
    out['active_or'] = rao[0][0].rsplit('.', 1)[-1]
    # --- exec: after SetSHM_FootPlaceOff insert SetSHM227_Rev, SetSHM227_Hold
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (fpo[0], 'then') in src((p, 'execute'))]; assert nxt, 'next after FootPlaceOff'
    for x in nxt: disconnect((x, 'execute'))
    rev = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM226_Rev'})
    tail = gs.set('SHM227_Rev', rev, (fpo[0], 'then'))
    revg = gs.get('SHM227_Rev')
    holdOn = gs.within(gs.get('SHM227_RevHold'), 0.5, 1.0e9)
    remOK = gs.within(revg, gs.get('SHM227_HoldExit'), 1.0e9)            # clip has more than HoldExit s left (0 when no authored clip is in the pose)
    prevAct = gs.get('SHM_RedirectActive')                                # last frame's ABP episode state (set later in this chain)
    intent = gs.get('HasIntent', COMP, ct)
    hold = gs.AND(gs.AND(holdOn, remOK), gs.AND(prevAct, intent))
    tail = gs.set('SHM227_Hold', hold, tail)
    for x in nxt: connect(tail, (x, 'execute'))
    # --- FootPlaceOff value: FPOff knob & clip in pose & flat ground
    fpOn = gs.within(gs.get('SHM227_FPOff'), 0.5, 1.0e9)
    inClip = gs.within(revg, 0.001, 1.0e9)
    flat = gs.get('SHM227_FlatMax'); slope = gs.get('TerrainSlope', COMP, ct)
    flatOK = gs.within(slope, gs.mul(flat, -1.0), flat)
    liftOK = gs.AND(gs.within(gs.get('SwingLiftL', COMP, ct), -1.0e9, 2.0), gs.within(gs.get('SwingLiftR', COMP, ct), -1.0e9, 2.0))
    fpOff = gs.AND(gs.AND(fpOn, inClip), gs.AND(flatOK, liftOK))
    connect(fpOff, (fpo[0], 'SHM_FootPlaceOff'))
    # --- episode held: SHM_RedirectActive = OR(old, SHM227_Hold); frame counter condition = OR(old, SHM227_Hold)
    hg = gs.get('SHM227_Hold')
    disconnect((ra[0], 'SHM_RedirectActive')); connect(gs.OR(rao[0], hg), (ra[0], 'SHM_RedirectActive'))
    disconnect((s3[0][0], 'bPickA')); connect(gs.OR(orn[0], gs.get('SHM227_Hold')), (s3[0][0], 'bPickA'))
    out['snapshot'] = 'wired'
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM227_RevHold', 'SHM227_FPOff', 'SHM227_HoldExit', 'SHM227_FlatMax')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and out['knobs']['SHM227_RevHold'] == 0.0 and out['knobs']['SHM227_FPOff'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V227_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('RH227 ' + json.dumps(out, default=str))
