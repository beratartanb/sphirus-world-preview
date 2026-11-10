# b5_relaxed.py (write): ABP_Sph_GASP_Rx = copy of ABP_Sph_GASP whose motion-matching chooser node evaluates GASP's
# CHT_PoseSearchDatabases_Relaxed (Relaxed walk/run/sprint/idle set) instead of CHT_PoseSearchDatabases (Neutral, LOD tables).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
D='/Game/Sphirus/Player/GASP/'
a=EA.duplicate_asset(D+'ABP_Sph_GASP',D+'ABP_Sph_GASP_Rx') if not EA.does_asset_exist(D+'ABP_Sph_GASP_Rx') else u.load_asset(D+'ABP_Sph_GASP_Rx'); assert a
rx=u.load_asset('/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/CHT_PoseSearchDatabases_Relaxed'); n_=0
for g in B.list_graphs(a):
    if g.get_name()!='Update_MotionMatching': continue
    for n in B.find_nodes(g):
        if type(n).__name__!='K2Node_EvaluateChooser2': continue
        print('PROPS',[p for p in ('chooser','Chooser') if True])
        try: print('OLD',n.get_editor_property('chooser'))
        except Exception as e: print('OLD ERR',str(e)[:150])
        n.set_editor_property('chooser',rx); print('NEW',n.get_editor_property('chooser').get_name()); n_+=1
assert n_==1,n_
L.compile_blueprint(a); print('ERR',errs(a),'STATUS',a.get_editor_property('status')); assert EA.save_loaded_asset(a,False); print('DONE')
