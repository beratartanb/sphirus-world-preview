# skin_probe.py (read-only, run in PIE): lights near the player with channels, and the player's mesh components/materials.
import unreal as u
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
P = u.GameplayStatics.get_player_pawn(W, 0); L = P.get_actor_location()
out = ['PAWN %s at %s' % (P.get_name(), L)]
def ch(c):
    try:
        lc = c.get_editor_property('lighting_channels'); return '%d%d%d' % (lc.channel0, lc.channel1, lc.channel2)
    except Exception as e: return '?'
for a in u.GameplayStatics.get_all_actors_of_class(W, u.Actor):
    for c in a.get_components_by_class(u.LightComponentBase):
        try: d = (c.get_world_location() - L).length()
        except Exception: d = -1
        isdir = isinstance(c, (u.DirectionalLightComponent, u.SkyLightComponent))
        if d < 1500 or isdir:
            g = lambda n: (c.get_editor_property(n) if True else None)
            r = []
            for n in ('intensity', 'attenuation_radius', 'cast_shadows', 'visible', 'specular_scale', 'indirect_lighting_intensity', 'volumetric_scattering_intensity', 'source_radius', 'inner_cone_angle', 'outer_cone_angle', 'intensity_units', 'light_color'):
                try: r.append('%s=%s' % (n, c.get_editor_property(n)))
                except Exception: pass
            out.append('LIGHT %s.%s [%s] d=%.0f ch=%s vis=%s loc=%s | %s' % (a.get_name(), c.get_name(), c.get_class().get_name(), d, ch(c), c.is_visible(), c.get_world_location() if not isdir else '-', ' '.join(r)))
for c in P.get_components_by_class(u.PrimitiveComponent):
    if isinstance(c, (u.SkeletalMeshComponent, u.GroomComponent)):
        m = []
        try: m = [x.get_path_name() if x else 'None' for x in c.get_materials()]
        except Exception: pass
        out.append('COMP %s [%s] vis=%s ch=%s mats=%s' % (c.get_name(), c.get_class().get_name(), c.is_visible(), ch(c), m))
import os
p = u.Paths.project_dir() + 'Saved/UE59Work/probe/skin_probe.txt'
open(p, 'w', encoding='utf8').write('\n'.join(out)); print('SKINPROBE', len(out))
