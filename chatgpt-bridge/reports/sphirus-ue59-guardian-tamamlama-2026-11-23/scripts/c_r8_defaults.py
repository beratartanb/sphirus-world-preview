# c_r8_defaults.py (control, in-memory): round-8 player defaults (builtins.R8V overrides): fatigue pace, breath, start dip limiter
import unreal as u, builtins
V={'FT_On':True,'BOB_On':True,'PS_RK':0.6,'GR_KFat':0.12,'PS_BrAmp':0.5,'PS_BrEff':1.6,'PS_BrRate0':0.25,'PS_BrRate1':0.75,'BOB_DipK':0.6,'BOB_DipFree':4.0,'BOB_DipMax':9.0,'BOB_DipAcc':150.0,'GR_StopRel':80.0,'GR_StopLead':2000.0}; V.update(getattr(builtins,'R8V',None) or {})
c=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
for k,v in V.items(): c.set_editor_property(k,v)
print('R8DEF',{k:c.get_editor_property(k) for k in V})
