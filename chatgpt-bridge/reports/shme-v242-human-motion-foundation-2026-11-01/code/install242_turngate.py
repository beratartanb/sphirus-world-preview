"""install242_turngate.py (editor job, write manifest = BP_GR_Player + BP_PBI_Player): V2.42 idle-turn settle gate.
Owner trace (V2.42, j41_rl / j42_lr lateral stops): the V2.34 locomotion frame starts exploring one frame before the stick is released
(LocoState 1 at 188 cm/s), so GR234_LocoYaw latches the TRAVEL yaw (-160.8) while the control yaw stays -71. When the capsule reaches
<= 5 cm/s, BP_GR_Player.GR_UpdateIdleTurn starts the 90 deg idle-turn montage (SHM_M_Neutral_Stand_Turn_090_L, root motion) toward
LocoYaw WHILE the stop clip is still playing with a planted foot -> the planted foot is dragged 32-38 cm (dyaw 101 deg) and the body
"swivels" right after the stop. No pawn yaw writer reads the stop clip's SHM_StopSettle curve (the V2.37 / V2.42 stops carry it = 1
until the settle ends).
Patch: GR_UpdateIdleTurn, the free literal pin A (= true) of K2Node_CommutativeAssociativeBinaryOperator_5 (the AND that starts a turn
when no montage plays) becomes NOT(GR242_TurnSettleGate AND GetCurveValue(AnimInstance, 'SHM_StopSettle') > 0.5). New pawn bool
GR242_TurnSettleGate, default False = production unchanged; the candidate sets it True (pawn_flags). The re-orientation itself (LocoYaw
hold, V2.34 design) is kept; it is only delayed until the stop has settled. Idempotent (marker variable). builtins.V242_SAVE saves.
Prints TURNGATE242 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
PAWN = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
# a dry run / earlier compile may have left the pawn or the ABPs dirty: start from disk
dirty = [p for p in LS.get_dirty_content_packages() if p.get_name() in (PAWN, CHILD) or 'ABP_GR_MotionMatching' in p.get_name()]
if dirty: out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
pb = u.load_asset(PAWN)
if 'GR242_TurnSettleGate' in [str(v) for v in B.list_variables(pb)]: out['patch'] = 'already'
else:
    ensure_vars(pb, [('GR242_TurnSettleGate', 'bool', 'GR242')]); compile_ok(pb); set_defaults(pb, {'GR242_TurnSettleGate': False}); compile_ok(pb)
    gp = pn(graph(pb, 'GR_UpdateIdleTurn')); g = G(gp); gn = [pn(n) for n in B.find_nodes(obj(gp))]
    op5 = [p for p in gn if p.rsplit('.', 1)[-1] == 'K2Node_CommutativeAssociativeBinaryOperator_5']; assert len(op5) == 1, op5; op5 = op5[0]
    pa = [q for q in info(op5).input_pins if q.name == 'A']; assert pa, [q.name for q in info(op5).input_pins]
    out['op5_A_before'] = {'value': str(pa[0].value), 'src': src((op5, 'A'))}
    assert not src((op5, 'A')) and str(pa[0].value).lower() in ('true', '1'), out['op5_A_before']
    ai = [p for p in gn if tid(p).endswith('GetAnimInstance')]; assert len(ai) >= 1, 'no GetAnimInstance in GR_UpdateIdleTurn'
    out['anim_instance_node'] = ai[0].rsplit('.', 1)[-1]
    curve = g.pure('/Script/Engine.AnimInstance:GetCurveValue', {'self': (ai[0], 'ReturnValue'), 'CurveName': 'SHM_StopSettle'})
    settling = g.within(curve, 0.5, 2.0)                      # InRange (the '>' operator is a promotable node qa_graph refuses)
    gate = g.AND(g.get('GR242_TurnSettleGate'), settling)
    connect(g.NOT(gate), (op5, 'A'))
    out['op5_A_after'] = src((op5, 'A'))
for name, a in (('pawn', pb), ('pawn_child', u.load_asset(CHILD))):
    st, errs = compile_ok(a); out[name] = [str(st), errs[:4]]
out['ok'] = all('UP_TO_DATE' in out[k][0] and not out[k][1] for k in ('pawn', 'pawn_child'))
if out['ok'] and getattr(builtins, 'V242_SAVE', False): save(pb, u.load_asset(CHILD)); out['saved'] = True
cdo = u.get_default_object(pb.generated_class()); out['default'] = bool(cdo.get_editor_property('GR242_TurnSettleGate'))
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('TURNGATE242 ' + json.dumps(out, default=str))
