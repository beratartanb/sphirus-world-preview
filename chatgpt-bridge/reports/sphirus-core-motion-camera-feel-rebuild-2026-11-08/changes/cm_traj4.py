# cm_traj4.py (write): the pose history collector kept only PoseCount=2 (then 4) poses at 0.04 s, i.e. 0.08-0.16 s of
# history. The query's past trajectory samples (-0.3 / -0.6 s) are clamped to the oldest stored pose, so the query
# always looked like "I have barely moved" and the start-clip acceleration windows won the search at every speed
# (trajectory-only experiment: Walk_Fwd_Start@0.5 chosen 74/90 frames at a steady 165 cm/s). PoseCount -> 24 (0.96 s).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
import re
d=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Driver'); ag=[g for g in B.list_graphs(d) if g.get_name()=='AnimGraph'][0]; n_=0
for n in B.find_nodes(ag):
    if 'HistoryCollector' in n.get_class().get_name():
        nd=n.get_editor_property('node'); t=str(nd.export_text()); t=re.sub(r'PoseCount=\d+','PoseCount=24',t); nd.import_text(t); n.set_editor_property('node',nd); n_+=1
        print('HC',re.findall(r'PoseCount=\d+|SamplingInterval=[0-9.]+|TrajectoryHistoryCount=\d+|TrajectoryPredictionCount=\d+|PredictionSamplingInterval=[0-9.]+|bGenerateTrajectory=\w+',str(n.get_editor_property('node').export_text())))
assert n_==1; L.compile_blueprint(d); print('ERR_D',errs(d)); assert not errs(d); assert EA.save_loaded_asset(d,False); print('DONE')
