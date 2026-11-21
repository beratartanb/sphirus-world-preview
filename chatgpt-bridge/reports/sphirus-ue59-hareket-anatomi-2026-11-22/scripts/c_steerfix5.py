# c_steerfix5.py (control, in-memory): restore the ProceduralTargetTime pin of Steering_0 under the Motion Matching node to its shipped
# value 1000000 (procedural steering off on that node). c_steerpin5.py had written 0.2 to both Motion Matching steering nodes; only
# Steering_1 (shipped 0.4) was meant to change.
import unreal as u
T = u.BlueprintToolset; a = u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); done = 0
for g in T.list_graphs(a):
    for n in T.find_nodes(g):
        if n.get_class().get_name() == 'AnimGraphNode_Steering' and 'MotionMatching_0' in n.get_path_name() and n.get_name().endswith('Steering_0'):
            inf = T.get_node_infos([n])[0]; P = {str(p.get_editor_property('name')): p for p in inf.get_editor_property('input_pins')}
            T.set_pin_value(P['ProceduralTargetTime'].get_editor_property('pin_id'), '1000000.0'); done += 1
            inf = T.get_node_infos([n])[0]; print('STEERFIX', n.get_name(), [str(p.get_editor_property('value')) for p in inf.get_editor_property('input_pins') if str(p.get_editor_property('name')) == 'ProceduralTargetTime'])
assert done == 1, done
u.BlueprintEditorLibrary.compile_blueprint(a); print('STEERFIX status', a.get_editor_property('status'))
