"""install_v229_pushcancel.py (editor job) - V2.29 sprint S->W control lock (found in the final production evidence, present since V2.28).
Measured (v229fin e29_load, also v229t4/t5 production): sprint W, S 1.4 s, W, S 1.4 s, W. On the last W the F_B clip was in its PUSH phase
(ct 1.54, designed speed -209 cm/s): a new component episode started (RevIntent 2 = the B_F family), the V2.28 against-intent safety fired
Dead for ONE frame (AgainstT 0.1 > 0.08), but Dead only latches while the component episode is inactive -> next frame the hold re-armed
on the same F_B clip with the OLD hold database, EntrySign re-latched to -1 (designed speed negative) so the push looked like a brake and
the safety never counted again: Motion Matching cycled late F_B frames (P20/P11, ct 1.3-1.66) and the clip-bound capsule ran BACKWARD at
210-255 cm/s for 2 s against a held W.
Change (SHM_Snapshot): the V2.28 cancel (new intent along the clip's brake direction -> re-route the hold database to the opposite family
with one interrupting search, EntrySign flipped, PrevRev disarmed) also fires in the PUSH phase once the against-intent timer runs:
Cancel := OR(old, PushCancel & inClip & (DesV*EntrySign < -1) & alongBrake & AgainstT > 0). The player asked for the old travel back
while the clip pushes the other way = exactly the cancel case; the opposite-family clip brakes the current motion and pushes along the
intent. Knob SHM229_PushCancel default 0 = V2.28 behaviour. Idempotent (variable SHM229_PCFix). builtins.V229_SAVE saves the ABPs.
Prints PUSHCANCEL229 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg, value
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
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
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
if 'SHM229_PCFix' in [str(v) for v in B.list_variables(bp)]:
    out['snapshot'] = 'already'
else:
    ensure_vars(bp, [('SHM229_PushCancel', 'float', 'SHM229')]); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    cs = [p for p in sn if 'SetSHM228_Cancel' in tid(p)]; assert len(cs) == 1, cs
    old = src((cs[0], 'SHM228_Cancel')); assert len(old) == 1, old
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'
    ct = (comp[0], 'ReturnValue')
    esg = gs.get('SHM228_EntrySign')
    inClip = gs.within(gs.get('SHM228_On'), 0.5, 1.0e9)
    push = gs.within(gs.mul(gs.get('SHM228_DesV'), esg), -1.0e9, -1.0)            # designed speed along the EXIT direction
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    fwd = gs.pure('/Script/Engine.Actor:GetActorForwardVector', {'self': pawn})
    ddir = gs.pure(M + 'Vector_Normal2D', {'A': gs.get('DesiredDir', COMP, ct), 'Tolerance': 0.0001})
    along = gs.pure(M + 'Dot_VectorVector', {'A': fwd, 'B': ddir})
    alongBrake = gs.within(gs.mul(along, esg), 0.3, 1.0e9)                        # intent along the old travel (brake) direction
    against = gs.within(gs.get('SHM228_AgainstT'), 0.001, 1.0e9)                  # the against-intent timer runs (this frame)
    knob = gs.within(gs.get('SHM229_PushCancel'), 0.5, 1.0e9)
    term = gs.AND(gs.AND(knob, inClip), gs.AND(gs.AND(push, alongBrake), against))
    disconnect((cs[0], 'SHM228_Cancel')); connect(gs.OR(old[0], term), (cs[0], 'SHM228_Cancel'))
    ensure_vars(bp, [('SHM229_PCFix', 'bool', 'SHM229')])
    out['snapshot'] = 'wired'
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = float(cdo.get_editor_property('SHM229_PushCancel'))
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and out['knob'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V229_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('PUSHCANCEL229 ' + json.dumps(out, default=str))
