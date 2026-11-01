import unreal as u, json
P = '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/PSD_Dense_Stand_Walk_Loops'; db = u.load_asset(P); db.modify()
ok = u.EditorAssetLibrary.save_asset(P, False)
print('SAVEDDB246 ' + json.dumps({'saved': ok, 'n': db.get_num_animation_assets(), 'dirty': [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}))
