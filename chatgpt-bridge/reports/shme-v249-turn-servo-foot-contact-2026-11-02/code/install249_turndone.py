"""install249_turndone.py (editor job, write manifest = ABP base + child): latch the end of the turn.
Measured (v249j60 jstart rm, -180 request): at the cropped clip's end the blend-weight witness drops, SHM238_T reads 0 for a frame, the
hold (TurnStart AND crop AND T < ReleaseT) re-engages and the T2 start database is searched again -> a one-frame TurnR135 crop -> CP2
start (shoulder pop 69). Patch (SHM_Snapshot):
  SHM249_TurnDone := RM>0.5 AND crop AND (SHM249_TurnDone OR SHM238_T >= SHM248_ReleaseT)       (set after SetSHM248_TurnStart)
  hold term InRange(SHM238_T, -1, ReleaseT) -> AND(InRange(|SHM238_T|, ...), NOT SHM249_TurnDone)   (|T|: the V2.48 Turn curve is signed,
  left turns end at -90, so the old test dropped the hold as soon as a left turn began)
Idempotent (variable SHM249_TurnDone). builtins.V249_SAVE saves. Prints TURNDONE249 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def succ(p, pin='then'):
    return [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for o in info(p).output_pins if str(o.name) == pin for q in o.connected_pins]
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
assert 'SHM249_Kp' in V, 'V2.49 servo first'
if 'SHM249_TurnDone' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM249_TurnDone', 'bool', 'SHM')]); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    # the hold's InRange(SHM238_T, -1, ReleaseT)
    ir = [p for p in sn if 'InRange' in tid(p) and any(tid(s_[0]).endswith('|GetSHM238_T') for s_ in src((p, 'Value'))) and any(tid(s_[0]).endswith('|GetSHM248_ReleaseT') for s_ in src((p, 'Max')))]
    assert len(ir) == 1, ('hold InRange', [p.rsplit('.', 1)[-1] for p in ir])
    users = [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for o in info(ir[0]).output_pins if o.name == 'ReturnValue' for q in o.connected_pins]
    vsrc = src((ir[0], 'Value'))[0]; disconnect((ir[0], 'Value')); connect(gs.pure('/Script/Engine.KismetMathLibrary:Abs', {'A': vsrc}), (ir[0], 'Value'))   # T is signed by the clip (L -90 / R +90)
    for un, up in users: disconnect((un, up)); connect(gs.AND((ir[0], 'ReturnValue'), gs.NOT(gs.get('SHM249_TurnDone'))), (un, up))
    out['hold_users'] = len(users)
    st = [p for p in sn if tid(p).endswith('|SetSHM248_TurnStart')]; assert len(st) == 1, st
    nxt = succ(st[0]); assert nxt, 'TurnStart successor'
    for tn, tp in nxt: disconnect((tn, tp))
    crop = gs.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': gs.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': gs.get('Phase27_SelectedObject')}), 'Substring': '_crop', 'bUseCase': False, 'bSearchFromEnd': False})
    done = gs.AND(gs.AND(gs.within(gs.get('SHM249_RM'), 0.5, 1.0e9), crop), gs.OR(gs.get('SHM249_TurnDone'), gs.within(gs.pure('/Script/Engine.KismetMathLibrary:Abs', {'A': gs.get('SHM238_T')}), gs.get('SHM248_ReleaseT'), 1.0e9)))
    s1 = gs.set('SHM249_TurnDone', done, (st[0], 'then'))
    for tn, tp in nxt: connect(s1, (tn, tp))
    out['turndone'] = [a.rsplit('.', 1)[-1] for a, _ in nxt]
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V249_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('TURNDONE249 ' + json.dumps(out, default=str))
