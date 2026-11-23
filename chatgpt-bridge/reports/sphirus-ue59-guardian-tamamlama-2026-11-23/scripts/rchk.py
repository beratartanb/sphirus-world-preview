import unreal as u
c=u.get_default_object(u.load_asset("/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player").generated_class())
print("RCHK player",{k:c.get_editor_property(k) for k in ("CT_BwdK","CT_StumK","FT_On","FT_In","FT_Ext","BOB_On","BOB_DipK","PS_RK","PS_BrEff","GR_KFat","GR_StopRel","GR_StopLead")})
m=u.get_default_object(u.load_asset("/Game/Sphirus/Player/Motion/AC_Sph_Motion").generated_class())
print("RCHK motion",{k:m.get_editor_property(k) for k in ("StSoftK","RcMin","RcMinSpr","RcMinV","StBoostRise","DmMax")})
print("RCHK world",u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world().get_outermost().get_name())
