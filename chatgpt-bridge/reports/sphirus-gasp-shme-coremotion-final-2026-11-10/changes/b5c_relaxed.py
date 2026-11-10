# b5c_relaxed.py (write): Sphirus copy of GASP's Relaxed chooser (CHT_Sph_Relaxed) with its context class set to
# ABP_Sph_GASP_Rx_C; the Rx AnimBP's chooser node evaluates that copy with Self as context. Vendor table untouched.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
D='/Game/Sphirus/Player/GASP/'
c=EA.duplicate_asset('/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/CHT_PoseSearchDatabases_Relaxed',D+'CHT_Sph_Relaxed') if not EA.does_asset_exist(D+'CHT_Sph_Relaxed') else u.load_asset(D+'CHT_Sph_Relaxed')
cd=c.get_editor_property('context_data'); print('CTX before',[str(x.export_text())[:200] for x in cd])
t="/Script/Chooser.ContextObjectTypeClass(Class=\"/Script/Engine.AnimBlueprintGeneratedClass'/Game/Sphirus/Player/GASP/ABP_Sph_GASP_Rx.ABP_Sph_GASP_Rx_C'\",Direction=ReadWrite)"
r=cd[0].import_text(t); print('IMPORT',r); c.set_editor_property('context_data',cd)
print('CTX after',[str(x.export_text())[:200] for x in c.get_editor_property('context_data')])
assert 'ABP_Sph_GASP_Rx' in str(c.get_editor_property('context_data')[0].export_text())
assert EA.save_loaded_asset(c,False); print('CHT saved')
a=u.load_asset(D+'ABP_Sph_GASP_Rx')
for g in B.list_graphs(a):
    if g.get_name()!='Update_MotionMatching': continue
    for n in B.find_nodes(g):
        if type(n).__name__!='K2Node_EvaluateChooser2': continue
        n.set_editor_property('chooser',c); p=pn(n)
        L.compile_blueprint(a)
        ins=[str(x.name) for x in info(p).input_pins]; print('PINS',ins)
        sf=[pn(x) for x in B.find_nodes(g) if type(x).__name__=='K2Node_Self'][0]
        for k in ins:
            if k not in ('execute',) : 
                try: disconnect((p,k))
                except Exception: pass
        tgt=[k for k in ins if 'ABP_Sph_GASP_Rx' in k or 'Rx' in k]; print('TARGET pin',tgt)
        connect((sf,'self'),(p,tgt[0])); print('CONNECTED')
L.compile_blueprint(a); e=errs(a); print('ERR',e,'STATUS',a.get_editor_property('status'))
assert not e; assert EA.save_loaded_asset(a,False); print('SAVED')
