"""post244_walk.py (A/B POST): reload the vendor walk loop from disk (discard the in-memory candidate edit). Prints POSTWALK244 ..."""
import unreal as u
LS = u.EditorLoadingAndSavingUtils; P = '/Game/GraceRanger/Animations/LocomotionBehavior/A_LB_Walk_Fwd'
pk = u.load_package(P); LS.reload_packages([pk], u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
print('POSTWALK244 reloaded dirty=%s' % [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()][:5])
