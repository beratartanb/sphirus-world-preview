# w_cm18.py (write, gated, manifest ue59_m18_cm): ABP_Sph_GASP remap gets Relaxed_Stand_Sprint_Stops -> Dense_Stand_Sprint_Stops.
# The Idle chooser row offers every stop database at once; a 415 jog release often scores the sprint stops best, so the sprint-stop
# family decides the jog stop. Dense (Neutral) sprint stops drop the pelvis 20 cm from a jog instead of 29 (runtime test T_STOP_ds).
import unreal as u
L = u.BlueprintEditorLibrary; EAL = u.EditorAssetLibrary
R = '/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/'
k = u.load_asset(R + 'Relaxed/PSD_Relaxed_Stand_Sprint_Stops'); v = u.load_asset(R + 'Dense/PSD_Dense_Stand_Sprint_Stops'); assert k and v
a = u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); c = u.get_default_object(a.generated_class())
ks = list(c.get_editor_property('CM_Keys')); vs = list(c.get_editor_property('CM_Vals')); print('BEFORE', len(ks), len(vs))
names = [x.get_path_name() for x in ks]
if k.get_path_name() in names: vs[names.index(k.get_path_name())] = v
else: ks.append(k); vs.append(v)
c.set_editor_property('CM_Keys', ks); c.set_editor_property('CM_Vals', vs)
L.compile_blueprint(a); st = str(a.get_editor_property('status')); assert 'UP_TO_DATE' in st, st
c2 = u.get_default_object(a.generated_class()); print('AFTER', len(c2.get_editor_property('CM_Keys')), c2.get_editor_property('CM_Keys')[-1].get_name(), '->', c2.get_editor_property('CM_Vals')[-1].get_name(), 'SphCM', c2.get_editor_property('SphCM'))
assert EAL.save_loaded_asset(a, False); print('DONE')
