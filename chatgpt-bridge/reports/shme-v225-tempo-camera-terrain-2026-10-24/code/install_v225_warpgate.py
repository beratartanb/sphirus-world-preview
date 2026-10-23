"""install_v225_warpgate.py (editor job) - V2.25 R4: expose the MM blend-stack Stride Warping / Orientation Warping alphas as ABP variables
SHM225_SWAlpha / SHM225_OWAlpha (defaults = the node values: identical behaviour) so a reversal A/B can switch them, and the production
gate (authored JogRev clips already match the capsule) can drive them. Only connects pins that are not linked yet; reports otherwise.
builtins.V225_SAVE saves. Prints WG225 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json, re
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); out = {}
bsg = [g for g in B.list_graphs(bp) if g.get_name() == 'AnimationBlendStackGraph_0']; assert len(bsg) == 1, 'blend stack graph'; gp = pn(bsg[0]); gg = G(gp)
nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
sw = nodes['AnimGraphNode_StrideWarping_0']; ow = nodes['AnimGraphNode_OrientationWarping_1']
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def alpha_of(p):
    m = re.search(r'(?<![A-Za-z])Alpha=([-\d.]+)', obj(p).get_editor_property('node').export_text()); return float(m.group(1)) if m else 1.0
d_sw, d_ow = alpha_of(sw), alpha_of(ow); out['node_alpha'] = [d_sw, d_ow]
ensure_vars(bp, [('SHM225_SWAlpha', 'float', 'SHM225'), ('SHM225_OWAlpha', 'float', 'SHM225')]); compile_ok(bp)
set_defaults(bp, {'SHM225_SWAlpha': 1.0, 'SHM225_OWAlpha': 1.0})   # multipliers on the existing alpha sources
for p, var in ((sw, 'SHM225_SWAlpha'), (ow, 'SHM225_OWAlpha')):
    cur = src((p, 'Alpha'))
    if cur and 'MapRangeUnclamped' in tid(cur[0][0]): out[var] = 'already gated'; continue
    if cur:   # existing alpha source (curve / property access): alpha = existing x var, via MapRangeUnclamped (Multiply is a promotable operator)
        disconnect((p, 'Alpha'))
        m = gg.pure('/Script/Engine.KismetMathLibrary:MapRangeUnclamped', {'Value': cur[0], 'InRangeA': 0.0, 'InRangeB': 1.0, 'OutRangeA': 0.0, 'OutRangeB': gg.get(var)})
        connect(m, (p, 'Alpha')); out[var] = 'gated (existing source %s x var)' % cur[0][0].rsplit('.', 1)[-1]
    else: connect(gg.get(var), (p, 'Alpha')); out[var] = 'wired'
st, errs = compile_ok(bp); cpb = u.load_asset(CP); st2 = compile_ok(cpb)[0]
cdo = u.get_default_object(bp.generated_class()); out['cdo'] = [cdo.get_editor_property('SHM225_SWAlpha'), cdo.get_editor_property('SHM225_OWAlpha')]
out['status'] = [str(st), str(st2)]; out['errs'] = errs[:4]
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in str(st2); out['ok'] = ok
if ok and getattr(builtins, 'V225_SAVE', False): save(bp, cpb); out['saved'] = True
print('WG225 ' + json.dumps(out, default=str))
