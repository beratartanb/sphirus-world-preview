import unreal as u
from editor_toolset.toolsets.blueprint import BlueprintTools as B
a=u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion')
for n in ('Enabled','EffortEnabled'): B.set_variable_instance_editable(a,n,True)
u.BlueprintEditorLibrary.compile_blueprint(a); assert u.EditorAssetLibrary.save_loaded_asset(a,False); print('DONE',a.get_editor_property('status'))
