"""post243_idle.py (A/B POST): reload ABP_GR_MotionMatchingBase / ABP_GR_MotionMatching from disk (undo pre243_idle). Prints POSTIDLE243 ..."""
import unreal as u
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
LS = u.EditorLoadingAndSavingUtils; AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
pk = [p for p in LS.get_dirty_content_packages() if p.get_name() in (AP, AP.replace('Base', ''))]
if pk: LS.reload_packages(pk, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE)
print('POSTIDLE243 reloaded %d dirty_after %s' % (len(pk), [p.get_name().split('/')[-1] for p in LS.get_dirty_content_packages()]))
