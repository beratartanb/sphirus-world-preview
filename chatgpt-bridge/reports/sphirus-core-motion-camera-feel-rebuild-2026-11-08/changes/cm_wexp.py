# cm_wexp.py (write): schema weight experiment. Reads "traj pos vel_l vel_r head" from wexp.txt and sets the channel
# weights of PSS_Sph_Loco (trajectory channel, foot position, two foot velocities, pelvis heading); saves schema + DBs so
# the indices rebuild. Used to find out whether the search is driven by the trajectory or by the pose channels.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
w=[float(x) for x in open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/wexp.txt').read().split()]; assert len(w)==5,w
s=u.load_asset('/Game/Sphirus/Player/MM/PSS_Sph_Loco'); chs=s.get_editor_property('channels')
tr=[c for c in chs if c.get_class().get_name()=='PoseSearchFeatureChannel_Trajectory'][0]; tr.set_editor_property('weight',w[0])
grp=[c for c in chs if c.get_class().get_name()=='PoseSearchFeatureChannel_Group'][0]; subs=list(grp.get_editor_property('sub_channels'))
for c,v in zip(subs,w[1:]): c.set_editor_property('weight',v)
s.modify(); assert EA.save_loaded_asset(s,False)
print('WEIGHTS',tr.get_editor_property('weight'),[c.get_editor_property('weight') for c in subs])
for n in ('PSD_Sph_Loco2','PSD_Sph_Walk','PSD_Sph_Jog','PSD_Sph_Run','PSD_Sph_Crouch'):
    p='/Game/Sphirus/Player/MM/'+n
    if EA.does_asset_exist(p): EA.save_loaded_asset(u.load_asset(p),False)
print('DONE')
