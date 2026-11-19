# b59.py: UE 5.9 shim for the 5.8 Python BlueprintTools API used by qa_graph / mj_common / g_common (editor_toolset removed it).
# exec this before g_common: it injects editor_toolset.toolsets.blueprint.BlueprintTools backed by unreal.BlueprintToolset.
import unreal as _u, editor_toolset.toolsets.blueprint as _m
_T = _u.BlueprintToolset
class BlueprintTools:
    get_graph = staticmethod(lambda bp, name: _T.get_graph(bp, name))
    find_nodes = staticmethod(lambda g, *a, **k: _T.find_nodes(g, *a, **k))
    _get_node_info = staticmethod(lambda n: _T.get_node_infos([n])[0])
    connect_pins = staticmethod(lambda a, b: _T.connect_pins(a, b))
    break_pins = staticmethod(lambda a, b: _T.disconnect_pins(a, b))
    set_pin_value = staticmethod(lambda p, v: _T.set_pin_value(p, v))
    create_node = staticmethod(lambda g, t, pos: _T.create_node(g, t, _u.IntPoint(int(pos[0]), int(pos[1])) if isinstance(pos, (tuple, list)) else pos))
    delete_node = staticmethod(lambda n: _T.delete_node(n))
    add_variable = staticmethod(lambda bp, n, t: _T.add_variable(bp, n, t))
    list_variables = staticmethod(lambda bp: [v.name for v in _T.list_variables(bp, None)])
    set_variable_instance_editable = staticmethod(lambda bp, n, v: _u.BlueprintEditorLibrary.set_blueprint_variable_instance_editable(bp, n, v))
    add_function_graph = staticmethod(lambda bp, n: _T.add_function_graph(bp, n))
    add_function_param = staticmethod(lambda g, n, t, i: _T.add_function_param(g, n, t, i))
    create = staticmethod(lambda d, n, p: _T.create(d, n, p))
    list_graphs = staticmethod(lambda bp: list(_T.list_graphs(bp)))
_m.BlueprintTools = BlueprintTools
