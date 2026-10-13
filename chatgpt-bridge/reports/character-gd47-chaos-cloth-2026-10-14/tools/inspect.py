"""GD47 read-only inspection (nothing saved): pawn components in BP_Player_MM, garment materials, Chaos shorts m1 materials/LODs,
PHYS_CR_HenleyCollider bodies, and the Henley f5 LOD0 source mesh (positions/triangles/material ids, DynamicMesh order) for the
offline MaxDistance weight design. Writes data/inspect.json + data/henley_f5_mesh.json.gz."""
import unreal as u, json, gzip, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD47_ChaosCloth_20261014/data'; O.mkdir(parents=True, exist_ok=True)
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); BFL = u.SubobjectDataBlueprintFunctionLibrary; q = u.GeometryScript_MeshQueries; lst = u.GeometryScript_List
BP = '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM'; bp = u.load_asset(BP); rep = {'components': {}}
def pn(x): return x.get_path_name() if x else None
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    d = BFL.get_data(h); o = BFL.get_object(d)
    if o is None: continue
    e = {'class': o.get_class().get_name()}
    try: e['parent'] = str(BFL.get_object(BFL.get_data(sds.find_parent_handle(h) if hasattr(sds, 'find_parent_handle') else h)).get_name())
    except Exception: pass
    if isinstance(o, u.SceneComponent):
        e['attach_parent'] = o.get_attach_parent().get_name() if o.get_attach_parent() else None; e['visible'] = o.get_editor_property('visible'); e['hidden_in_game'] = o.get_editor_property('hidden_in_game')
    if isinstance(o, u.SkeletalMeshComponent):
        e['mesh'] = pn(o.get_skeletal_mesh_asset()); e['override_materials'] = [pn(m) for m in o.get_editor_property('override_materials')]
        e['materials'] = [pn(o.get_material(i)) for i in range(o.get_num_materials())]
    rep['components'][o.get_name()] = e
for p in ('/Game/Sphirus/CharacterLab/GD46_GarmentFit_20261013/Outfit/SKM_GD46_Henley_f5', '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Outfit/SKM_LK_Shorts_g16c'):
    m = u.load_asset(p); mats = []
    for sm in m.get_editor_property('materials'):
        mi = sm.get_editor_property('material_interface'); par = mi.get_editor_property('parent') if isinstance(mi, u.MaterialInstance) else None
        mats.append({'slot': str(sm.get_editor_property('material_slot_name')), 'mi': pn(mi), 'parent': pn(par)})
    rep[p.rsplit('/', 1)[-1]] = {'materials': mats, 'physics_asset': pn(m.get_editor_property('physics_asset')), 'lods': m.get_lod_num() if hasattr(m, 'get_lod_num') else None}
ca = u.load_asset('/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Cloth/CA_CR_Shorts_m1')
rep['CA_CR_Shorts_m1'] = {'materials': [pn(m.get_editor_property('material_interface')) for m in ca.get_editor_property('materials')], 'pa': pn(ca.get_editor_property('physics_asset')) if hasattr(ca, 'physics_asset') else None}
try: rep['CA_CR_Shorts_m1']['props'] = [p for p in dir(ca) if not p.startswith('_')][:200]
except Exception: pass
for mp in rep['CA_CR_Shorts_m1']['materials']:
    mi = u.load_asset(mp); rep.setdefault('shorts_cloth_mi_parent', {})[mp] = pn(mi.get_editor_property('parent'))
pa = u.load_asset('/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Cloth/PHYS_CR_HenleyCollider'); bodies = {}
for b in u.ObjectIterator(u.BodySetup):
    if b.get_outer() != pa: continue
    g = b.get_editor_property('agg_geom'); bodies[str(b.get_editor_property('bone_name'))] = {'sphyl': [(round(s.get_editor_property('radius'), 2), round(s.get_editor_property('length'), 2)) for s in g.get_editor_property('sphyl_elems')], 'sphere': len(g.get_editor_property('sphere_elems')), 'box': len(g.get_editor_property('box_elems')), 'convex': len(g.get_editor_property('convex_elems'))}
rep['henley_collider_bodies'] = bodies
skm = u.load_asset('/Game/Sphirus/CharacterLab/GD46_GarmentFit_20261013/Outfit/SKM_GD46_Henley_f5'); dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(skm, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); rep['copy'] = str(r[-1])
P = lst.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); T = lst.convert_triangle_list_to_array(q.get_all_triangle_indices(dm, False)[1])
_r = u.GeometryScript_Materials.get_all_triangle_material_i_ds(dm); _r = _r if isinstance(_r, tuple) else (_r,); mids = lst.convert_index_list_to_array([x for x in _r if isinstance(x, u.GeometryScriptIndexList)][0])
gzip.open(O/'henley_f5_mesh.json.gz', 'wt').write(json.dumps({'P': [[round(p.x, 4), round(p.y, 4), round(p.z, 4)] for p in P], 'T': [[t.x, t.y, t.z] for t in T], 'M': list(mids)}))
rep['henley_f5'] = {'verts': len(P), 'tris': len(T), 'mat_counts': {str(k): list(mids).count(k) for k in set(mids)}}
(O/'inspect.json').write_text(json.dumps(rep, indent=1, default=str)); print('GD47_INSPECT', json.dumps({k: v for k, v in rep.items() if k != 'components'}, default=str)[:1500], flush=True)
