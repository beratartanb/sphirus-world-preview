# q_dslwrite.py (write, scratch asset only): does write_graph_dsl work in this (Turkish) editor? Creates
# /Game/Sphirus/Player/Motion/_DSLProbe (ActorComponent), two float vars, a Tick body using arithmetic, compiles, reports.
import unreal as u
from editor_toolset.toolsets.blueprint import BlueprintTools as B
EA=u.EditorAssetLibrary; L=u.BlueprintEditorLibrary
P='/Game/Sphirus/Player/Motion/_DSLProbe'
bp=u.load_asset(P) if EA.does_asset_exist(P) else L.create_blueprint_asset_with_parent(P,u.ActorComponent)
for v in ('A','Bv'):
    if v not in [str(x) for x in B.list_variables(bp)]: B.add_variable(bp,v,'float')
L.compile_blueprint(bp)
g=B.get_graph(bp,'EventGraph')
print('DOC',B.write_graph_dsl.__doc__[:500])
for q in ('Tick','GetA','SetA','FInterpTo','GetOwner','GetVelocity','VectorLengthXY'):
    print('T',q,[str(x) for x in B.find_node_types(g,q)][:8])
dsl='''(event ReceiveTick (DeltaSeconds)
  (bind a (Değişkenler|Default|GetA))
  (Değişkenler|Default|SetBv (+ (* a 2.0) DeltaSeconds)))'''
try:
    r=B.write_graph_dsl(g,dsl); print('WRITE',r)
except Exception as e: print('WRITE ERR',str(e)[:800])
L.compile_blueprint(bp); print('STATUS',bp.get_editor_property('status'))
EA.save_loaded_asset(bp,False); print('DONE')
for m in ('add_event','add_variable','create_node','add_function_graph','add_function_param','set_pin_value'):
    print('DOC2',m,(getattr(B,m).__doc__ or '')[:350].replace('\n',' '))
