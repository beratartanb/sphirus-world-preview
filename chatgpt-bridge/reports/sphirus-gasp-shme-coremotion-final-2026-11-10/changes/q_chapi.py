import unreal as u
print('CH',[k for k in dir(u) if 'hooser' in k][:40])
print('IS',[k for k in dir(u) if 'InstancedStruct' in k][:10])
c=u.load_asset('/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/CHT_PoseSearchDatabases_Relaxed')
cd=c.get_editor_property('context_data'); x=cd[0]; print('ELEM',type(x).__name__,[m for m in dir(x) if not m.startswith('_')][:30])
