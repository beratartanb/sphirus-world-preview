"""install_v230_earlyrev2.py (editor job) - V2.30 EarlyRev low bound, 'recently running' test widened: SpeedPeak > SHM230_EarlyRevPeak OR
component EffortEUse > 0.2 (walking never builds effort; a slow back-run after sprinting / the loaded family keeps SpeedPeak below the
walk-safe 145 - v230t9 e29_load lrL fell back to the vendor stand-sprint-pivot tail at 80 cm/s). Edits the select condition installed by
install_v230_earlyrev.py. Idempotent (SHM230_ERFix2). builtins.V230_SAVE saves. Prints EARLYREV2_230 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
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
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
vars_ = [str(v) for v in B.list_variables(bp)]
assert 'SHM230_ERFix' in vars_, 'install_v230_earlyrev.py first'
if 'SHM230_ERFix2' in vars_:
    out['mt'] = 'already'
else:
    mg = pn(graph(bp, 'SHM213_MontTick')); gm = G(mg); un = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(mg))}
    gt = un['K2Node_PromotableOperator_56']; bsrc = src((gt, 'B')); assert len(bsrc) == 1 and 'SelectFloat' in tid(bsrc[0][0]), [tid(x[0]) for x in bsrc]
    sel = bsrc[0][0]; cond = src((sel, 'bPickA')); assert len(cond) == 1 and 'AND' in tid(cond[0][0]).upper(), tid(cond[0][0])
    knob_term, peak_term = src((cond[0][0], 'A')), src((cond[0][0], 'B'))
    assert knob_term and peak_term
    comp = gm.pure('/Script/Engine.Actor:GetComponentByClass', {'self': gm.pure('/Script/Engine.AnimInstance:TryGetPawnOwner'), 'ComponentClass': COMP})
    eff = gm.within(gm.get('EffortEUse', COMP, comp), 0.2, 1.0e9)
    disconnect((sel, 'bPickA')); connect(gm.AND(knob_term[0], gm.OR(peak_term[0], eff)), (sel, 'bPickA'))
    ensure_vars(bp, [('SHM230_ERFix2', 'bool', 'SHM230')])
    out['mt'] = 'widened'
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child']
out['ok'] = ok
if ok and getattr(builtins, 'V230_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('EARLYREV2_230 ' + json.dumps(out, default=str))
