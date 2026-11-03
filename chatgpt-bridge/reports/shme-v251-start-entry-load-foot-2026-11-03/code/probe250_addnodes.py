"""probe250_addnodes.py (measure job, read-only): what the additive / blend nodes of the ABP AnimGraph evaluate - BlendSpacePlayer_0 (mesh-space
additive on the Motion Matching output), SequenceEvaluator_3/4/5/13/14/15, BlendSpacePlayer_2, PoseSnapshot_2/4, LayeredBoneBlend_3,
Inertialization_0: asset, bound pins / property bindings (export text excerpt). Prints ADDNODES250 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info, obj, src
import json, re
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); out = {}
WANT = ('BlendSpacePlayer_0', 'BlendSpacePlayer_2', 'SequenceEvaluator_3', 'SequenceEvaluator_4', 'SequenceEvaluator_5', 'SequenceEvaluator_13', 'SequenceEvaluator_14', 'SequenceEvaluator_15',
        'PoseSnapshot_2', 'PoseSnapshot_4', 'LayeredBoneBlend_3', 'Inertialization_0', 'ApplyMeshSpaceAdditive_2', 'ApplyAdditive_1', 'ApplyAdditive_0', 'TwoWayBlend_0', 'TwoWayBlend_1', 'BlendListByBool_2', 'BlendListByBool_1')
g = [x for x in B.list_graphs(bp) if x.get_name() == 'AnimGraph'][0]
for n in B.find_nodes(g):
    p = pn(n); k = p.rsplit('.', 1)[-1].replace('AnimGraphNode_', '')
    if k not in WANT: continue
    o = obj(p); rec = {}
    try:
        t = o.get_editor_property('node').export_text()
        m = re.findall(r'(BlendSpace|Sequence|SnapshotName|Alpha|AlphaInputType|bAlphaBoolEnabled|ActualAlpha|LayerSetup)=([^,)]{0,160})', t); rec['props'] = m[:12]
    except Exception as e: rec['export_err'] = str(e)[:120]
    try:
        pins = []
        for q in info(p).input_pins:
            ss = src((p, q.name)); 
            if ss: pins.append('%s<-%s' % (q.name, ','.join(s_[0].rsplit('.', 1)[-1] + '.' + str(s_[1]) for s_ in ss)))
        rec['pins'] = pins
    except Exception as e: rec['pin_err'] = str(e)[:120]
    try:
        bnd = o.get_editor_property('property_bindings') if hasattr(o, 'property_bindings') else None
        rec['bindings'] = str(bnd)[:600] if bnd else None
    except Exception as e: rec['bind_err'] = str(e)[:100]
    out[k] = rec
print('ADDNODES250 ' + json.dumps(out, default=str))
