import unreal as u
LS = u.EditorLoadingAndSavingUtils; AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
pk = [u.load_package(AP), u.load_package(AP.replace('Base', ''))]; LS.reload_packages(pk, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
print('POSTINERTIA246 reloaded dirty=%s' % [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()][:5])
