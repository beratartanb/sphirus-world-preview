# w_ledge_rtg.py (write, gated): project copies of the AAMS ledge / wall-step clips retargeted from the AAMS UE5 Manny skeleton to the driver's
# UEFN mannequin skeleton (RTG_UE5_to_UEFN, AAMS demo retargeter) into /Game/Sphirus/Player/Anim/Ledge (prefix SphL_). Sources untouched.
import unreal as u
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
A = '/Game/AAMS/AAMS/Animations/'
names = ['Ledge/Braced/AS_Ledge_Braced_' + n for n in ('FallToBracedIdle', 'Idle', 'Mantle', 'Jump_Down', 'StandToBracedIdle', 'Jump_Up', 'Left', 'Right', 'StandDropToIdle', 'Jump_Back')] + \
        ['Vault/AS_Vault_MantleJumpUp_1m', 'Vault/AS_Vault_FallToMantle', 'Vault/AS_Vault_MantleStep']
src = [u.EditorAssetLibrary.find_asset_data(A + n) for n in names]
print('LRTG src', sum(1 for s in src if s.is_valid()), len(src))
out = u.IKRetargetBatchOperation.duplicate_and_retarget(src, u.load_asset('/Game/AAMS/Demo/Characters/Mannequins/Meshes/SKM_Manny_Simple'), u.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin'),
    u.load_asset('/Game/AAMS/Demo/Characters/Mannequins/Rigs/RTG_UE5_to_UEFN'), '', '', 'SphL_', '', '/Game/Sphirus/Player/Anim/Ledge', False, False, False)
for a in out:
    s = u.load_asset(str(a.package_name)); print('LRTG', str(a.asset_name), s.get_editor_property('skeleton').get_name(), 'len %.2f' % s.get_play_length(), 'rm', s.get_editor_property('enable_root_motion'))
    u.EditorAssetLibrary.save_loaded_asset(s, False)
