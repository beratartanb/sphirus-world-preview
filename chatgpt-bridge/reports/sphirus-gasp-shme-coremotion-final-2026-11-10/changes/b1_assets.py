# b1_assets.py (write): Sphirus-owned GASP derivatives (vendor GASP files untouched):
#  - /Game/Sphirus/Player/GASP/Rig/RTG_Sph_UEFN_to_MH   (copy of GASP RTG_UEFN_to_Metahuman_nrw, target preview = Sphirus MH body)
#  - /Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP        (copy of ABP_Sph_Body, retarget node -> RTG_Sph_UEFN_to_MH)
#  - /Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter     (copy of GASP SandboxCharacter_CMC; editable parent for the Sphirus pawn)
#  - /Game/Sphirus/Player/GASP/ABP_Sph_GASP             (copy of GASP SandboxCharacter_CMC_ABP)
#  - /Game/Sphirus/Player/GASP/BP_Sph_GASP_B            (copy of BP_HybridA_Player; becomes the clean-GASP candidate)
import unreal as u
EA=u.EditorAssetLibrary; D='/Game/Sphirus/Player/GASP/'
def dup(src,dst):
    if EA.does_asset_exist(dst): print('EXISTS',dst); return u.load_asset(dst)
    a=EA.duplicate_asset(src,dst); assert a,dst; print('DUP',src,'->',dst); return a
rtg=dup('/Game/MetaHumans/Common/Common/Rigs/RTG_UEFN_to_Metahuman_nrw',D+'Rig/RTG_Sph_UEFN_to_MH')
body=u.load_asset('/Game/Sphirus/CharacterLab/Sph_20261108/Built/MHC_Sph8/Body/SKM_MHC_Sph8_BodyMesh')
try:
    c=u.IKRetargeterController.get_controller(rtg); c.set_preview_mesh(u.RetargetSourceOrTarget.TARGET,body); print('RTG target preview set')
except Exception as e: print('RTG preview WARN',str(e)[:120])
assert EA.save_loaded_asset(rtg,False)
abp=dup('/Game/Sphirus/Player/Anim/ABP_Sph_Body',D+'ABP_Sph_Body_GASP')
n_=0
for g in u.BlueprintEditorLibrary.get_graphs(abp) if hasattr(u.BlueprintEditorLibrary,'get_graphs') else []:
    pass
from editor_toolset.toolsets.blueprint import BlueprintTools as B
for g in B.list_graphs(abp):
    for n in B.find_nodes(g):
        if 'RetargetPoseFromMesh' not in type(n).__name__: continue
        nd=n.get_editor_property('node'); print('OLD',nd.get_editor_property('ik_retargeter_asset'))
        nd.set_editor_property('ik_retargeter_asset',rtg); n.set_editor_property('node',nd)
        print('NEW',n.get_editor_property('node').get_editor_property('ik_retargeter_asset').get_path_name()); n_+=1
assert n_==1,n_
u.BlueprintEditorLibrary.compile_blueprint(abp); assert EA.save_loaded_asset(abp,False)
ch=dup('/Game/Blueprints/SandboxCharacter_CMC',D+'BP_Sph_GASPCharacter'); u.BlueprintEditorLibrary.compile_blueprint(ch); assert EA.save_loaded_asset(ch,False)
ga=dup('/Game/Blueprints/SandboxCharacter_CMC_ABP',D+'ABP_Sph_GASP'); u.BlueprintEditorLibrary.compile_blueprint(ga); assert EA.save_loaded_asset(ga,False)
b=dup('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player',D+'BP_Sph_GASP_B'); u.BlueprintEditorLibrary.compile_blueprint(b); assert EA.save_loaded_asset(b,False)
for a in (abp,ch,ga,b): print('STATUS',a.get_name(),a.get_editor_property('status'))
print('DONE')
