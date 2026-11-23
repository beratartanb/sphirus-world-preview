# c_atm.py (control, in-memory only): atmosphere candidate on level actors from builtins.R2G_ATM, e.g.
# {'sun': {'volumetric_scattering_intensity': 0.5}, 'fog': {...}, 'sky': {...}, 'lfv:EX_Look_Fog_Pond': {...}}. Prints old -> new. Dirties the open map (never saved here).
import unreal as u, builtins
V = getattr(builtins, 'R2G_ATM', None) or {}
acts = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
def comp(key):
    for a in acts:
        cn = a.get_class().get_name(); lb = a.get_actor_label()
        if key == 'sun' and cn == 'DirectionalLight': return a.light_component
        if key == 'sky' and cn == 'SkyLight': return a.light_component
        if key == 'fog' and cn == 'ExponentialHeightFog': return a.component
        if key.startswith('lfv:') and lb == key[4:]: return a.get_component_by_class(u.LocalFogVolumeComponent)
        if key.startswith('ppv:') and lb == key[4:]: return a
for key, d in V.items():
    c = comp(key)
    for k, v in d.items():
        o = c.settings if key.startswith('ppv:') else c
        if key.startswith('ppv:'):
            s = c.settings; old = s.get_editor_property(k); s.set_editor_property(k, v); c.set_editor_property('settings', s); new = c.settings.get_editor_property(k)
        else:
            old = c.get_editor_property(k); c.set_editor_property(k, v); new = c.get_editor_property(k)
        print('ATM', key, k, old, '->', new)
