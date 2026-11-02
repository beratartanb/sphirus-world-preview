"""install248_loco.py (editor job, write manifest = ABP base + child; after install248_turnbind5.py): the locomotion frame follows the
turning start. Measured (v248tl60 j45_sl2 ts, cropped turn clip): the clip-bound heading ends at the request heading (-47) but the V2.34
locomotion frame (SHME component LocoYaw / LocoState, SHM_UpdateCameraV21) is still the LOOK frame (+43) until its own explore entry
(speed / hold conditions, 0.5-1 s later): the pawn slews the body back to +43 and strafes (A_CT_Jog_Left) before exploring to -47 again
-> a visible double turn and 20-30 cm slips. Patch (SHM_Snapshot, right after SetSHM248_TT, before SetSHM248_PostTurn):
  Branch( SHM248_On > 0.5 AND SHM248_PrevTS AND NOT SHM248_TurnStart )   (= the turn just completed)
    true -> component LocoExplore := true, LocoState := 1, LocoOn := true, LocoYaw := yaw(component Facing)   (the explored frame = the body)
so the pawn keeps the heading the turn produced and the explore state machine continues from there. Production (knob off) unchanged.
Idempotent (variable SHM248_Loco). builtins.V248_SAVE saves. Prints LOCO248 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
assert 'SHM248_PostTurn' in V, 'install248_turnbind5.py first'
if 'SHM248_Loco' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM248_Loco', 'bool', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM248_Loco': True}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'; ct = (comp[0], 'ReturnValue')
    tt = [p for p in sn if tid(p).endswith('|SetSHM248_TT')]; assert len(tt) == 1, tt
    nxt = [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for o in info(tt[0]).output_pins if str(o.name) == 'then' for q in o.connected_pins]
    assert nxt, 'no successor'; out['next'] = [a.rsplit('.', 1)[-1] for a, _ in nxt]
    for tn, tp in nxt: disconnect((tn, tp))
    cond = gs.AND(gs.within(gs.get('SHM248_On'), 0.5, 1.0e9), gs.AND(gs.get('SHM248_PrevTS'), gs.NOT(gs.get('SHM248_TurnStart'))))
    bt, bf = gs.branch(cond, (tt[0], 'then'))
    yaw = gs.yaw(gs.pure(M + 'MakeRotFromX', {'X': gs.get('Facing', COMP, ct)}))
    t1 = gs.set('LocoExplore', True, bt, COMP, ct); t2 = gs.set('LocoState', 1.0, t1, COMP, ct); t3 = gs.set('LocoOn', True, t2, COMP, ct); t4 = gs.set('LocoYaw', yaw, t3, COMP, ct)
    for tn, tp in nxt: connect(t4, (tn, tp)); connect(bf, (tn, tp))
    out['wired'] = True
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: str(cdo.get_editor_property(k)) for k in ('SHM248_On',)}
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knobs']['SHM248_On'] == '0.0'
if out['ok'] and getattr(builtins, 'V248_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('LOCO248 ' + json.dumps(out, default=str))
