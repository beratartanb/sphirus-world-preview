import unreal as u, json
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, obj
out = {}
bp = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'); gp = graph(bp, 'AnimGraph')
for n in B.find_nodes(obj(pn(gp))):
    if n.get_class().get_name() != 'AnimGraphNode_LookAt': continue
    node = n.get_editor_property('node'); la = node.get_editor_property('look_at_axis')
    out['export'] = la.export_text(); out['dict'] = str(la.to_dict())[:300]
    out['axis_type'] = str(type(la.get_editor_property('axis')))
    try:
        c = u.Axis(); c.import_text('(Axis=Y,bInBoneSpace=True,CustomAxis=(X=0.0,Y=1.0,Z=0.0))'); out['import_ok'] = c.export_text()
    except Exception as e: out['import_err'] = str(e)[:200]
    try:
        c2 = u.Axis(); c2.set_editor_property('axis', 'Y'); out['set_str'] = c2.export_text()
    except Exception as e: out['set_str_err'] = str(e)[:200]
    break
print('AXIS2 ' + json.dumps(out))
