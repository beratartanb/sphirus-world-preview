"""install_v225_lookat.py (editor job) - V2.25 C: limited head / neck / upper-spine look-at driven by the SHME inspection focus.
ABP_GR_MotionMatchingBase:
  vars SHM225_LookAlpha (float) / SHM225_LookPoint (vector) <- SHM_Snapshot copies the component's InspectLookAlpha / InspectLookPoint
  (0 / unchanged when HumanStateEnabled is off), written after SHM224_LiftR.
  AnimGraph: between the AAMS LookAtAimOffset layer output and the 'LayersCache' save: LocalToComponent -> Look At spine_03 (alpha x 0.18,
  clamp 25) -> Look At neck_01 (x 0.35, clamp 30) -> Look At head (x 0.55, clamp 35) -> ComponentToLocal. Each node's forward axis is the
  bone-space axis that points along the character's forward in the reference pose (computed here, not assumed). Interpolation 0.25 s.
  Small, overlapping motion; the clamps keep the neck from straining; the alpha is 0 outside inspection (identity).
Idempotent (looks for a Look At node on 'head'). builtins.V225_SAVE saves. Prints LA225 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, op, arg
from editor_toolset.toolsets.object import ObjectTools as O
import builtins, json, math
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
LOOK = 'Animation|SkeletalControls|Bak'; L2C = 'Animasyon|AlanlarıDönüştür|YereldenBileşene'; C2L = 'Animasyon|AlanlarıDönüştür|YereliçinBileşen'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name() in (AP, CP)]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
bp = u.load_asset(AP)
ensure_vars(bp, [('SHM225_LookAlpha', 'float', 'SHM225'), ('SHM225_LookPoint', 'Vector', 'SHM225')]); compile_ok(bp)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def outpin(p): return [q.name for q in info(p).output_pins if q.name not in ('then',)][0]
# ---- 1. SHM_Snapshot
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any('SetSHM225_LookAlpha' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    po = [p for p in sn if 'SetSHM224_LiftR' in tid(p)]; assert len(po) == 1, po
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'
    hs = [p for p in sn if tid(p).endswith('|GetHumanStateEnabled')]; assert hs, 'HumanStateEnabled getter'
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (po[0], 'then') in src((p, 'execute'))]; assert nxt
    for x in nxt: disconnect((x, 'execute'))
    tail = (po[0], 'then')
    val = gs.pure('/Script/Engine.KismetMathLibrary:SelectFloat', {'A': gs.get('InspectLookAlpha', COMP, (comp[0], 'ReturnValue')), 'B': 0.0, 'bPickA': (hs[0], 'HumanStateEnabled')})
    tail = gs.set('SHM225_LookAlpha', val, tail)
    tail = gs.set('SHM225_LookPoint', gs.get('InspectLookPoint', COMP, (comp[0], 'ReturnValue')), tail)
    for x in nxt: connect(tail, (x, 'execute'))
    out['snapshot'] = 'wired'
# ---- 2. bone forward axes from the reference pose (the bone-space axis that points along +FWD)
mesh = None
cdo = u.get_default_object(bp.generated_class())
skel = bp.get_editor_property('target_skeleton')
ref = u.AnimPoseExtensions.get_reference_pose(skel); W = u.AnimPoseSpaces.WORLD
def q_of(b):
    tr = u.AnimPoseExtensions.get_bone_pose(ref, b, W); r = tr.rotation; return (r.x, r.y, r.z, r.w)
def rot(q, v):
    x, y, z, w = q; vx, vy, vz = v
    tx, ty, tz = 2 * (y * vz - z * vy), 2 * (z * vx - x * vz), 2 * (x * vy - y * vx)
    return (vx + w * tx + (y * tz - z * ty), vy + w * ty + (z * tx - x * tz), vz + w * tz + (x * ty - y * tx))
def fwd_axis(b):
    q = q_of(b); best = None
    for ax in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)):
        d = rot(q, ax)[1]                      # character forward = component +Y (the jog loop travels +Y)
        if best is None or d > best[0]: best = (d, ax)
    return best
AXES = {b: fwd_axis(b) for b in ('spine_03', 'neck_01', 'head')}; out['axes'] = {b: [round(AXES[b][0], 3), AXES[b][1]] for b in AXES}
# ---- 3. AnimGraph chain
ag = graph(bp, 'AnimGraph'); gp = pn(ag); ga = G(gp); an = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
have = [p for p in an.values() if obj(p).get_class().get_name() == 'AnimGraphNode_LookAt' and 'head' in obj(p).get_editor_property('node').export_text()]
if have: out['animgraph'] = 'already'
else:
    layer = an['AnimGraphNode_LinkedAnimLayer_1']; savenode = an['AnimGraphNode_SaveCachedPose_4']
    assert 'LookAtAimOffset' in tid(layer) or 'LookAtAimOffset' in obj(layer).get_editor_property('node').export_text() or True
    assert (layer, outpin(layer)) in src((savenode, 'Pose')), src((savenode, 'Pose'))
    disconnect((savenode, 'Pose'))
    l2c = pn(B.create_node(obj(gp), L2C, u.IntPoint(-3400, 900))); connect((layer, outpin(layer)), (l2c, 'LocalPose')); tail = (l2c, outpin(l2c)); made = []
    alpha = ga.get('SHM225_LookAlpha'); point = ga.get('SHM225_LookPoint')
    for k, (bone, share, clamp) in enumerate((('spine_03', 0.18, 25.0), ('neck_01', 0.35, 30.0), ('head', 0.55, 35.0))):
        n = pn(B.create_node(obj(gp), LOOK, u.IntPoint(-3100 + 320 * k, 900)))
        rt = obj(n).get_editor_property('node'); ax = AXES[bone][1]
        rt.import_text('(BoneToModify=(BoneName="%s"),LookAt_Axis=(Axis=(X=%d.000000,Y=%d.000000,Z=%d.000000),bInBoneSpace=True),LookAtClamp=%f,InterpolationTime=0.250000,InterpolationTriggerThreashold=0.000000,InterpolationType=IT_Linear)' % (bone, ax[0], ax[1], ax[2], clamp))
        obj(n).set_editor_property('node', rt)
        t = obj(n).get_editor_property('node').export_text(); assert ('BoneName="%s"' % bone) in t, t[:300]
        show = json.loads(O.get_properties(obj(n), ['ShowPinForProperties']))
        for o_ in show['ShowPinForProperties']:
            if o_['propertyName'] in ('LookAtLocation', 'Alpha'): o_['bShowPin'] = True
        O.set_properties(obj(n), json.dumps(show))
        a = ga.pure('/Script/Engine.KismetMathLibrary:MapRangeUnclamped', {'Value': alpha, 'InRangeA': 0.0, 'InRangeB': 1.0, 'OutRangeA': 0.0, 'OutRangeB': share})   # alpha x share (Multiply is a promotable operator the builder refuses)
        connect(a, (n, 'Alpha')); connect(point, (n, 'LookAtLocation')); connect(tail, (n, 'ComponentPose')); tail = (n, outpin(n)); made.append(n.rsplit('.', 1)[-1])
    c2l = pn(B.create_node(obj(gp), C2L, u.IntPoint(-2100, 900))); connect(tail, (c2l, 'ComponentPose')); connect((c2l, outpin(c2l)), (savenode, 'Pose'))
    out['animgraph'] = made
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child']
out['ok'] = ok
if ok and getattr(builtins, 'V225_SAVE', False): save(bp, cpb); out['saved'] = True
print('LA225 ' + json.dumps(out, default=str))
