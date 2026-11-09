# cm_traj3.py (write): the PoseHistory collector's TransformTrajectory input was wired to the driver variable
# 'Trajectory'. An external trajectory on that pin replaces the generated one, and the variable is never produced by a
# working source, so every search ran with an empty/stationary trajectory -> the search systematically preferred the
# slowest poses that fit the body (start-clip acceleration windows, idle turns) at every speed. Unlink the pin so the
# collector generates the trajectory from the character movement (bGenerateTrajectory=True, 26 x 0.04 s history,
# 6 x 0.25 s prediction). Also reports where 'Trajectory' is written in the event graph.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
_LF=open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/traj3_progress.txt','w')
def P(*a):
    print(*a); print(*a,file=_LF); _LF.flush()
d=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Driver'); ag=[g for g in B.list_graphs(d) if g.get_name()=='AnimGraph'][0]
ph=[n for n in B.find_nodes(ag) if 'HistoryCollector' in n.get_class().get_name()]; assert len(ph)==1; ph=pn(ph[0])
P('BEFORE',src((ph,'TransformTrajectory')))
disconnect((ph,'TransformTrajectory')); P('AFTER',src((ph,'TransformTrajectory')))
eg=B.get_graph(d,'EventGraph')
for n in B.find_nodes(eg):
    p=pn(n); i=info(p)
    if 'Trajectory' in str(i.type_id) or any(str(x.name)=='Trajectory' for x in list(i.input_pins)+list(i.output_pins)): P('EG',str(i.type_id)[-80:],[str(x.name) for x in i.input_pins][:6])
L.compile_blueprint(d); P('ERR_D',errs(d)); assert not errs(d); assert EA.save_loaded_asset(d,False); P('DONE')
