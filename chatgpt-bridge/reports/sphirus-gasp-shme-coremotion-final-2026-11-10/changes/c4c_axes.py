# c4c_axes.py (write): calibrated breathing axes (cal_breath_result.json): clavicles Y (both shoulders rise with +s),
# chest spine_05 Z (sagittal extension + neck lift); ChestDeg 3, ClavDeg 4.
import unreal as u
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'); c=u.get_default_object(a.generated_class())
for k,v in (('ChestAxis',u.Vector(0,0,1)),('ClavAxisL',u.Vector(0,1,0)),('ClavAxisR',u.Vector(0,1,0)),('ChestDeg',3.0),('ClavDeg',4.0)): c.set_editor_property(k,v)
u.BlueprintEditorLibrary.compile_blueprint(a); assert u.EditorAssetLibrary.save_loaded_asset(a,False); print('DONE',{k:str(c.get_editor_property(k)) for k in ('ChestAxis','ClavAxisL','ChestDeg','ClavDeg')})
