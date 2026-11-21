# c_traj5.py (control, in-memory): ABP_Sph_GASP TrajectoryGenerationData_Idle.MaxControllerYawRate 100 -> builtins.TRJ_YAW (default 0).
# The idle trajectory extrapolated the camera yaw rate into the future facing. The capsule does not follow the camera when no input is
# held (free look), so releasing W while the camera still turns asked Motion Matching for a facing change that never happens: it picked
# Walk_Reface_Stop_180/090 or Stand_Turn_090 (body turned up to 59 deg away from the capsule and sprang back, 19-27 cm foot travel).
import unreal as u, builtins
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); c=u.get_default_object(a.generated_class())
v=c.get_editor_property('TrajectoryGenerationData_Idle'); old=v.get_editor_property('max_controller_yaw_rate')
v.set_editor_property('max_controller_yaw_rate', float(getattr(builtins,'TRJ_YAW',0.0) if getattr(builtins,'TRJ_YAW',None) is not None else 0.0)); c.set_editor_property('TrajectoryGenerationData_Idle', v)
print('TRAJ5 idle max yaw rate', old, '->', c.get_editor_property('TrajectoryGenerationData_Idle').get_editor_property('max_controller_yaw_rate'))
