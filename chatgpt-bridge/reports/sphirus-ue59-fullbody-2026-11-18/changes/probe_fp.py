# probe_fp.py (read-only, editor): FootPlacement node settings in ABP_Sph_GASP -> Saved/UE59Work/probe/fp_node.txt
import unreal as u
a = u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP')
n = u.find_object(None, '/Game/Sphirus/Player/GASP/ABP_Sph_GASP.ABP_Sph_GASP:AnimGraph.AnimGraphNode_FootPlacement_0')
o = ['node %s' % n]
nd = n.get_editor_property('node')
for k in ('pelvis_settings', 'plant_settings', 'interpolation_settings', 'trace_settings', 'pelvis_bone', 'ik_foot_root_bone', 'plant_speed_mode', 'foot_definitions', 'leg_definitions'):
    try: v = nd.get_editor_property(k); o.append('%s = %s' % (k, v.export_text() if hasattr(v, 'export_text') else v))
    except Exception as e: o.append('%s ? %s' % (k, str(e)[:80]))
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/fp_node.txt', 'w').write('\n'.join(o)); print('FPNODE', len(o))
