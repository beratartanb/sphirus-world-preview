# runtime only (PIE world, not saved): local exposure highlight contrast on the top unbound post process volume. builtins.SKV = value or None (restore)
import unreal as u, builtins
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
V = sorted([v for v in u.GameplayStatics.get_all_actors_of_class(W, u.PostProcessVolume) if v.get_editor_property('unbound') and v.get_editor_property('enabled')], key=lambda v: -v.get_editor_property('priority'))
o = []
for v in V:
    s = v.get_editor_property('settings'); r = [v.get_name(), v.get_editor_property('priority')]
    for n in ('auto_exposure_method','auto_exposure_bias','auto_exposure_min_brightness','auto_exposure_max_brightness','local_exposure_highlight_contrast_scale','local_exposure_shadow_contrast_scale','local_exposure_detail_strength','local_exposure_method','bloom_intensity'):
        try: r.append('%s=%s(ov %s)' % (n, s.get_editor_property(n), s.get_editor_property('override_' + n)))
        except Exception as e: r.append(n + '=?')
    o.append(' '.join(str(x) for x in r))
if not hasattr(builtins, 'SKV_DUMPED'):
    open(u.Paths.project_dir()+'Saved/UE59Work/probe/ppv.txt','w').write('\n'.join(o)); builtins.SKV_DUMPED = 1
v = V[0]; s = v.get_editor_property('settings')
if not hasattr(builtins, 'SKV_ORIG'): builtins.SKV_ORIG = (s.get_editor_property('override_local_exposure_highlight_contrast_scale'), s.get_editor_property('local_exposure_highlight_contrast_scale'))
if builtins.SKV is None: ov, val = builtins.SKV_ORIG
else: ov, val = True, builtins.SKV
s.set_editor_property('override_local_exposure_highlight_contrast_scale', ov); s.set_editor_property('local_exposure_highlight_contrast_scale', val); v.set_editor_property('settings', s)
print('SKV', v.get_name(), ov, val)
