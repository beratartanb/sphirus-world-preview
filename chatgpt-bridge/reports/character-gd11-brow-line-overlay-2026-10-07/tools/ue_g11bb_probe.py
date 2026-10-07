"""pass BB (brow line): probe the library brow SOURCE head (SKM_Groom_Head_Legacy01) vs the candidate face: vertex counts, bounds, brow-area positions."""
import unreal as u, json
q = u.GeometryScript_MeshQueries; l = u.GeometryScript_List; out = {}
def fresh(m):
    dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
    r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); return dm, str(r[-1] if isinstance(r, tuple) else r)
for k, p in (('src', '/MetaHumanCharacter/Optional/Grooms/GroomMesh/SKM_Groom_Head_Legacy01'), ('face', '/Game/Sphirus/CharacterLab/GD11_FaceR_20261006/Face/SKM_G11RR_Face_ss4')):
    m = u.load_asset(p); dm, st = fresh(m); P = l.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1])
    xs = [v.x for v in P]; ys = [v.y for v in P]; zs = [v.z for v in P]
    br = [(round(v.x, 2), round(v.y, 2), round(v.z, 2)) for v in P if abs(v.x-3.0) < 0.3 and 164.0 < v.z < 165.5][:4]
    out[k] = {'status': st, 'n': len(P), 'x': [round(min(xs), 2), round(max(xs), 2)], 'y': [round(min(ys), 2), round(max(ys), 2)], 'z': [round(min(zs), 2), round(max(zs), 2)], 'brow_sample': br,
              'first3': [(round(v.x, 3), round(v.y, 3), round(v.z, 3)) for v in P[:3]]}
print('BBPROBE', json.dumps(out))
