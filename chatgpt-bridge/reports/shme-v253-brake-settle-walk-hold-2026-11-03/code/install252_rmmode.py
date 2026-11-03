"""install252_rmmode.py (editor job, write manifest = ABP base + child): V2.52 candidate owner of the 180 deg crop-end pop.
Measured (v252a60 jstart o / yt): the second-difference spike (shoulder -1.9 cm, pelvis -0.65 / -0.50 cm) sits on the FIRST frame after the
V2.49 owner releases (15.033), identical with and without the smooth yaw hand-over. At that frame the V2.49 snapshot switches
SetRootMotionMode from RootMotionFromEverything (while owned) to RootMotionFromMontagesOnly. Engine root motion is zero through the blend
stack (ResetRoot, V2.49), so the switch adds nothing but a change of root extraction on the pose.
Patch: the branch that selects RootMotionFromEverything gets AND (SHM252_KeepRM < 0.5); knob SHM252_KeepRM 1 keeps MontagesOnly all the
time (default 0 = production unchanged). Idempotent (variable SHM252_KeepRM). builtins.V252_SAVE saves. Prints RMMODE252 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
if 'SHM252_KeepRM' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM252_KeepRM', 'float', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM252_KeepRM': 0.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    fes = []
    for p in sn:
        if 'SetRootMotionMode' not in tid(p): continue
        vals = [str(q.value) for q in info(p).input_pins if str(q.name) == 'Value']
        out.setdefault('modes', []).append([p.rsplit('.', 1)[-1], vals])
        if vals and 'Everything' in vals[0]: fes.append(p)
    assert len(fes) == 1, fes
    ex = src((fes[0], 'execute')); assert len(ex) == 1, ex
    br = ex[0][0]; assert 'IfThenElse' in br, br
    c0 = src((br, 'Condition')); assert len(c0) == 1, c0
    disconnect((br, 'Condition')); connect(gs.AND(c0[0], gs.within(gs.get('SHM252_KeepRM'), -1.0e9, 0.5)), (br, 'Condition'))
    out['wired'] = {'branch': br.rsplit('.', 1)[-1], 'set': fes[0].rsplit('.', 1)[-1]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM252_KeepRM'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V252_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('RMMODE252 ' + json.dumps(out, default=str))
