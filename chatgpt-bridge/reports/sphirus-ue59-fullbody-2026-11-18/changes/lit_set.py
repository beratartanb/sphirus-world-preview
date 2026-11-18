# lit_set.py (runtime only, PIE world, not saved): builtins.LS = {'ppv': {prop: value}, 'ppvname': 'PostProcessVolume_0',
#   'sun': {prop: value}, 'cvar': {name: value}, 'reset': True}. Originals are kept in builtins.LS_ORIG and restored by 'reset'.
import unreal as u, builtins
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
LS = getattr(builtins, 'LS', {}) or {}
if not hasattr(builtins, 'LS_ORIG') or getattr(builtins, 'LS_W', None) != W.get_path_name(): builtins.LS_ORIG = {'ppv': {}, 'sun': {}, 'ppvs': {}}; builtins.LS_W = W.get_path_name()
O = builtins.LS_ORIG
V = {v.get_name(): v for v in u.GameplayStatics.get_all_actors_of_class(W, u.PostProcessVolume)}
v = V.get(LS.get('ppvname', 'PostProcessVolume_0'))
sun = [a for a in u.GameplayStatics.get_all_actors_of_class(W, u.DirectionalLight) if a.get_name() == 'DirectionalLight_0'][0].get_components_by_class(u.DirectionalLightComponent)[0]
out = []
if LS.get('reset'):
    for vn, kv in O.get('ppvs', {}).items():
        vv = V[vn]; s = vv.get_editor_property('settings')
        for k, (ov, val) in kv.items(): s.set_editor_property('override_' + k, ov); s.set_editor_property(k, val)
        vv.set_editor_property('settings', s, u.PropertyAccessChangeNotifyMode.NEVER)
    for k, val in O['sun'].items():
        if k == 'intensity': sun.set_intensity(val)
        else: sun.set_editor_property(k, val, u.PropertyAccessChangeNotifyMode.NEVER)
    out.append('RESET')
s = v.get_editor_property('settings')
for k, val in (LS.get('ppv') or {}).items():
    kv = O.setdefault('ppvs', {}).setdefault(v.get_name(), {})
    if k not in kv: kv[k] = (s.get_editor_property('override_' + k), s.get_editor_property(k))
    s.set_editor_property('override_' + k, True); s.set_editor_property(k, val); out.append('%s=%s' % (k, val))
v.set_editor_property('settings', s, u.PropertyAccessChangeNotifyMode.NEVER)
for k, val in (LS.get('sun') or {}).items():
    if k not in O['sun']: O['sun'][k] = sun.get_editor_property(k)
    if k == 'intensity': sun.set_intensity(val)
    else: sun.set_editor_property(k, val, u.PropertyAccessChangeNotifyMode.NEVER)
    out.append('sun.%s=%s' % (k, val))
for k, val in (LS.get('cvar') or {}).items():
    u.SystemLibrary.execute_console_command(W, '%s %s' % (k, val)); out.append('%s %s' % (k, val))
print('LITSET', v.get_name(), ' '.join(out))
