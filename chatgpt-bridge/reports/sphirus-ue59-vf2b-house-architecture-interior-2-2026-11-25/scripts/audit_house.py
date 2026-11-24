# VF2B read-only: plaster material parameters, fireplace/soot decal materials, which architecture actors use the lime plaster.
import unreal as u
mel = u.MaterialEditingLibrary
def dump(p, full=True):
    m = u.load_asset(p)
    if not m: print('AH missing', p); return None
    base = m.get_base_material()
    print('AH', p.split('/')[-1], '| parent', m.get_editor_property('parent').get_name() if isinstance(m, u.MaterialInstance) else '-', '| base', base.get_path_name().split('.')[0], str(base.get_editor_property('material_domain')).split('.')[-1][:16], str(base.get_editor_property('blend_mode')).split('.')[-1][:20])
    if full:
        print('AH   scalars', {str(n): round(mel.get_material_instance_scalar_parameter_value(m, n), 3) for n in mel.get_scalar_parameter_names(m)})
        print('AH   vectors', {str(n): [round(x, 3) for x in (lambda c: (c.r, c.g, c.b))(mel.get_material_instance_vector_parameter_value(m, n))] for n in mel.get_vector_parameter_names(m)})
        print('AH   textures', {str(n): (mel.get_material_instance_texture_parameter_value(m, n).get_name() if mel.get_material_instance_texture_parameter_value(m, n) else None) for n in mel.get_texture_parameter_names(m)})
        print('AH   switches', {str(n): mel.get_material_instance_static_switch_parameter_value(m, n) for n in mel.get_static_switch_parameter_names(m)})
    return m
dump('/Game/SphirusHouse/LivedIn_R05/Materials/Instances/MI_R3_Surface_lime')
dump('/Game/SphirusHouse/LivedIn_R05/Materials/Instances/MI_R3_Surface_masonry')
dump('/Game/SphirusHouse/LivedIn_R05/Materials/Instances/MI_R3_hearth_OriginalAtlas')
acts = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
for a in acts:
    if isinstance(a, u.DecalActor) and a.get_actor_label() in ('DWR_G_SootHearth', 'DWR_G_Hearth', 'DWR_G_SootRange', 'HP_Damp_EastBase', 'DWR_G_Bench'):
        d = a.decal; m = d.get_decal_material(); r = a.get_actor_rotation(); s = a.get_actor_scale3d()
        print('AH decal', a.get_actor_label(), m.get_path_name().split('.')[0] if m else None, 'size', d.get_editor_property('decal_size'), 'scale', [round(v, 2) for v in (s.x, s.y, s.z)], 'rot', [round(v) for v in (r.pitch, r.yaw, r.roll)], 'lvl', a.get_outer().get_outer().get_name())
        if m and isinstance(m, u.MaterialInstance): dump(m.get_path_name().split('.')[0])
ar = u.AssetRegistryHelpers.get_asset_registry()
for d in ('/Game/SphirusHouse/LivedIn_R05/Materials', '/Game/Sphirus/Interior', '/Game/GraceRanger/Environment/Interior20261111'):
    xs = [str(a.asset_name) for a in ar.get_assets_by_path(d, recursive=True) if any(k in str(a.asset_name) for k in ('Decal', 'DWR', 'HP_', 'Soot', 'Dust', 'Ash', 'Stain', 'Grime'))]
    if xs: print('AH decal assets', d, xs[:40])
lime = [a for a in acts if isinstance(a, u.StaticMeshActor) and any(m and m.get_name() == 'MI_R3_Surface_lime' for m in a.static_mesh_component.get_materials())]
print('AH lime actors', len(lime), [a.get_actor_label()[:34] for a in lime][:30])
