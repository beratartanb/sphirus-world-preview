# r7_jumpfilter.py (write) on ABP_Sph_GASP: the Relaxed chooser was authored for the Mover ABP, whose on-ground rows include
# jump-START databases (Mover predicts jumps on the ground). On the CMC character a fast mouse spin while walking picked
# M_Relaxed_Jump_RL_Start -> Land_Walk_Light (B_turns_pr1, ~1 s) with no jump. Fix on the Relaxed path only:
#   after SetValidDatabases(Relaxed result): if MovementMode == OnGround (E_MovementMode NewEnumerator0) remove
#   PSD_Relaxed_Stand_WalkAndRun_Jump / PSD_Relaxed_Stand_Sprint_Jump / PSD_Relaxed_Stand_Jump from ValidDatabases.
#   In the air the list is untouched (real jumps keep their in-air databases).
import unreal as u, sys, pathlib
sys.path.insert(0,str(pathlib.Path(u.Paths.project_dir())/'Saved/Codex/GraceRanger_QA_20260914/Scripts'))
from qa_graph import connect, disconnect, src, pn, info, value
from editor_toolset.toolsets.blueprint import BlueprintTools as B
EA=u.EditorAssetLibrary; L=u.BlueprintEditorLibrary; GE=u.BlueprintGraphEditor.get_graph_editor
D='/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/'
DBS=[u.load_asset(D+n) for n in ('PSD_Relaxed_Stand_WalkAndRun_Jump','PSD_Relaxed_Stand_Sprint_Jump','PSD_Relaxed_Stand_Jump')]; assert all(DBS)
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); g=B.get_graph(a,'Update_MotionMatching'); e=GE(g)
N=[pn(n) for n in B.find_nodes(g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]; outs=lambda p:[str(x.name) for x in info(p).output_pins]
rm=[t for t in B.find_node_types(g,'RemoveItem')]+[t for t in B.find_node_types(g,'Kaldır')]; print('RM types',rm[:12])
eq=[t for t in B.find_node_types(g,'Eşit(Enum)')]; print('EQ types',eq[:6])
rmt=[t for t in rm if 'Dizi' in t or 'Array' in t]; assert rmt,'no array remove type'; assert eq
sd=[p for p in N if tp(p).endswith('SetDatabasesToSearch')][0]
ex=src((sd,'execute')); print('SD exec src',ex)
# the Relaxed path setter = the SetValidDatabases fed by the evaluate node whose chooser is the Relaxed copy
rel=None
for n in B.find_nodes(g):
    if n.get_class().get_name()=='K2Node_EvaluateChooser2' and 'Relaxed' in n.get_editor_property('chooser').get_name(): rel=pn(n)
assert rel; sv=[p for p in N if tp(p).endswith('|SetValidDatabases') and src((p,'ValidDatabases')) and src((p,'ValidDatabases'))[0][0]==rel]; assert len(sv)==1,sv; sv=sv[0]
assert (sv,'then') in ex; disconnect((sd,'execute')); [connect(x,(sd,'execute')) for x in ex if x!=(sv,'then')]
q=pn(B.create_node(g,eq[0],u.IntPoint(900,900))); print('EQ pins',ins(q),outs(q))
gm=pn(e.add_get_member_variable_node('MovementMode','')); connect((gm,'MovementMode'),(q,ins(q)[0])); value((q,ins(q)[1]),'NewEnumerator0')
br=pn(e.add_branch_node()); connect((sv,'then'),(br,'execute')); connect((q,outs(q)[0]),(br,'Condition'))
t=(br,'then')
for db in DBS:
    r=pn(B.create_node(g,rmt[0],u.IntPoint(1100,900))); print('RM pins',ins(r),outs(r))
    gv=pn(e.add_get_member_variable_node('ValidDatabases','')); connect((gv,'ValidDatabases'),(r,[x for x in ins(r) if x not in ('execute','Item')][0]))
    L.compile_blueprint(a)
    value((r,'Item'),db.get_path_name()); connect(t,(r,'execute')); t=(r,'then')
connect(t,(sd,'execute')); connect((br,'else'),(sd,'execute'))
L.compile_blueprint(a); er=[(gg.get_name(),len(GE(gg).list_nodes_with_errors())) for gg in B.list_graphs(a) if GE(gg).list_nodes_with_errors()]; print('ERR',er); assert not er
exec(open(u.Paths.project_dir()+'Tools/GASP_20261109/gdump.py',encoding='utf8').read())
print('DUMP',gdump(g,u.Paths.project_dir()+'Tools/GASP_20261109/g_abp_umm2.txt'))
assert EA.save_loaded_asset(a,False); print('DONE')
