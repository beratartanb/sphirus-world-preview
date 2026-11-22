# c_contact6_defaults.py (control, in-memory): contact v2 defaults on the BP_HybridA_Player CDO (builtins.P6V overrides).
import unreal as u, builtins
V={'CT_SepMin':25.0,'CT_TripV':330.0,'CT_TanKeep':0.7,'CT_TripKick':110.0,'CT_RetD':44.0,'CT_RetT':0.38,'CT_KneelClr':30.0,'CT_CutMin':0.5,'CT_FallRate':2.2,'CT_FallTf':0.7,'CT_FallDur':1.5,'CT_TripH':0.85,
   'CT_LieHold':1.2,'CT_UpRate':2.0,'CT_UpDur':3.0,'CT_HalfH':92.0,'CT_HandOff':8.0,'CT_GrazeReach':0.3,'CT_StandOff':20.0,'CT_KneeSeeV':230.0,'CT_Tuck':-24.0,'CT_PalmK':1.0,'CT_StepV':100000.0,'CT_DuckD':110.0,'CT_DuckOn':True,'CT_SlopeLo':0.34,'CT_SlopeHi':0.5,'CT_StairV':80.0,'CT_StairRunV':170.0,'CT_Since':99.0,'CT_Sep':99.0}; V.update(getattr(builtins,'P6V',None) or {})
c=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
for k,v in V.items(): c.set_editor_property(k,v)
print('P6DEF',{k:c.get_editor_property(k) for k in V})
