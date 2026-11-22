# c_soft6_defaults.py (control, in-memory): soft start defaults on the BP_HybridA_Player CDO (builtins.SOFT overrides)
import unreal as u, builtins
V={'GR_SoftStartOn':True,'GR_SoftStartT':0.42,'GR_SoftStartV':150.0,'GR_SprintMinSp':250.0}; V.update(getattr(builtins,'SOFT',None) or {})
c=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
for k,v in V.items(): c.set_editor_property(k,v)
print('SOFTDEF',{k:c.get_editor_property(k) for k in V})
