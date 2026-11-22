# c_mmblend6.py (control, in-memory): MotionMatching node BlendTime pin of ABP_Sph_GASP (builtins.MMBLEND, default 0.5 = saved value)
import unreal as u, builtins
T=u.BlueprintToolset; a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); v=float(getattr(builtins,'MMBLEND',0.5))
for g in T.list_graphs(a):
    for n in T.find_nodes(g):
        if n.get_class().get_name()=='AnimGraphNode_MotionMatching':
            for p in T.get_node_infos([n])[0].get_editor_property('input_pins'):
                if str(p.get_editor_property('name'))=='BlendTime':
                    print('MMBLEND old',p.get_editor_property('value'),T.set_pin_value(p.get_editor_property('pin_id'),'%.3f'%v))
u.BlueprintEditorLibrary.compile_blueprint(a)
for g in T.list_graphs(a):
    for n in T.find_nodes(g):
        if n.get_class().get_name()=='AnimGraphNode_MotionMatching':
            print('MMBLEND now',[p.get_editor_property('value') for p in T.get_node_infos([n])[0].get_editor_property('input_pins') if str(p.get_editor_property('name'))=='BlendTime'])
