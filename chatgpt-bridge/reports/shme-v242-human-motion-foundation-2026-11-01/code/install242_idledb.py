"""install242_idledb.py (editor job, write manifest = ABP_GR_MotionMatchingBase + child): V2.42 idle database hook for the
Locomotion Identity idle (SHM242_Idle_Weighted in PSD_SHM242_Idle). PoseSearchDatabase membership cannot be edited in memory on this
build (no 'animation_assets' property), so the swap is an ABP knob in the V2.40 wall-patch position (Update_MotionMatching entry, before
the existing chain):
  SHM242_IdleOn > 0.5 AND GetObjectName(CurrentSelectedDatabase) contains 'Stand_Idles'
      -> CurrentSelectedDatabase := SHM242_IdleDB; SetDatabaseToSearch(SHM242_IdleDB, InterruptOnDatabaseChangeAndInvalidateContinuingPose)
Defaults SHM242_IdleOn 0 / SHM242_IdleDB None = production unchanged. Idempotent (marker SHM242_IdleOn). builtins.V242_SAVE saves.
Prints IDLEDB242 {...}. Whether the later chooser route overrides this is verified by the run telemetry (av_Phase27_SelectedObject)."""
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
if dirty: out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP)
if 'SHM242_IdleOn' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM242_IdleOn', 'float', 'SHM242'), ('SHM242_IdleDB', u.PoseSearchDatabase.static_class(), 'SHM242')]); compile_ok(bp); set_defaults(bp, {'SHM242_IdleOn': 0.0}); compile_ok(bp)
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
    entry = [p for k, p in nodes.items() if k.startswith('K2Node_FunctionEntry')]; assert len(entry) == 1, entry; et = (entry[0], 'then')
    firsts = [p for p in nodes.values() if any(q.name == 'execute' for q in info(p).input_pins) and et in src((p, 'execute'))]
    assert len(firsts) == 1, firsts
    keep = [s_ for s_ in src((firsts[0], 'execute')) if s_ != et]
    sdb = [p for p in nodes.values() if 'SetDatabaseToSearch' in tid(p)]; mm = src((sdb[0], 'MotionMatchingNode')); assert mm; mm = mm[0]
    disconnect((firsts[0], 'execute'))
    nm = g.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': g.get('CurrentSelectedDatabase')})
    has = g.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': nm, 'Substring': 'Stand_Idles', 'bUseCase': False, 'bSearchFromEnd': False})
    cond = g.AND(g.within(g.get('SHM242_IdleOn'), 0.5, 10.0), has)      # no IsValid: not thread-safe in Update_MotionMatching; IdleOn and IdleDB are set together
    bt, be = g.branch(cond, et)
    sc = g.set('CurrentSelectedDatabase', g.get('SHM242_IdleDB'), bt)
    f1 = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(sc, (f1, 'execute')); connect(mm, (f1, 'MotionMatchingNode'))
    connect(g.get('SHM242_IdleDB'), (f1, 'Database')); arg(f1, 'InterruptMode', 'InterruptOnDatabaseChangeAndInvalidateContinuingPose')
    connect((f1, 'then'), (firsts[0], 'execute')); connect(be, (firsts[0], 'execute'))
    for s_ in keep: connect(s_, (firsts[0], 'execute'))
    out['patch'] = {'first': firsts[0].rsplit('.', 1)[-1], 'kept_links': len(keep), 'first_in_links': len(src((firsts[0], 'execute')))}
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V242_SAVE', False): save(bp, cpb); out['saved'] = True
cdo = u.get_default_object(bp.generated_class()); out['defaults'] = {'IdleOn': cdo.get_editor_property('SHM242_IdleOn'), 'IdleDB': str(cdo.get_editor_property('SHM242_IdleDB'))}
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('IDLEDB242 ' + json.dumps(out, default=str))
