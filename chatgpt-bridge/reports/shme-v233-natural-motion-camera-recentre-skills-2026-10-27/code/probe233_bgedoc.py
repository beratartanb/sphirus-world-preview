import unreal as u
for m in ("create_and_edit_function_graph","add_graph_input_parameter","add_graph_output_parameter","add_return_node","set_is_pure_function","find_graph_entry_pin","get_graph_editor","get_graph_editor_by_name","create_node_from_name"):
    print("DOC", m, (getattr(u.BlueprintGraphEditor, m).__doc__ or "")[:500].replace(chr(10)," | "))
