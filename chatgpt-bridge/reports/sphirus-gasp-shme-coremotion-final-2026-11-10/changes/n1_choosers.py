# n1_choosers.py (write): fix the per-frame LogChooser context error without touching vendor GASP assets.
#  - duplicate CHT_PoseSearchDatabases_Dense and CHT_CMCCharacterAnimations into /Game/Sphirus/Player/GASP/Choosers/
#  - copies: ContextData class SandboxCharacter_CMC_ABP_C -> ABP_Sph_GASP_C (InstancedStruct text import; other entries kept)
#  - ABP_Sph_GASP: Update_MotionMatching evaluates the Dense copy directly (the vendor root CHT_PoseSearchDatabases only
#    switches Dense/Sparse/ExtremeSparse by DDCvar.MMDatabaseLOD, which is 0 in Sphirus -> always Dense);
#    SetBlendStackAnimFromChooser evaluates the CMC copy.
import unreal as u
from editor_toolset.toolsets.blueprint import BlueprintTools as B
import sys,pathlib; sys.path.insert(0,str(pathlib.Path(u.Paths.project_dir())/'Saved/Codex/GraceRanger_QA_20260914/Scripts'))
from qa_graph import connect, disconnect, src, pn, info
EA=u.EditorAssetLibrary; L=u.BlueprintEditorLibrary; GE=u.BlueprintGraphEditor.get_graph_editor
D='/Game/Characters/UEFN_Mannequin/Animations/'; T='/Game/Sphirus/Player/GASP/Choosers/'
OLD='/Game/Blueprints/SandboxCharacter_CMC_ABP.SandboxCharacter_CMC_ABP_C'; NEW='/Game/Sphirus/Player/GASP/ABP_Sph_GASP.ABP_Sph_GASP_C'
PAIRS={D+'MotionMatchingData/CHT_PoseSearchDatabases_Dense':T+'CHT_Sph_PoseSearchDatabases_Dense',
       D+'ExperimentalStateMachineData/CHT_CMCCharacterAnimations':T+'CHT_Sph_CMCCharacterAnimations'}
copies={}
for s,d in PAIRS.items():
    c=u.load_asset(d) if EA.does_asset_exist(d) else EA.duplicate_asset(s,d); assert c,d
    new=[]
    for x in c.get_editor_property('context_data'):
        txt=str(x.export_text()); i=u.InstancedStruct(); assert i.import_text(txt.replace(OLD,NEW)),txt; new.append(i)
    c.set_editor_property('context_data',new)
    got=[str(x.export_text()) for x in c.get_editor_property('context_data')]
    assert NEW in got[0] and not any(OLD in g for g in got),got
    assert len(got)==len(new); print('CTX',d.split('/')[-1],[g[:150] for g in got])
    assert EA.save_loaded_asset(c,False); copies[s.split('/')[-1]]=c
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); n=0
for g in B.list_graphs(a):
    for nd in B.find_nodes(g):
        if nd.get_class().get_name()!='K2Node_EvaluateChooser2': continue
        cur=nd.get_editor_property('chooser'); cn=cur.get_name() if cur else None
        tgt={'CHT_PoseSearchDatabases':copies['CHT_PoseSearchDatabases_Dense'],'CHT_CMCCharacterAnimations':copies['CHT_CMCCharacterAnimations']}.get(cn)
        print('NODE',g.get_name(),cn,'->',tgt.get_name() if tgt else None)
        if not tgt: continue
        P=pn(nd); before=[str(x.name) for x in info(P).input_pins]; ctx=[x for x in before if 'Sandbox' in x]; assert len(ctx)==1,before
        S=src((P,ctx[0])); print('  pins before',before,'ctx src',S)
        nd.set_editor_property('chooser',tgt); L.compile_blueprint(a)
        after=[str(x.name) for x in info(P).input_pins]; nw=[x for x in after if 'Sph' in x and 'GASP' in x]; print('  pins after',after)
        assert len(nw)==1,after
        for s_ in S: connect(s_,(P,nw[0]))
        if ctx[0] in after:
            disconnect((P,ctx[0]))
            try: GE(g).remove_node_pin(nd,[x for x in info(P).input_pins if str(x.name)==ctx[0]][0]); print('  orphan removed')
            except Exception as e: print('  orphan remove skipped',str(e)[:120])
        print('  ctx now',src((P,nw[0]))); n+=1
assert n==2,n
L.compile_blueprint(a); e=[(g.get_name(),len(GE(g).list_nodes_with_errors())) for g in B.list_graphs(a) if GE(g).list_nodes_with_errors()]; print('ERR',e); assert not e
for g in B.list_graphs(a):
    for nd in B.find_nodes(g):
        if nd.get_class().get_name()=='K2Node_EvaluateChooser2': print('AFTER',g.get_name(),nd.get_editor_property('chooser').get_path_name())
assert EA.save_loaded_asset(a,False); print('DONE')
