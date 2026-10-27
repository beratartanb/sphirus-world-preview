import unreal as u, json
LS = u.EditorLoadingAndSavingUtils; EAL = u.EditorAssetLibrary
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
dirty = [p.get_name() for p in LS.get_dirty_content_packages()]
saved = []
for n in dirty:
    if n.startswith('/Game/GraceRanger/SHME/Animations/Starts/PSD_SHM_'): saved.append((n, bool(EAL.save_asset(n, False))))
rl = [p for p in LS.get_dirty_content_packages() if p.get_name() in ('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching', '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase', '/Game/GraceRanger/SHME/DA_SHM_Response_Default')]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
print('C1FIX ' + json.dumps({'dirty_before': dirty, 'saved': saved, 'reloaded': [p.get_name() for p in rl], 'dirty_after': [p.get_name() for p in LS.get_dirty_content_packages()]}))
