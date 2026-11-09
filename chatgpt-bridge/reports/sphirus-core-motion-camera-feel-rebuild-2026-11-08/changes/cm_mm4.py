# cm_mm4.py: selection stability. Driver clip identification showed steady walking served by start/stop clips with the walk
# loop rarely chosen, and running by the run start clip instead of the run loop. Database biases: continuing pose -0.12
# (stay on the current clip unless clearly better), looping -0.15 (prefer loops at steady speed). Node blend 0.25 -> 0.3 s.
import unreal as u, re
D='/Game/Sphirus/Player/MM'; E=u.EditorAssetLibrary
for n in ('PSD_Sph_Walk','PSD_Sph_Jog','PSD_Sph_Run','PSD_Sph_Crouch'):
    db=u.load_asset(D+'/'+n); db.set_editor_property('continuing_pose_cost_bias',-0.12); db.set_editor_property('looping_cost_bias',-0.15); assert E.save_loaded_asset(db,False); print('DB',n,'biases set')
exec(open(u.Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
d=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Driver'); ag=[g for g in B.list_graphs(d) if g.get_name()=='AnimGraph'][0]
for n in B.find_nodes(ag):
    if 'MotionMatching' in n.get_class().get_name():
        nd=n.get_editor_property('node'); t=str(nd.export_text()); t=re.sub(r'BlendTime=[0-9.]+','BlendTime=0.300000',t,1); nd.import_text(t); n.set_editor_property('node',nd); print('MM blend 0.3')
L.compile_blueprint(d); print('ERR_D',errs(d)); assert not errs(d); assert EA.save_loaded_asset(d,False); print('DONE')
