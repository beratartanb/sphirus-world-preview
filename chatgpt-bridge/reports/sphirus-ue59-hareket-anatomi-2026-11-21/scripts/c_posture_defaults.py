# c_posture_defaults.py (control job, in-memory): posture controller defaults on the BP_HybridA_Player CDO. builtins.PSV overrides.
import unreal as u, builtins
P='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; a=u.load_asset(P); d=u.get_default_object(a.generated_class())
V={'PS_On':True,'PS_K':2.5,'PS_R2':0.7,'PS_R3':0.55,'PS_R4':0.3,'PS_B1':7.1,'PS_B2':-8.9,'PS_B3':-11.2,'PS_B4':11.9,'PS_C3':-4.0,'PS_C5':-12.0,'PS_CN':12.0,'PS_CH':-2.0,
   'PS_HK':0.0,'PS_HMove':1.0,'PS_KAR':0.85,'PS_KARBent':0.45,'PS_Bent':0.0,'PS_ShF':-0.7,'PS_ShL':5.2,'PS_ShLRun':0.8,'PS_KC':1.0,'PS_RH':21.0,'PS_RW':17.0,'PS_RF':6.0,'PS_KAU':12.0,'PS_KAD':0.4,
   'PS_PAMax':14.0,'PS_ArmBase':0.0,'PS_Eff':0.0,'PS_HRS':1.0,'PS_CHR':0.0}
V.update(getattr(builtins,'PSV',None) or {})
for k,v in V.items(): d.set_editor_property(k,v)
print('PSDEF',{k:d.get_editor_property(k) for k in ('PS_On','PS_K','PS_R2','PS_RH','PS_KAR')})
