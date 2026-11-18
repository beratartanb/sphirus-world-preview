# skin_mat.py (read-only): parameter dump of the body skin instance and its parent chain.
import unreal as u
MEL = u.MaterialEditingLibrary
out = []
m = u.load_asset('/Game/Sphirus/CharacterLab/Day_20261107/Skin/MI_Sph_Body_HomeB')
while m is not None:
    out.append('== %s [%s]' % (m.get_path_name(), m.get_class().get_name()))
    if isinstance(m, u.MaterialInstanceConstant):
        for p in m.get_editor_property('scalar_parameter_values'): out.append('  S %s = %s' % (p.parameter_info.name, p.parameter_value))
        for p in m.get_editor_property('vector_parameter_values'): v = p.parameter_value; out.append('  V %s = %.3f %.3f %.3f %.3f' % (p.parameter_info.name, v.r, v.g, v.b, v.a))
        for p in m.get_editor_property('texture_parameter_values'): out.append('  T %s = %s' % (p.parameter_info.name, p.parameter_value.get_path_name() if p.parameter_value else None))
        try:
            for n in MEL.get_static_switch_parameter_names(m): out.append('  SW %s = %s' % (n, MEL.get_material_instance_static_switch_parameter_value(m, n)))
        except Exception as e: out.append('  sw err %s' % e)
        m = m.get_editor_property('parent')
    else:
        for n in ('shading_model', 'blend_mode', 'subsurface_profile'):
            try: out.append('  %s = %s' % (n, m.get_editor_property(n)))
            except Exception: pass
        for n in MEL.get_scalar_parameter_names(m): out.append('  dS %s = %s' % (n, MEL.get_material_default_scalar_parameter_value(m, n)))
        for n in MEL.get_vector_parameter_names(m): out.append('  dV %s = %s' % (n, MEL.get_material_default_vector_parameter_value(m, n)))
        for n in MEL.get_texture_parameter_names(m):
            t = MEL.get_material_default_texture_parameter_value(m, n); out.append('  dT %s = %s' % (n, t.get_path_name() if t else None))
        m = None
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/skin_mat.txt', 'w', encoding='utf8').write('\n'.join(out)); print('SKINMAT', len(out))
