import unreal as u
LS = u.EditorLoadingAndSavingUtils
d = [p for p in LS.get_dirty_content_packages() if p.get_name() in ("/Game/GraceRanger/BP_GR_Player", "/Game/GraceRanger/Profiles/BP_GR_MotionProfile", "/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player")]
if d: LS.reload_packages(d, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
print("RELOADGR dirty after", [p.get_name() for p in LS.get_dirty_content_packages()])
