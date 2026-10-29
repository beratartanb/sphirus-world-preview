"""probe237_fp.py (read-only): FootPlacement node(s) in ABP_GR_MotionMatchingBase FeetIK_Layer - input pins (bound / literal), the node's
pelvis / plant / interpolation settings structs, and the ABP CDO values of every FootPlacement plant-settings variable (PlantSettings_*),
to see which limit lowers the pelvis in a brake (V2.37 pelvis chain: FootPlacement + LegIK lower it 6 cm vs the clip). Prints FP237 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info, obj
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); g = graph(bp, 'FeetIK_Layer'); out = {'nodes': {}, 'cdo': {}}
for n in B.find_nodes(obj(pn(g))):
    if n.get_class().get_name() != 'AnimGraphNode_FootPlacement': continue
    p = pn(n); o = obj(p); nd = o.get_editor_property('node'); d = {'pins': {q.name: str(q.value)[:600] for q in info(p).input_pins}}
    for k in ('pelvis_settings', 'plant_settings', 'interpolation_settings', 'trace_settings', 'foot_definitions', 'leg_definitions'):
        try: d[k] = nd.get_editor_property(k).export_text()[:1500] if hasattr(nd.get_editor_property(k), 'export_text') else str(nd.get_editor_property(k))[:1500]
        except Exception as e: d[k] = 'ERR ' + str(e)[:80]
    out['nodes'][p.rsplit('.', 1)[-1]] = d
cdo = u.get_default_object(bp.generated_class())
for name in ['PlantSettings_Stops', 'PlantSettings_Default', 'PlantSettings_Turns', 'PlantSettings_Idle', 'PlantSettings_Moving', 'PlantSettings']:
    try:
        x = cdo.get_editor_property(name); out['cdo'][name] = x.export_text()[:1500] if hasattr(x, 'export_text') else str(x)[:1500]
    except Exception as e: out['cdo'][name] = 'ERR ' + str(e)[:60]
print('FP237 ' + json.dumps(out, default=str))
