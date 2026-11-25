import unreal as u, re
K = ('AutoExposureMinBrightness', 'AutoExposureMaxBrightness', 'AutoExposureBias', 'AutoExposureMethod', 'AutoExposureLowPercent', 'AutoExposureHighPercent', 'BloomIntensity', 'LocalExposureHighlightContrastScale', 'LocalExposureShadowContrastScale', 'LocalExposureHighlightThreshold', 'LocalExposureShadowThreshold', 'LocalExposureDetailStrength', 'LocalExposureMethod', 'LocalExposureBlurredLuminanceBlend', 'ColorSaturation', 'ColorContrast', 'ColorGain', 'WhiteTemp', 'VignetteIntensity', 'FilmSlope', 'FilmToe', 'FilmShoulder', 'LumenSceneLightingQuality', 'LumenFinalGatherQuality', 'IndirectLightingIntensity')
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    if isinstance(a, u.PostProcessVolume):
        t = a.settings.export_text(); o = {}
        for k in K:
            if re.search(r'bOverride_%s=True' % k, t):
                m = re.search(r'[,(]%s=(\([^)]*\)|[^,)]+)' % k, t); o[k] = m.group(1)[:44] if m else '?'
        l = a.get_actor_location(); e = a.get_actor_bounds(False)[1]
        print('PP', a.get_actor_label(), '| unbound', a.unbound, 'prio', a.priority, 'blendR', a.blend_radius, 'w', a.blend_weight, 'on', a.enabled, '| at', [round(v) for v in (l.x, l.y, l.z)], 'ext', [round(v) for v in (e.x, e.y, e.z)], '|', o)
    if a.get_actor_label() in ('GR_DayBoot',):
        print('PP dayboot vars', [(p, str(a.get_editor_property(p))[:40]) for p in dir(a) if p.startswith('gr_')][:20])
