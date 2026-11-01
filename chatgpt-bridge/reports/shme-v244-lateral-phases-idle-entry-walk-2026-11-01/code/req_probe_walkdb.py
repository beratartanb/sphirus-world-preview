import unreal as u, json
AR = u.AssetRegistryHelpers.get_asset_registry(); out = {}
for nm in ('PSD_LB_WalkLoops', 'PSD_Dense_Stand_Walk_Loops', 'PSD_Dense_Stand_Walk_Stops', 'PSD_SHM216_WalkLink', 'PSD_SHM_StartTransfer_R', 'A_LB_Walk_Fwd', 'M_Ranger_Walk_Loop_F_PureForward_CWF'):
    ads = AR.get_assets_by_package_name(nm) or []
    if not ads:
        f = u.ARFilter(class_names=[], package_paths=[], recursive_paths=True); ads = [a for a in AR.get_all_assets() if str(a.asset_name) == nm]
    o = {'paths': [str(a.package_name) for a in ads][:3]}
    for a in ads[:1]:
        obj = a.get_asset()
        if isinstance(obj, u.PoseSearchDatabase):
            try: o['n'] = obj.get_num_animation_assets(); o['entries'] = [obj.get_animation_asset(i).get_name() for i in range(o['n'])][:40]; o['schema'] = obj.get_editor_property('schema').get_name()
            except Exception as e: o['err'] = str(e)[:80]
        elif isinstance(obj, u.AnimSequence):
            try:
                o['len'] = float(obj.get_play_length()); o['frames'] = u.AnimationLibrary.get_num_frames(obj); o['rate'] = str(u.AnimationLibrary.get_sequence_frame_rate(obj))
                rm = u.AnimationLibrary.get_root_motion_total(obj) if hasattr(u.AnimationLibrary, 'get_root_motion_total') else None
                o['root_motion_enabled'] = obj.get_editor_property('enable_root_motion'); o['skeleton'] = obj.get_editor_property('skeleton').get_name()
            except Exception as e: o['err'] = str(e)[:80]
    out[nm] = o
bp = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'); c = u.get_default_object(bp.generated_class())
out['abp_db_vars'] = [p for p in dir(c) if 'db' in p.lower() and p.startswith(('shm', 'gr', 'cp', 'ls'))][:40]
print('WALKDB244 ' + json.dumps(out, default=str))
