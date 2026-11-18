import unreal as u
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(); o = []
for v in u.GameplayStatics.get_all_actors_of_class(W, u.PostProcessVolume):
    s = v.get_editor_property('settings'); o.append('%s prio %s' % (v.get_name(), v.get_editor_property('priority')))
    for n in ('local_exposure_method','local_exposure_highlight_contrast_scale','local_exposure_highlight_threshold','local_exposure_highlight_threshold_strength','local_exposure_blurred_luminance_blend','local_exposure_blurred_luminance_kernel_size_percent','local_exposure_detail_strength','local_exposure_middle_grey_bias','tonemapping_method','film_shoulder','film_white_clip','film_toe','film_slope','auto_exposure_high_percent','auto_exposure_low_percent','auto_exposure_speed_up','auto_exposure_speed_down','histogram_log_min','histogram_log_max','auto_exposure_apply_physical_camera_exposure'):
        try: o.append('   %s=%s ov=%s' % (n, s.get_editor_property(n), s.get_editor_property('override_' + n)))
        except Exception as e: o.append('   %s ?' % n)
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/ppv_full.txt', 'w').write('\n'.join(o)); print('PPVFULL', len(o))
