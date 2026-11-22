# c_plant6.py (control, in-memory): FootPlacement plant settings of ABP_Sph_GASP (class defaults PlantSettings_Default / _Stops).
# builtins.PLANT = {'thr':..,'rad_def':..,'rad_stop':..,'ang':..}  (None keeps the value)
import unreal as u, builtins, re
P=dict(thr=25.0,rad_def=45.0,rad_stop=50.0,ang=90.0); P.update(getattr(builtins,'PLANT',None) or {})
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); cdo=u.get_default_object(a.generated_class())
for n,rk in (('PlantSettings_Default','rad_def'),('PlantSettings_Stops','rad_stop')):
    s=cdo.get_editor_property(n)
    if P['thr'] is not None: s.set_editor_property('speed_threshold',P['thr'])
    if P[rk] is not None: s.set_editor_property('unplant_radius',P[rk])
    if P['ang'] is not None: s.set_editor_property('unplant_angle',P['ang'])
    cdo.set_editor_property(n,s); print('PLANT',n,cdo.get_editor_property(n).export_text()[:150])
