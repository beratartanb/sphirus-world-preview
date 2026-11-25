# c_mr3_defaults.py (control, in memory; re-appliable; runs LAST in alldef) - movement realism pass 3 (2026-11-25).
# GaitUpAcc 0.8 -> 0.38: a gait step-up (walk -> run -> sprint) develops over 2-4 steps instead of one.
# CS_*: braking steps on a key release at run / sprint speed (m_coast3_mcp).
import unreal as u, builtins
M3={'StBoostMax':1400.0,'StBoostMaxSt':800.0,'StBoostDur':0.42}; M3.update(getattr(builtins,'MR3M',None) or {})
m=u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())
for k,v in M3.items():
    try: m.set_editor_property(k,v)
    except Exception as e: print('MR3DEF missing',k)
P3={'BR_Sh':3.5,'BR_FatK':1.0,'PS_BrEff':2.4,'PS_S2':6.0,'PS_S3':6.0,'PS_S4':2.5,'TLM_On':1.0,'TLM_Free':14.0,'TLM_K':0.6,'TLM_Max':14.0,'TLM_Rate':120.0,'TLM_KS':0.5,'CA_On':1.0,'CA_Tgt':6.5,'CA_K':2.5,'CA_Max':12.0,'CA_Fall':1.0,'CA_Rise':40.0,'CA_Rad':9.5,'PS_AbdBack':5.0,'GU_Run':0.38,'GU_Tempo':0.16,'CS_On':1.0,'CS_VMin':350.0,'CS_VEnd':320.0,'CS_Max':1.0,'CS_Look':0.45,'CS_K':1.0,'CS_Dec':520.0}; P3.update(getattr(builtins,'MR3P',None) or {})
c=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
for k,v in P3.items():
    try: c.set_editor_property(k,v)
    except Exception as e: print('MR3DEF missing',k)
print('MR3DEF',{k:m.get_editor_property(k) for k in M3},{k:c.get_editor_property(k) for k in P3})
# camera (AC_Sph_Camera class defaults + the player's component template)
C3={'SpeedArm':-14.0,'SprArm':-4.0,'FovSpr':3.5}; C3.update(getattr(builtins,'MR3C',None) or {})
cc=u.get_default_object(u.load_asset('/Game/Sphirus/Player/Camera/AC_Sph_Camera').generated_class()); tg=[cc]
try:
    sub=u.get_engine_subsystem(u.SubobjectDataSubsystem); bp=u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player')
    for h in sub.k2_gather_subobject_data_for_blueprint(bp):
        o=u.SubobjectDataBlueprintFunctionLibrary.get_object(sub.k2_find_subobject_data_from_handle(h))
        if o and o.get_class().get_name()=='AC_Sph_Camera_C': tg.append(o)
except Exception as e: print('MR3DEF cam template',e)
for o in tg:
    for k,v in C3.items():
        try: o.set_editor_property(k,v)
        except Exception as e: print('MR3DEF cam missing',k)
print('MR3DEF cam',[(o.get_name(),{k:o.get_editor_property(k) for k in C3}) for o in tg])
