exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
# c_plturn9.py (control job, in-memory build; saved later by a gated write job) on ABP_Sph_GASP - round 9.
# Quick A/D slide, part 3: when the turn command arrives while the leading foot is about to land, that foot touches down ~0.08 s earlier
# and ~30 cm shorter than the 180 turn clip's final plant. FootPlacement locks it, the clip keeps moving its foot to the wide plant
# position, the lock breaks at UnplantRadius 45 cm and the planted foot slides 33-53 cm on the ground. For turn / pivot databases (tag
# 'Pivots') a third plant setting set PlantSettings_Turns (= Default, UnplantRadius 85) keeps the foot where it really landed until the
# clip lifts it: a shorter, more upright pivot instead of a slide. Other databases keep PlantSettings_Default / _Stops unchanged.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
P='/Game/Sphirus/Player/GASP/ABP_Sph_GASP'; a=u.load_asset(P); have=[str(v) for v in B.list_variables(a)]
cdo=u.get_default_object(a.generated_class()); d0=cdo.get_editor_property('PlantSettings_Default'); d0.set_editor_property('unplant_radius',45.0); cdo.set_editor_property('PlantSettings_Default',d0)
if 'PlantSettings_Turns' in have: print('PLTURN9 already')
else:
    r=None
    for tn in ('FootPlacementPlantSettings','/Script/AnimationWarpingRuntime.FootPlacementPlantSettings','struct:/Script/AnimationWarpingRuntime.FootPlacementPlantSettings'):
        try:
            B.add_variable(a,'PlantSettings_Turns',tn); L.compile_blueprint(a)
            if 'PlantSettings_Turns' in [str(v) for v in B.list_variables(a)]: r=tn; break
        except Exception as e: print('PLTURN9 type fail',tn,repr(e)[:120])
    assert r, 'no type'; print('PLTURN9 var type',r)
    g=B.get_graph(a,'Get_FootPlacementPlantSettings'); N={str(pn(x)).split('.')[-1]:pn(x) for x in B.find_nodes(g)}
    sel=N['K2Node_Select_1']; arr=N['K2Node_CallArrayFunction_1']; gd=N['K2Node_VariableGet_7']; gt=N['K2Node_VariableGet_3']
    tsel=str(info(sel).type_id); tarr=str(info(arr).type_id); print('PLTURN9 types',tsel,'|',tarr)
    ge=GE(g); nv=ge.add_get_member_variable_node('PlantSettings_Turns',''); assert nv; nv.set_node_pos(u.IntPoint(-700,520)); nv=pn(nv)
    na=pn(B.create_node(g,tarr,(-700,700))); connect((gt,'CurrentDatabaseTags'),(na,'TargetArray')); value((na,'ItemToFind'),'Pivots')
    ns=pn(B.create_node(g,tsel,(-350,520)))
    disconnect((sel,'Option 0')); connect((gd,'PlantSettings_Default'),(ns,'Option 0')); connect((nv,'PlantSettings_Turns'),(ns,'Option 1')); connect((na,'ReturnValue'),(ns,'Index')); connect((ns,'ReturnValue'),(sel,'Option 0'))
    L.compile_blueprint(a); e=errs(a); print('PLTURN9 built ERR',e); assert not e
cdo=u.get_default_object(a.generated_class()); s=cdo.get_editor_property('PlantSettings_Default'); s.set_editor_property('unplant_radius',85.0); cdo.set_editor_property('PlantSettings_Turns',s)
d0=cdo.get_editor_property('PlantSettings_Default'); d0.set_editor_property('unplant_radius',45.0); cdo.set_editor_property('PlantSettings_Default',d0)
print('PLTURN9 default',cdo.get_editor_property('PlantSettings_Default').export_text()[97:130],'turns',cdo.get_editor_property('PlantSettings_Turns').export_text()[97:130])
