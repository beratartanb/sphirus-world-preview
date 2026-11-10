# s3_tune.py (write): calibration from PIE (PH_phys_rx3): braking settle pitched the chest BACK (-1.5 deg trunk lean) ->
# ABP_Sph_Body_GASP PitchAxis (0,0,-1) -> (0,0,1); AC_Sph_Motion SettleDeg 3 -> 4.
import unreal as u
EA=u.EditorAssetLibrary; L=u.BlueprintEditorLibrary
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'); c=u.get_default_object(a.generated_class())
c.set_editor_property('PitchAxis',u.Vector(0,0,1)); L.compile_blueprint(a); assert EA.save_loaded_asset(a,False)
m=u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion'); mc=u.get_default_object(m.generated_class())
mc.set_editor_property('SettleDeg',4.0); L.compile_blueprint(m); assert EA.save_loaded_asset(m,False)
print('TUNE',u.get_default_object(a.generated_class()).get_editor_property('PitchAxis'),u.get_default_object(m.generated_class()).get_editor_property('SettleDeg')); print('DONE')
