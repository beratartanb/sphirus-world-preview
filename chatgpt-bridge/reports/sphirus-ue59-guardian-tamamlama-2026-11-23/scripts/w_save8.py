# w_save7.py (write, gated): save the round-7 in-memory edits one asset at a time (multi-asset save once raised SAVE_EXC on an AnimBP):
# BP_HybridA_Player (contact / posture / foot clearance / bob events + defaults), AC_Sph_Motion + BP_Sph_GASPCharacter (motion defaults).
# Not saved on purpose: ABP_Sph_GASP (only recompiled; blend time back at its saved 0.5), BP_GR_MaskBench + L_GR_SphirusHouse (inspect
# framing trial restored to the saved values 18/24/33/0.9).
import unreal as u
P=['/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player','/Game/Sphirus/Player/Motion/AC_Sph_Motion','/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter']
for p in P:
    a=u.load_asset(p)
    if isinstance(a,u.Blueprint): u.BlueprintEditorLibrary.compile_blueprint(a)
    try: r=u.EditorAssetLibrary.save_loaded_asset(a,False)
    except Exception as e: r='SAVE_EXC '+repr(e)[:120]
    print('SAVE8',p.split('/')[-1],r)
c=u.get_default_object(u.load_asset(P[0]).generated_class())
print('CHK8 player',{k:c.get_editor_property(k) for k in ('CT_KneeExtra','CT_BwdK','CT_StumK','FT_On','FT_In','FT_Ext','FT_HMax','BOB_On','BOB_DipK','PS_RK','PS_BrEff','GR_KFat','GR_StopRel','GR_StopLead')})
m=u.get_default_object(u.load_asset(P[1]).generated_class())
print('CHK8 motion',{k:m.get_editor_property(k) for k in ('StSoftK','RcMin','RcMinSpr','RcMinV','StBoostRise','DmMax')})
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
