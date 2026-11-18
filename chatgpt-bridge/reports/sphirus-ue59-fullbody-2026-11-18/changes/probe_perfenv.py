# probe_perfenv.py (read-only, PIE): rendering/performance environment of the measurement -> Saved/UE59Work/probe/perfenv.txt
import unreal as u
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(); o = []
try: vs = u.WidgetLayoutLibrary.get_viewport_size(W); o.append('viewport %.0fx%.0f' % (vs.x, vs.y))
except Exception as e: o.append('viewport ?')
for cv in ('r.ScreenPercentage', 'r.SecondaryScreenPercentage.GameViewport', 'r.AntiAliasingMethod', 'r.TSR.History.ScreenPercentage', 'sg.ResolutionQuality', 'sg.ViewDistanceQuality', 'sg.AntiAliasingQuality', 'sg.ShadowQuality', 'sg.GlobalIlluminationQuality', 'sg.ReflectionQuality', 'sg.PostProcessQuality', 'sg.TextureQuality', 'sg.EffectsQuality', 'sg.FoliageQuality', 'sg.ShadingQuality', 'r.DynamicGlobalIlluminationMethod', 'r.ReflectionMethod', 'r.Shadow.Virtual.Enable', 'r.Nanite', 'r.MegaLights.Allow', 'r.VSync', 't.MaxFPS', 'r.RayTracing', 'r.Lumen.HardwareRayTracing'):
    try: o.append('%s = %s' % (cv, u.SystemLibrary.get_console_variable_float_value(cv)))
    except Exception: o.append('%s ?' % cv)
try: o.append('RHI %s | GPU %s' % (u.RenderingLibrary and '', u.SystemLibrary.get_rendering_device_name() if hasattr(u.SystemLibrary, 'get_rendering_device_name') else '?'))
except Exception: pass
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/perfenv.txt', 'w').write('\n'.join(o)); print('PERFENV', len(o))
