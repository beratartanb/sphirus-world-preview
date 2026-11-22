# c_foot7_defaults.py (control, in-memory): foot clearance defaults on the BP_HybridA_Player CDO (builtins.FTV overrides)
import unreal as u, builtins
V={'FT_On':True,'FT_Min':8.0,'FT_Sole':8.0,'FT_Clear':3.0,'FT_Max':45.0,'FT_In':25.0,'FT_Out':8.0,'FT_Ext':2.0,'FT_HMax':40.0}; V.update(getattr(builtins,'FTV',None) or {})
c=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
for k,v in V.items(): c.set_editor_property(k,v)
print('FTDEF',{k:c.get_editor_property(k) for k in V})
