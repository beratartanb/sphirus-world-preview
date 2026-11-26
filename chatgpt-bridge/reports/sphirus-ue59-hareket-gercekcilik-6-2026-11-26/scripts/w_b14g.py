# w_b14g.py (write, gated): B14 garments = B13 top and shorts pulled toward the body at the back and sides (g_tighten.py; front drape kept).
# Delta relative to the source garments (s13 + tightening). keep_normals False: b4_apply keeps the source (authored) normals where a vertex
# did not move and blends to recomputed normals where it moved (> 0.3 cm full). Also measures the source garments' stored-vs-recomputed
# normal deviation (are the B13 deviations authored or caused by the earlier keep_normals bakes?).
import builtins, unreal as u, math
D = u.Paths.project_dir(); B = '/Game/Sphirus/CharacterLab/B14_20261126'; W = D + 'Saved/UE59Work/b4/s14/'
G = u.GeometryScript_AssetUtils; L = u.GeometryScript_List; N = u.GeometryScript_Normals
for p in ('/Game/Sphirus/CharacterLab/VF2_20261124/Garments/SKM_Sph_RetroTop_VF2', '/Game/Sphirus/CharacterLab/Day_20261107/Garments/SKM_Sph_Pants70'):
    dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL
    G.copy_mesh_from_skeletal_mesh(u.load_asset(p), dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod)
    n0 = L.convert_vector_list_to_array(N.get_mesh_per_vertex_normals(dm, True)[1]); N.recompute_normals(dm, u.GeometryScriptCalculateNormalsOptions()); n1 = L.convert_vector_list_to_array(N.get_mesh_per_vertex_normals(dm, True)[1])
    ang = sorted(math.degrees(math.acos(max(-1, min(1, x.x * y.x + x.y * y.y + x.z * y.z)))) for x, y in zip(n0, n1))
    print('NRMSRC', p.split('/')[-1], 'p50 %.1f p90 %.1f p99 %.1f' % (ang[len(ang) // 2], ang[int(len(ang) * .9)], ang[int(len(ang) * .99)]))
builtins.B4_APPLY = [{'src': '/Game/Sphirus/CharacterLab/VF2_20261124/Garments/SKM_Sph_RetroTop_VF2', 'dst': B + '/Garments/SKM_Sph_RetroTop_B14', 'delta': W + 'delta_g_retrotop.json', 'keep_normals': False, 'reuse': True},
                     {'src': '/Game/Sphirus/CharacterLab/Day_20261107/Garments/SKM_Sph_Pants70', 'dst': B + '/Garments/SKM_Sph_Pants70_B14', 'delta': W + 'delta_g_pants70.json', 'keep_normals': False, 'reuse': True}]
exec(open(D + 'Tools/UE59_20261124/b4_apply.py', encoding='utf8').read())
