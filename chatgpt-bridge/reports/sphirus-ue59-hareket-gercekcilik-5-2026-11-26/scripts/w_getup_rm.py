# w_getup_rm.py (write, gated): root motion on the project get-up copy (SphF_..._GetUp, no referencers): the clip moves its root ~34 cm while
# standing up; without root motion the pose would snap back at the end. Played by the player fall logic (m_fall_mcp) as a dynamic montage.
import unreal as u
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
s = u.load_asset('/Game/Sphirus/Player/Anim/Fall/SphF_am_InjuredBelly_DropToFloor_GetUp'); s.set_editor_property('enable_root_motion', True); s.set_editor_property('force_root_lock', False)
print('GURM', s.get_editor_property('enable_root_motion'), u.EditorAssetLibrary.save_loaded_asset(s, False))
