# r1_relaxed_abp.py (write): Relaxed GASP family selectable in ABP_Sph_GASP (default OFF = production unchanged).
#  - CHT_PoseSearchDatabases_Relaxed -> /Game/Sphirus/Player/GASP/Choosers/CHT_Sph_PoseSearchDatabases_Relaxed (context ABP_Sph_GASP_C)
#  - ABP var SphRelaxed (bool, instance editable). Update_MotionMatching: Branch(SphRelaxed)
#      false -> existing Dense copy eval -> SetValidDatabases ; true -> Relaxed copy eval -> SetValidDatabases
#      SetDatabasesToSearch.Databases <- Get ValidDatabases (both paths)
import unreal as u, sys, pathlib
sys.path.insert(0,str(pathlib.Path(u.Paths.project_dir())/'Saved/Codex/GraceRanger_QA_20260914/Scripts'))
from qa_graph import connect, disconnect, src, pn, info, value
from editor_toolset.toolsets.blueprint import BlueprintTools as B
EA=u.EditorAssetLibrary; L=u.BlueprintEditorLibrary; GE=u.BlueprintGraphEditor.get_graph_editor
S='/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/CHT_PoseSearchDatabases_Relaxed'; T='/Game/Sphirus/Player/GASP/Choosers/CHT_Sph_PoseSearchDatabases_Relaxed'
OLD='/Game/Blueprints/SandboxCharacter_Mover_ABP.SandboxCharacter_Mover_ABP_C'; NEW='/Game/Sphirus/Player/GASP/ABP_Sph_GASP.ABP_Sph_GASP_C'
c=u.load_asset(T) if EA.does_asset_exist(T) else EA.duplicate_asset(S,T); assert c
new=[]
for x in c.get_editor_property('context_data'):
    i=u.InstancedStruct(); assert i.import_text(str(x.export_text()).replace(OLD,NEW)); new.append(i)
c.set_editor_property('context_data',new); got=[str(x.export_text()) for x in c.get_editor_property('context_data')]
assert NEW in got[0] and OLD not in got[0],got; print('CTX',got[0][:160]); assert EA.save_loaded_asset(c,False)
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP')
if 'SphRelaxed' not in [str(v) for v in B.list_variables(a)]: B.add_variable(a,'SphRelaxed','bool')
B.set_variable_instance_editable(a,'SphRelaxed',True); L.compile_blueprint(a)
g=B.get_graph(a,'Update_MotionMatching'); e=GE(g); N=[pn(n) for n in B.find_nodes(g)]; tp=lambda p:str(info(p).type_id)
ins=lambda p:[str(x.name) for x in info(p).input_pins]; outs=lambda p:[str(x.name) for x in info(p).output_pins]
entry=[p for p in N if tp(p).endswith('|Update_MotionMatching')][0]
ev=[p for p in N if 'SeçiciyiDeğerlendir' in tp(p)]; assert len(ev)==1,ev; ev=ev[0]
sv=[p for p in N if tp(p).endswith('|SetValidDatabases')][0]; sd=[p for p in N if tp(p).endswith('SetDatabasesToSearch')][0]
selfn=[p for p in N if 'KendineReferans' in tp(p)][0]
evn=[n for n in B.find_nodes(g) if pn(n)==ev][0]
print('EV props mode',evn.get_editor_property('mode'))
# Branch
br=pn(e.add_branch_node()); disconnect((ev,'execute')) if False else None
assert src((ev,'execute'))==[(entry,'then')],src((ev,'execute'))
disconnect((ev,'execute')); connect((entry,'then'),(br,'execute')); connect((br,'else'),(ev,'execute'))
gv=pn(e.add_get_member_variable_node('SphRelaxed','')); connect((gv,'SphRelaxed'),(br,'Condition'))
# new evaluate node
et=[t for t in B.find_node_types(g,'SeçiciyiDeğerlendir')]; print('EVAL types',et[:4])
n2=B.create_node(g,et[0],u.IntPoint(400,600)); n2.set_editor_property('chooser',c); n2.set_editor_property('mode',evn.get_editor_property('mode'))
L.compile_blueprint(a); p2=pn(n2); print('NEW pins in',ins(p2),'out',outs(p2))
ctxp=[x for x in ins(p2) if 'GASP' in x]; assert len(ctxp)==1,ins(p2); connect((selfn,'self'),(p2,ctxp[0]))
connect((br,'then'),(p2,'execute'))
s2=pn(e.add_set_member_variable_node('ValidDatabases','')); connect((p2,'execute') if 'then' not in outs(p2) else (p2,'then'),(s2,'execute'))
connect((p2,'Result'),(s2,'ValidDatabases')); connect((s2,'then'),(sd,'execute'))
disconnect((sd,'Databases')); gdb=pn(e.add_get_member_variable_node('ValidDatabases','')); connect((gdb,'ValidDatabases'),(sd,'Databases'))
L.compile_blueprint(a); er=[(gg.get_name(),len(GE(gg).list_nodes_with_errors())) for gg in B.list_graphs(a) if GE(gg).list_nodes_with_errors()]; print('ERR',er); assert not er
print('SD exec src',src((sd,'execute')),'DB src',src((sd,'Databases')))
cdo=u.get_default_object(a.generated_class()); print('DEFAULT SphRelaxed',cdo.get_editor_property('SphRelaxed'))
assert EA.save_loaded_asset(a,False); print('DONE')
