"""install243_turnlook.py (editor job, write manifest = BP_GR_Player + BP_PBI_Player): V2.43 standing-turn ownership rule.
V2.42 found the post-stop 90 deg swivel: the V2.34 loco frame explores one frame before release (a look-driven 90 deg strafe is inside
LocoExploreMin..Max 20..120), latches GR234_LocoYaw = travel yaw, and GR_UpdateIdleTurn (whose yaw reference became
Select(LocoOn, LocoYaw, control yaw) in V2.34) turns the standing body 90 deg toward a frame the body never reached while moving.
Rule (knob GR243_TurnNeedsLook, default False = unchanged): the explored locomotion frame alone never commands a STANDING turn; a
standing turn starts only when the player's look (control yaw) ALSO disagrees with the body by >= 42 deg (the smallest turn band).
  - strafe stop (control -71, body -78, LocoYaw -161): look agrees -> no turn, the body settles where it faces, LocoYaw is abandoned by
    the next look / input (V2.34 hold semantics unchanged while moving)
  - walk-explore stop (body already at LocoYaw): delta ~0 -> no turn, as before
  - player looks away >= 42 deg while standing: look and frame disagree -> turn, as before
Patch: GR_UpdateIdleTurn, the AND that starts a turn when no montage plays (K2Node_CommutativeAssociativeBinaryOperator_5): pin A
currently NOT(GR242 settle gate) [install242_turngate.py]; it becomes AND(that, NOT(GR243_TurnNeedsLook AND |Delta(control, actor).Yaw| < 42)).
Idempotent (marker variable). builtins.V243_SAVE saves. Prints TURNLOOK243 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
PAWN = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if p.get_name() in (PAWN, CHILD) or 'ABP_GR_MotionMatching' in p.get_name()]
if dirty: out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
pb = u.load_asset(PAWN)
if 'GR243_TurnNeedsLook' in [str(v) for v in B.list_variables(pb)]: out['patch'] = 'already'
else:
    assert 'GR242_TurnSettleGate' in [str(v) for v in B.list_variables(pb)], 'install242_turngate.py first'
    ensure_vars(pb, [('GR243_TurnNeedsLook', 'bool', 'GR243')]); compile_ok(pb); set_defaults(pb, {'GR243_TurnNeedsLook': False}); compile_ok(pb)
    gp = pn(graph(pb, 'GR_UpdateIdleTurn')); g = G(gp); gn = [pn(n) for n in B.find_nodes(obj(gp))]
    op5 = [p for p in gn if p.rsplit('.', 1)[-1] == 'K2Node_CommutativeAssociativeBinaryOperator_5']; assert len(op5) == 1, op5; op5 = op5[0]
    old = src((op5, 'A')); assert len(old) == 1, ('pin A source', old); out['A_before'] = old[0][0].rsplit('.', 1)[-1]
    disconnect((op5, 'A'))
    ctl = g.yaw(g.pure('Control')); body = g.yaw(g.pure('Body'))
    d = g.yaw(g.pure('NormalizedDeltaRotator', {'A': g.rot(ctl), 'B': g.rot(body)}))
    small = g.within(g.pure('Abs', {'A': d}), -1.0, 42.0)
    block = g.AND(g.get('GR243_TurnNeedsLook'), small)
    connect(g.AND(old[0], g.NOT(block)), (op5, 'A'))
    out['A_after'] = [s[0].rsplit('.', 1)[-1] for s in src((op5, 'A'))]
for name, a in (('pawn', pb), ('pawn_child', u.load_asset(CHILD))):
    st, errs = compile_ok(a); out[name] = [str(st), errs[:4]]
out['ok'] = all('UP_TO_DATE' in out[k][0] and not out[k][1] for k in ('pawn', 'pawn_child'))
if out['ok'] and getattr(builtins, 'V243_SAVE', False): save(pb, u.load_asset(CHILD)); out['saved'] = True
cdo = u.get_default_object(pb.generated_class()); out['defaults'] = {'needs_look': bool(cdo.get_editor_property('GR243_TurnNeedsLook')), 'settle_gate': bool(cdo.get_editor_property('GR242_TurnSettleGate'))}
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('TURNLOOK243 ' + json.dumps(out, default=str))
