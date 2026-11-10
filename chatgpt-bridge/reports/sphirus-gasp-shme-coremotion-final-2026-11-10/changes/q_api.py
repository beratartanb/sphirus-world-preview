import unreal as u
from editor_toolset.toolsets.blueprint import BlueprintTools as B
print('B',[m for m in dir(B) if not m.startswith('__')])
print('GE',[m for m in dir(u.BlueprintGraphEditor) if not m.startswith('_')])
bp=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASP_B'); g=B.get_graph(bp,'EventGraph'); e=u.BlueprintGraphEditor.get_graph_editor(g)
print('GEI',[m for m in dir(e) if not m.startswith('_')])
