"""install237_fppelvis.py (editor job): ABP_GR_MotionMatchingBase FeetIK_Layer FootPlacement node: pelvis_settings.DisablePelvisCurveName =
'SHM237_FPPelvisOff' (was empty). No production clip carries this curve -> production behaviour unchanged (verified by an o run); a clip
that carries it (1 = on) keeps its own pelvis instead of the FootPlacement pelvis offset (V2.37 stop / start / re-push candidates).
builtins.V237_FPP = {'name': 'SHM237_FPPelvisOff' | '' (rollback)}. Prints FPP237 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
import builtins
from qa_graph import pn, obj
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
CP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching'
want = dict(getattr(builtins, 'V237_FPP', {'name': 'SHM237_FPPelvisOff'})); out = {'want': want}
bp = u.load_asset(AP); g = graph(bp, 'FeetIK_Layer')
nodes = [pn(n) for n in B.find_nodes(obj(pn(g))) if n.get_class().get_name() == 'AnimGraphNode_FootPlacement']; assert len(nodes) == 1, nodes
o = obj(nodes[0]); nd = o.get_editor_property('node'); ps = nd.get_editor_property('pelvis_settings')
out['before'] = str(ps.get_editor_property('disable_pelvis_curve_name'))
ps.set_editor_property('disable_pelvis_curve_name', want['name']); nd.set_editor_property('pelvis_settings', ps); o.set_editor_property('node', nd)
out['after'] = str(o.get_editor_property('node').get_editor_property('pelvis_settings').get_editor_property('disable_pelvis_curve_name'))
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:4]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
out['saved'] = False
if 'UP_TO_DATE' in str(st) and out['after'] == want['name']: save(bp, cpb); out['saved'] = True
print('FPP237 ' + json.dumps(out, default=str))
