"""install248_turnbind2.py (editor job, write manifest = ABP base + child; after install248_turnbind.py): release the turning-start hold
when the turn is done. Measured (v248tbreal ts r1/r2): the hold 'while inside PSD_SHM248_JogStartT' and the route 'search that database
while held' are circular -> the start database was searched for 2.2 s (TurnL135 to 1.9 s, then SHM237_JogStart_F), no run loop until the
stop. Patch: hold := SHM248_TurnStart AND in-database AND SHM238_T < SHM248_ReleaseT (89 = the normalised turn progress 1 deg short of the
end; the capsule heading has reached the request, the clip-bound contract and the LS block drop with the hold, the chooser's full list is
searched again with the turn clip tail as the continuing pose). Idempotent (variable SHM248_ReleaseT). builtins.V248_SAVE saves. Prints TURNBIND248B {...}."""
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
assert 'SHM248_Bind' in V, 'install248_turnbind.py first'
if 'SHM248_ReleaseT' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM248_ReleaseT', 'float', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM248_ReleaseT': 89.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    st = [p for p in sn if tid(p).endswith('|SetSHM248_TurnStart')]; assert len(st) == 1, st
    orn = src((st[0], 'SHM248_TurnStart')); assert len(orn) == 1, ('expected one source', orn)
    orn = orn[0][0]; ins = {q.name: src((orn, q.name)) for q in info(orn).input_pins if q.name in ('A', 'B')}
    assert ins['A'] and ins['B'], ins     # (commutative operator nodes carry no function name in type_id: identify by wiring)
    def direct_getter(n): return any(tid(s_[0]).endswith('|GetSHM248_TurnStart') for q in info(n).input_pins for s_ in src((n, q.name)) if q.name in ('A', 'B'))
    hold = [k for k in ('A', 'B') if direct_getter(ins[k][0][0])]; core = [k for k in ('A', 'B') if k not in hold]
    assert len(hold) == 1 and len(core) == 1, (hold, core)
    holdn = ins[hold[0]][0]; coren = ins[core[0]][0]
    disconnect((st[0], 'SHM248_TurnStart'))
    rel = gs.within(gs.get('SHM238_T'), -1.0, gs.get('SHM248_ReleaseT'))
    connect(gs.OR(coren, gs.AND(holdn, rel)), (st[0], 'SHM248_TurnStart')); out['hold_release'] = True
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: str(cdo.get_editor_property(k)) for k in ('SHM248_On', 'SHM248_ReleaseT')}
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knobs']['SHM248_On'] == '0.0'
if out['ok'] and getattr(builtins, 'V248_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('TURNBIND248B ' + json.dumps(out, default=str))
