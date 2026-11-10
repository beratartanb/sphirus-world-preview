# b5b_relaxed.py (write): rewire the Relaxed chooser node context: Self -> the table's context pin (Mover ABP type);
# break the orphaned CMC-typed pin. Compile must be clean, else the asset is not saved.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP_Rx')
for g in B.list_graphs(a):
    if g.get_name()!='Update_MotionMatching': continue
    for n in B.find_nodes(g):
        if type(n).__name__!='K2Node_EvaluateChooser2': continue
        p=pn(n); s=src((p,'SandboxCharacter_CMC_ABP_C')); print('OLD src',s); disconnect((p,'SandboxCharacter_CMC_ABP_C'))
        try: connect(s[0],(p,'SandboxCharacter_Mover_ABP_C')); print('CONNECTED self -> Mover pin')
        except Exception as e: print('CONNECT FAIL',str(e)[:300])
L.compile_blueprint(a); e=errs(a); print('ERR',e,'STATUS',a.get_editor_property('status'))
if not e: assert EA.save_loaded_asset(a,False); print('SAVED')
