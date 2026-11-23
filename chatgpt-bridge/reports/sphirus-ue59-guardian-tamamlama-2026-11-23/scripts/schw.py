import unreal as u, builtins
W=float(getattr(builtins,'SCHW',10.0))
s=u.load_asset('/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Schemas/PSS_Relaxed_Pivots')
for c in s.get_editor_property('channels'):
    if c.get_class().get_name()=='PoseSearchFeatureChannel_Trajectory':
        old=c.get_editor_property('weight'); c.set_editor_property('weight',W); print('SCHW',old,'->',c.get_editor_property('weight'))
try: u.PoseSearchLibrary  # touch
except Exception: pass
