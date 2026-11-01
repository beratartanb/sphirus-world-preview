import unreal as u, json
P = '/Game/GraceRanger/Animations/LocomotionBehavior/PSD_LB_WalkLoops'; db = u.load_asset(P)
ok = u.EditorAssetLibrary.save_asset(P, False)
print('SAVEWDB245 ' + json.dumps({'saved': ok, 'entries': [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())], 'dirty': [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}))
