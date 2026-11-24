import unreal as u
c=u.get_default_object(u.load_asset("/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player").generated_class())
print("RCHK player",{k:c.get_editor_property(k) for k in ("CT_BwdK","CT_StumK","FT_On","FT_In","FT_Ext","BOB_On","BOB_DipK","BOB_DipFree","BOB_DipMax","PS_RK","PS_BrEff","GR_KFat","GR_StopRel","GR_StopLead")})
m=u.get_default_object(u.load_asset("/Game/Sphirus/Player/Motion/AC_Sph_Motion").generated_class())
print("RCHK motion",{k:m.get_editor_property(k) for k in ("StSoftK","RcMin","RcMinSpr","RcMinV","StBoostRise","DmMax","RcOpen","RcKMax","DmMin","DmOpen","DmRate","DmRateK","DmWalkV")})
a=u.get_default_object(u.load_asset("/Game/Sphirus/Player/GASP/ABP_Sph_GASP").generated_class())
print("RCHK abp plant default/turns",a.get_editor_property("PlantSettings_Default").get_editor_property("unplant_radius"),a.get_editor_property("PlantSettings_Turns").get_editor_property("unplant_radius"),"SphSelTime" in dir(a) or hasattr(a,"sph_sel_time"))
print("RCHK world",u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world().get_outermost().get_name())
