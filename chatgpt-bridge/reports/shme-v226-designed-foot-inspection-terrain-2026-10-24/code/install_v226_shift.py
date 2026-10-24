"""install_v226_shift.py (editor job) - V2.26 T3b: the swing foot's IK target is shifted along the travel onto a step (world-space vector).
ABP_GR_MotionMatchingBase:
  vars SHM226_ShiftL / SHM226_ShiftR (Vector, cm, world) <- SHM_Snapshot copies the component's SwingShiftL / SwingShiftR (zero when
  HumanStateEnabled is off), written right after SHM224_LiftR (same pattern as the V2.24 lift).
  FeetIK_Layer: two 'Transform (Modify) Bone' nodes on ik_foot_l / ik_foot_r (translation ADDITIVE in WORLD space = the shift vector),
  inserted right after the V2.24 lift nodes and before the PBI pelvis ModifyBone_2 -> LegIK then solves the shifted target. The component
  holds the shift constant while the foot is planted, so FootPlacement's locked foot plus a constant shift stays still.
Idempotent (looks for the SHM226_ShiftL variable getter in FeetIK). The profile switch StepEdgeOn (SHME DA, default false) keeps the
vector at zero. builtins.V226_SAVE saves. Prints SH226 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, op, arg
from editor_toolset.toolsets.object import ObjectTools as O
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
MB = 'Animation|SkeletalControls|KemiğiDönüştürme(Değiştirme)'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name() in (AP, CP)]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
bp = u.load_asset(AP)
ensure_vars(bp, [('SHM226_ShiftL', 'Vector', 'SHM226'), ('SHM226_ShiftR', 'Vector', 'SHM226')]); compile_ok(bp)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def outpin(p): return [q.name for q in info(p).output_pins if q.name not in ('then',)][0]
# ---- 1. SHM_Snapshot: copy the component shifts (after SetSHM224_LiftR)
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any('SetSHM226_ShiftL' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    po = [p for p in sn if 'SetSHM224_LiftR' in tid(p)]; assert len(po) == 1, po
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'
    hs = [p for p in sn if tid(p).endswith('|GetHumanStateEnabled')]; assert hs, 'HumanStateEnabled getter'
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (po[0], 'then') in src((p, 'execute'))]; assert nxt
    for x in nxt: disconnect((x, 'execute'))
    tail = (po[0], 'then')
    for v, c in (('SHM226_ShiftL', 'SwingShiftL'), ('SHM226_ShiftR', 'SwingShiftR')):
        val = gs.pure('/Script/Engine.KismetMathLibrary:SelectVector', {'A': gs.get(c, COMP, (comp[0], 'ReturnValue')), 'bPickA': (hs[0], 'HumanStateEnabled')})   # B left unlinked = zero vector
        tail = gs.set(v, val, tail)
    for x in nxt: connect(tail, (x, 'execute'))
    out['snapshot'] = 'wired'
# ---- 2. FeetIK_Layer: shift nodes after the lift nodes
fik = graph(bp, 'FeetIK_Layer'); fp = pn(fik); gf = G(fp); fn_ = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(fp))}
def mbtxt(p):
    try: return obj(p).get_editor_property('node').export_text()
    except Exception: return ''
lifts = [p for p in fn_.values() if obj(p).get_class().get_name() == 'AnimGraphNode_ModifyBone' and 'BMM_Additive' in mbtxt(p) and 'BCS_ComponentSpace' in mbtxt(p) and ('ik_foot_l' in mbtxt(p) or 'ik_foot_r' in mbtxt(p))]
have = [p for p in fn_.values() if obj(p).get_class().get_name() == 'AnimGraphNode_ModifyBone' and 'BCS_WorldSpace' in mbtxt(p) and 'ik_foot_' in mbtxt(p)]
if have: out['feetik'] = 'already'
else:
    assert len(lifts) == 2, ('lift nodes', len(lifts))
    mb2 = fn_['AnimGraphNode_ModifyBone_2']; assert 'pelvis' in mbtxt(mb2)
    last = [p for p in lifts if (p, outpin(p)) in src((mb2, 'ComponentPose'))]; assert len(last) == 1, ('lift chain end', src((mb2, 'ComponentPose')))
    disconnect((mb2, 'ComponentPose')); tail = (last[0], outpin(last[0])); made = []
    for k, (bone, var) in enumerate((('ik_foot_l', 'SHM226_ShiftL'), ('ik_foot_r', 'SHM226_ShiftR'))):
        n = pn(B.create_node(obj(fp), MB, u.IntPoint(-1800 + 300 * k, -900)))
        rt = obj(n).get_editor_property('node')
        rt.import_text('(BoneToModify=(BoneName="%s"),Translation=(X=0.000000,Y=0.000000,Z=0.000000),TranslationMode=BMM_Additive,RotationMode=BMM_Ignore,ScaleMode=BMM_Ignore,TranslationSpace=BCS_WorldSpace,RotationSpace=BCS_ComponentSpace,ScaleSpace=BCS_ComponentSpace)' % bone)
        obj(n).set_editor_property('node', rt)
        t = obj(n).get_editor_property('node').export_text(); assert ('BoneName="%s"' % bone) in t and 'BMM_Additive' in t and 'BCS_WorldSpace' in t, t[:300]
        show = json.loads(O.get_properties(obj(n), ['ShowPinForProperties']))
        for o_ in show['ShowPinForProperties']:
            if o_['propertyName'] == 'Translation': o_['bShowPin'] = True
        O.set_properties(obj(n), json.dumps(show))
        connect(gf.get(var), (n, 'Translation')); connect(tail, (n, 'ComponentPose')); tail = (n, outpin(n)); made.append(n.rsplit('.', 1)[-1])
    connect(tail, (mb2, 'ComponentPose')); out['feetik'] = made
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child']
out['ok'] = ok
if ok and getattr(builtins, 'V226_SAVE', False): save(bp, cpb); out['saved'] = True
print('SH226 ' + json.dumps(out, default=str))
