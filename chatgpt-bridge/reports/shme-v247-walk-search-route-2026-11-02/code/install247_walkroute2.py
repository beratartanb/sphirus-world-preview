"""install247_walkroute2.py (editor job, write manifest = ABP base + child; after install247_walkroute.py): the route kick must happen only
at the ENTRY of a Dense forward loop (hand-over from the CP start, a steering restart), never mid-stride: at real time the V2.47 hook kicked
a loop entered at 2.73 s (30 deg restart) and forced SHM245@0.04 after the hand-over -> 24.7 / 28.3 cm foot drags that 30 FPS never showed.
Patch: Branch condition := old AND InRange(Phase27_SelectedTime, -1, SHM247_EntryWindow(0.12)). Idempotent (variable marker).
builtins.V247_SAVE saves. Prints WALKROUTE247B {...}."""
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
bp = u.load_asset(AP); assert 'SHM247_WalkOn' in [str(v) for v in B.list_variables(bp)], 'install247_walkroute.py first'
if 'SHM247_EntryWindow' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM247_EntryWindow', 'float', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM247_EntryWindow': 0.12}); compile_ok(bp)
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
    # the hook's branch = the exec successor of the chooser's SetDatabasesToSearch (K2Node_CallFunction_2): CF2.then -> hook Branch
    cf2 = nodes['K2Node_CallFunction_2']; assert 'SetDatabasesToSearch' in tid(cf2), tid(cf2)
    nxt = [p for p in nodes.values() if any(q.name == 'execute' for q in info(p).input_pins) and (cf2, 'then') in src((p, 'execute'))]
    assert len(nxt) == 1 and 'IfThenElse' in nxt[0], ('CF2 successor', [p.rsplit('.', 1)[-1] for p in nxt])
    br = nxt[0]; cs = src((br, 'Condition')); assert cs, ('condition', cs); andn = cs[0][0]; target = (br, andn)
    assert target, 'hook branch not found'; br, andn = target; out['branch'] = br.rsplit('.', 1)[-1]
    disconnect((br, 'Condition'))
    newc = g.AND((andn, 'ReturnValue'), g.within(g.get('Phase27_SelectedTime'), -1.0, g.get('SHM247_EntryWindow')))
    connect(newc, (br, 'Condition')); out['condition_after'] = [s_[0].rsplit('.', 1)[-1] for s_ in src((br, 'Condition'))]
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V247_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('WALKROUTE247B ' + json.dumps(out, default=str))
