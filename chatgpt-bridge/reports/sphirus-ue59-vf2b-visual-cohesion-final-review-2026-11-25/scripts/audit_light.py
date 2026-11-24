# VF2B read-only: exposure / bloom / sun / sky / fog values that decide whether skin and grass blow out in direct sun.
import unreal as u, re
EA = u.get_editor_subsystem(u.EditorActorSubsystem)
K = ('AutoExposureMinBrightness', 'AutoExposureMaxBrightness', 'AutoExposureBias', 'AutoExposureMethod', 'AutoExposureSpeedUp', 'AutoExposureSpeedDown', 'BloomIntensity', 'BloomThreshold', 'LocalExposureHighlightContrastScale', 'LocalExposureShadowContrastScale', 'LocalExposureDetailStrength', 'FilmSlope', 'FilmToe', 'FilmShoulder', 'ColorSaturation', 'ColorContrast', 'VignetteIntensity', 'AmbientOcclusionIntensity')
for a in EA.get_all_level_actors():
    if isinstance(a, u.PostProcessVolume):
        t = a.settings.export_text(); o = {}
        for k in K:
            if re.search(r'bOverride_%s=True' % k, t):
                m = re.search(r'[,(]%s=([^,)]+(?:\([^)]*\))?)' % k, t); o[k] = m.group(1)[:40] if m else '?'
        e = a.get_actor_bounds(False)[1]
        print('LT ppv', a.get_actor_label(), 'unbound', a.unbound, 'prio', a.priority, 'w', a.blend_weight, 'enabled', a.enabled, 'ext', [round(v) for v in (e.x, e.y, e.z)], o)
    elif isinstance(a, u.DirectionalLight):
        c = a.light_component; r = a.get_actor_rotation(); print('LT sun', a.get_actor_label(), 'int', c.intensity, 'col', [round(v, 2) for v in (c.light_color.r / 255, c.light_color.g / 255, c.light_color.b / 255)], 'temp', c.temperature, c.use_temperature, 'rot', round(r.pitch), round(r.yaw), 'src', c.light_source_angle, 'vol', c.volumetric_scattering_intensity)
    elif isinstance(a, u.SkyLight):
        c = a.light_component; print('LT sky', 'int', c.intensity, 'realtime', c.real_time_capture, 'col', [round(v, 2) for v in (c.light_color.r / 255, c.light_color.g / 255, c.light_color.b / 255)])
    elif isinstance(a, u.ExponentialHeightFog):
        c = a.component; print('LT fog density', c.fog_density, 'falloff', c.fog_height_falloff, 'vol', c.volumetric_fog, 'scatter', c.volumetric_fog_scattering_distribution, 'ext', c.volumetric_fog_extinction_scale)
D = '/Game/GraceRanger/Environment/GroundLayer20261111/Materials/'; mel = u.MaterialEditingLibrary
for n in ('MI_GL_GrassMedium01', 'MI_GL_GrassLarge01', 'MI_GL_GroundCover01_FO'):
    mi = u.load_asset(D + n)
    if mi: print('LT grass', n, {str(k): [round(x, 3) for x in (lambda c: (c.r, c.g, c.b))(mel.get_material_instance_vector_parameter_value(mi, k))] for k in mel.get_vector_parameter_names(mi)}, {str(k): round(mel.get_material_instance_scalar_parameter_value(mi, k), 2) for k in mel.get_scalar_parameter_names(mi) if any(s in str(k).lower() for s in ('sat', 'bright', 'spec', 'rough', 'trans', 'subsurf', 'opacity'))})
