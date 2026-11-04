"""install255_v4.py (editor job, write manifest = ABP base + child): V2.55 brake rate limit (knob SHM255_Ctl through SHM255_NoGain).
A plan entered mid-approach reads a clip speed below the capsule's; FMin alone would snap the capsule in one frame. While braking: ClipSpeed := FMax(ClipSpeed, capsule speed - SHM255_BrakeRate * dt): the capsule starts
slowing on the entry frame at a physical rate instead of holding full speed until the first planned contact (v255i60 fz_sprint_a: 0.30 s stalls at 490 cm/s) or jumping.
Spliced after the install255_v3 SetClipSpeed. Idempotent (variable SHM255_BrakeRate). builtins.V255_SAVE saves. Prints V4255 {...}."""
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
def succ(p, pin='then'):
    return [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for o in info(p).output_pins if str(o.name) == pin for q in o.connected_pins]
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
assert 'SHM255_NoGain' in V, 'install255_v3 first'
if 'SHM255_BrakeRate' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM255_BrakeRate', 'float', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM255_BrakeRate': 900.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    ng = [p for p in sn if tid(p).endswith('|SetSHM255_NoGain')]; assert len(ng) == 1, ng
    cs = [x[0] for x in succ(ng[0]) if tid(x[0]).endswith('|SetClipSpeed')]; assert len(cs) == 1, succ(ng[0]); cs = cs[0]
    nx = succ(cs); assert len(nx) == 1 and len(src(nx[0])) == 1, nx; disconnect(nx[0])
    spd = gs.pure(M + 'VSize', {'A': gs.pure('/Script/Engine.Actor:GetVelocity', {'self': gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')})})
    dt = gs.pure('/Script/Engine.GameplayStatics:GetWorldDeltaSeconds')
    floor_ = gs.sub(spd, gs.mul(gs.get('SHM255_BrakeRate'), dt))
    cur = gs.get('ClipSpeed', COMP, ct)
    t = gs.set('ClipSpeed', gs.select(gs.get('SHM255_NoGain'), gs.pure(M + 'FMax', {'A': cur, 'B': floor_}), cur), (cs, 'then'), COMP, ct)
    connect(t, nx[0]); out['wired'] = cs.rsplit('.', 1)[-1]
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM255_Ctl'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V255_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('V4255 ' + json.dumps(out, default=str))
