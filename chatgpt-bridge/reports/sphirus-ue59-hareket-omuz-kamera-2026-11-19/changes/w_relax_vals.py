# w_relax_vals.py (write, gated): verify the p3 relax chain on ABP_Sph_Body_GASP and store its parameters (builtins.RV or defaults).
import unreal as u, builtins
exec(open(u.Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
B = u.BlueprintToolset; L = u.BlueprintEditorLibrary; EA = u.EditorAssetLibrary
a = u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'); L.compile_blueprint(a); print('STATUS', a.get_editor_property('status'))
g = B.get_graph(a, 'EventGraph'); bad = [n for n in B.find_nodes(g) if 'Error' in str(n.get_editor_property('error_msg') if hasattr(n, 'error_msg') else '')]
ge = u.BlueprintGraphEditor.get_graph_editor(g); print('ERRNODES', len(ge.list_nodes_with_errors()))
vs = [v.name for v in B.list_variables(a, None)]; print('VARS', [v for v in vs if v.startswith(('VW_', 'VD_')) or v in ('MoveA', 'RelA', 'SpPrev', 'RelDecel', 'RelUp', 'RelDown')])
sets = [n for n in B.find_nodes(g) if B.get_node_infos([n])[0].type_id.startswith('Variables|Set') and any(p.name in ('RelA', 'MoveA', 'SpPrev') for p in B.get_node_infos([n])[0].input_pins)]
print('SETNODES', len(sets))
d = u.get_default_object(a.generated_class())
RV = getattr(builtins, 'RV', None) or {'RelDecel': 300.0, 'RelUp': 8.0, 'RelDown': 1.2}
for k, v in RV.items(): d.set_editor_property(k, u.Vector(*v) if isinstance(v, (tuple, list)) else v)
L.compile_blueprint(a)
try: EA.save_loaded_asset(a, False)
except RuntimeError as e: print('SAVE_SCRIPT_WARNING', str(e)[:160])
d = u.get_default_object(a.generated_class()); print('STORED', {k: str(d.get_editor_property(k)) for k in RV}); print('DONE')
