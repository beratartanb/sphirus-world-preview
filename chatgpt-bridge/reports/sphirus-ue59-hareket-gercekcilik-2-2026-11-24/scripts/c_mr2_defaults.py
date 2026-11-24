# c_mr2_defaults.py (control, in memory; re-appliable; runs LAST in alldef, after c_mr1_defaults) - movement realism pass 2 (2026-11-24).
# RcOpen 1500 -> 150: the flip-frame prediction equals the governed one, Motion Matching enters the turn clip once (no wrong-foot entry).
# SL_*: relocation step (m_slidestep2). HD_K: head keeps the clip orientation against the shoulder correction (c_hip3 / m_hip3).
import unreal as u, builtins
M2={'RcOpen':150.0}; M2.update(getattr(builtins,'MR2M',None) or {})
m=u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())
for k,v in M2.items(): m.set_editor_property(k,v)
P2={'SL_On':1.0,'SL_K':0.06,'SL_V0':70.0,'SL_Max':6.0,'SL_In':30.0,'SL_Out':10.0,'HD_K':0.0,'HD_B':1.0,'HIP_GY':22.0,'HIP_GO':14.0,'SH_G':34.0,'HIP_Rate':150.0,'HD_T':0.0,'ID_On':1.0,'ID_X':2.2,'ID_Z':0.6,'ID_O':3.0,'ID_Y':2.0,'ID_KS':1.3,'ID_Delay':1.2,'ID_Period':14.0}; P2.update(getattr(builtins,'MR2P',None) or {})
c=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
for k,v in P2.items():
    try: c.set_editor_property(k,v)
    except Exception as e: print('MR2DEF missing',k)
print('MR2DEF',{k:m.get_editor_property(k) for k in M2},{k:c.get_editor_property(k) for k in P2 if hasattr(c,'get_editor_property')})
