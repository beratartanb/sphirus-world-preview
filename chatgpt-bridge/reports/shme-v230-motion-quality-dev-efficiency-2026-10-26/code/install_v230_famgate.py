"""install_v230_famgate.py (editor job) - V2.30: recovery family must not take over an authored clip that is still held.
Measured (v229fn2 vs v229fn3 j24_dbl, same build, two editor sessions): at the second-reversal exit the B_F clip was held (SHM227_Hold)
while the component episode had ended; in one session the component Family was 6 (recovery) and Update_MotionMatching's family branches
(IfThenElse_47 / _53 / _54 -> SHM_RecoveryDB / _L / _R, InterruptOnDatabaseChange) switched to SHM_Rec_F_Lfoot (23 cm slip), in the
other Family stayed 0 and the clip continued (16 cm). Change: those three branch conditions get AND NOT(FamGate & SHM227_Hold).
Knob SHM230_FamGate default 0 = V2.29 behaviour. Idempotent (variable SHM230_FGFix). builtins.V230_SAVE saves. Prints FAMGATE230 {...}."""
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
if 'SHM230_FGFix' in [str(v) for v in B.list_variables(bp)]:
    out['umm'] = 'already'
else:
    ensure_vars(bp, [('SHM230_FamGate', 'float', 'SHM230')]); compile_ok(bp)
    ug = pn(graph(bp, 'Update_MotionMatching')); gu = G(ug); un = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(ug))}
    done = {}
    for br, target in (('K2Node_IfThenElse_47', 'SHM_RecoveryDB'), ('K2Node_IfThenElse_53', 'SHM_RecoveryDB_L'), ('K2Node_IfThenElse_54', 'SHM_RecoveryDB_R')):
        b_ = un[br]; c_ = src((b_, 'Condition')); assert len(c_) == 1, (br, c_)
        # the true branch must lead to the recovery DB set (graph identity check)
        nx = [p for p in un.values() if any(q.name == 'execute' for q in info(p).input_pins) and (b_, 'then') in src((p, 'execute'))]
        assert any(any(target in tid(s[0]) for s in src((p, 'Database'))) for p in nx if 'SetDatabaseToSearch' in tid(p)), (br, 'target changed', [tid(p) for p in nx])
        gate = gu.AND(gu.within(gu.get('SHM230_FamGate'), 0.5, 1.0e9), gu.get('SHM227_Hold'))
        disconnect((b_, 'Condition')); connect(gu.AND(c_[0], gu.NOT(gate)), (b_, 'Condition')); done[br] = target
    ensure_vars(bp, [('SHM230_FGFix', 'bool', 'SHM230')])
    out['umm'] = done
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = float(cdo.get_editor_property('SHM230_FamGate'))
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and out['knob'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V230_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('FAMGATE230 ' + json.dumps(out, default=str))
