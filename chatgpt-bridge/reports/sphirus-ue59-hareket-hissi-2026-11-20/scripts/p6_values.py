# p6_values.py (write, gated): carriage values on ABP_Sph_Body_GASP defaults. builtins.P6V overrides the table.
import unreal as u, builtins
P='/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'; a=u.load_asset(P); d=u.get_default_object(a.generated_class())
V=getattr(builtins,'P6V',None) or {'RunLo':200.0,'RunFull':415.0,'VR_ArmL':(6.0,5.0,0.0),'VR_ArmR':(6.0,-5.0,0.0),'VW_ArmL':(0.0,-1.5,0.0),'VW_ArmR':(0.0,1.5,0.0),'VW_Neck1':(-8.0,0.0,0.0),'VW_Head':(0.0,0.0,0.0)}
for k,v in V.items():
    old=d.get_editor_property(k); o=(old.x,old.y,old.z) if hasattr(old,'x') else old
    d.set_editor_property(k, u.Vector(*v) if isinstance(v,tuple) else v); print('SET',k,o,'->',v)
u.BlueprintEditorLibrary.compile_blueprint(a)
try: print('SAVE',u.EditorAssetLibrary.save_loaded_asset(a,False))
except Exception as e: print('SAVE_EXC',repr(e)[:100])
d=u.get_default_object(u.load_asset(P).generated_class())
print('NOW',{k:((lambda q:(q.x,q.y,q.z))(d.get_editor_property(k)) if isinstance(v,tuple) else d.get_editor_property(k)) for k,v in V.items()})
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
