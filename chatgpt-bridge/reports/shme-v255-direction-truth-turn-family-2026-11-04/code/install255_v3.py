"""install255_v3.py (editor job, write manifest = ABP base + child): V2.55 no free speed (knob SHM255_Ctl).
Measured (v255h60 fz_jog_m 30.6 s AS > SD, 209 cm/s): a plan entered below its approach speed took the clip's 300 cm/s at once: the capsule sped UP along the old travel for 0.27 s while the player asked to go
the other way. While the plan is still braking (curve SHM255_Phase < 0.5, SHM254_W > 0.3) the commanded speed can only fall: ClipSpeed := FMin(SHM228_Cmd, capsule speed).
Spliced after the first SetClipSpeed. Idempotent (variable SHM255_NoGain). builtins.V255_SAVE saves. Prints V3255 {...}."""
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
assert 'SHM255_CutMin' in V, 'install255_cut first'
if 'SHM255_NoGain' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM255_NoGain', 'bool', 'SHM')]); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    cs = [p for p in sn if tid(p).endswith('|SetClipSpeed') and any('SetSHM228_PrevDesV' in tid(s_[0]) for s_ in src((p, 'execute')))]; assert len(cs) == 1, cs; cs = cs[0]
    nx = succ(cs); assert len(nx) == 1 and len(src(nx[0])) == 1, nx; disconnect(nx[0])
    def curve(n): return gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': n})
    ctl = gs.within(gs.get('SHM255_Ctl'), 0.5, 1.0e9)
    brake = gs.AND(ctl, gs.AND(gs.within(curve('SHM254_W'), 0.3, 1.0e9), gs.within(curve('SHM255_Phase'), -1.0, 0.5)))
    spd = gs.pure(M + 'VSize', {'A': gs.pure('/Script/Engine.Actor:GetVelocity', {'self': gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')})})
    cmd = gs.get('SHM228_Cmd')
    t1 = gs.set('SHM255_NoGain', brake, (cs, 'then'))
    t2 = gs.set('ClipSpeed', gs.select(gs.get('SHM255_NoGain'), gs.pure(M + 'FMin', {'A': cmd, 'B': spd}), cmd), t1, COMP, ct)
    connect(t2, nx[0]); out['wired'] = cs.rsplit('.', 1)[-1]
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM255_Ctl'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V255_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('V3255 ' + json.dumps(out, default=str))
