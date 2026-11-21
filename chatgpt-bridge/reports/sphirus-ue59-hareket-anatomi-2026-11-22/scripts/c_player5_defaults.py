# c_player5_defaults.py (control, in-memory): round-5 defaults on the BP_HybridA_Player CDO (builtins.P5V overrides).
import unreal as u, builtins
V={'GR_SprintMinSp':20.0,'CT_On':True,'CT_Look':0.45,'CT_Dec':600.0,'CT_CosHead':0.6,'CT_VMin':110.0,'CT_VRef':330.0,'CT_KFat':0.5,'CT_KAnt':0.75,'CT_SBump':0.35,'CT_SStag':0.9,'CT_SDown':1.5,'CT_KickP':90.0,'CT_KickR':70.0,'CT_GrazeLean':250.0,'CT_DownHold':0.6,'CT_DownFat':1.6}; V.update(getattr(builtins,'P5V',None) or {})
c=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
for k,v in V.items(): c.set_editor_property(k,v)
print('P5DEF',{k:c.get_editor_property(k) for k in V})
