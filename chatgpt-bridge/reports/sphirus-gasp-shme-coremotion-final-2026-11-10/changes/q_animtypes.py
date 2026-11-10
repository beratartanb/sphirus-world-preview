import unreal as u
from editor_toolset.toolsets.blueprint import BlueprintTools as B
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'); g=B.get_graph(a,'AnimGraph'); ge=B.get_graph(a,'EventGraph')
for q in ('Modify','Dönüştür','LocalTo','ComponentTo','Yerel','Bileşen','Additive','Apply'):
    try: print('AT',q,[str(x) for x in B.find_node_types(g,q)][:14])
    except Exception as e: print('AT ERR',q,str(e)[:100])
for q in ('GetComponentByClass','Sin','GetWorldDeltaSeconds'):
    print('ET',q,[str(x) for x in B.find_node_types(ge,q)][:6])
