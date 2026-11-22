# c_posture7_defaults.py (control job, in-memory): posture controller v2 defaults on the BP_HybridA_Player CDO. builtins.PSV overrides.
import unreal as u, builtins
d=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
V={'PS_On':True,'PS_K':1.6,'PS_R2':0.7,'PS_R3':0.55,'PS_R4':0.3,'PS_Keep':0.35,'PS_KeepMax':4.0,'PS_E2':3.0,'PS_E3':3.5,'PS_E4':1.5,'PS_EH':3.0,'PS_LK':0.08,'PS_LW':9.0,'PS_LZ':0.5,
   'PS_HP0':2.0,'PS_HMove':2.0,'PS_HK':0.2,'PS_HKeep':0.35,'PS_HRK':0.4,'PS_HRS':1.0,
   'PS_ShF':-0.7,'PS_ShL':5.7,'PS_ShLRun':0.5,'PS_ShAsym':0.5,'PS_ShEffF':0.5,'PS_ShEffL':0.4,'PS_KC':1.0,
   'PS_KArm':1.2,'PS_AbdBase':12.5,'PS_AbdRun':9.5,'PS_AbdSpr':4.0,'PS_KV':0.75,'PS_KR':1.8,'PS_DAL':-4.0,'PS_DAR':-4.0,
   'PS_RH':18.3,'PS_RW':15.0,'PS_RF':3.0,'PS_KAU':12.0,'PS_KAD':2.0,'PS_PAMax':8.0,'PS_KAR':0.85,'PS_KARBent':0.45,'PS_ArmBase':0.0,'PS_KeepRun':0.4,'PS_LuK':2.0,'PS_LuMax':15.0,'PS_LuRun':6.0,'PS_RK':0.6,'PS_RLP':2.0,'PS_RSign':-1.0,'PS_LZ':0.8}
V.update(getattr(builtins,'PSV',None) or {})
for k,v in V.items(): d.set_editor_property(k,v)
print('PS2DEF',{k:d.get_editor_property(k) for k in ('PS_K','PS_Keep','PS_AbdBase','PS_RH','PS_ShL')})
