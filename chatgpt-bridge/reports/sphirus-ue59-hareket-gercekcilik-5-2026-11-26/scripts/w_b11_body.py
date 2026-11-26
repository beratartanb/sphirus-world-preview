# w_b11_body.py (write, gated): B11 body = the complete MetaHuman template body topology (SKM_Body, no hidden-face removal) carrying
# the B10 shape. b11_match.py matched all 29,711 B10 vertices to template vertices (UV + position at seams); the 744 template vertices
# B10 lacks (waist band, hip holes, crotch: one connected region) got a biharmonic continuation of the B10 displacement.
# Written into a duplicate of the B10 body asset (Sph8 reference pose, physics, DNA user data, material), LOD0 only.
# Matched vertices keep B10's skin weights and normals; the hole region and two rings around it get template weights / recomputed normals.
import unreal as u, json, builtins
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
E = u.EditorAssetLibrary; G = u.GeometryScript_AssetUtils; Q = u.GeometryScript_MeshQueries; L = u.GeometryScript_List; BW = u.GeometryScript_BoneWeights; N = u.GeometryScript_Normals
SRC = '/Game/Sphirus/CharacterLab/B10_20261126/Body/SKM_Sph_B10_BodyMesh'; TM = '/MetaHumanCharacter/Body/IdentityTemplate/SKM_Body'
DST = getattr(builtins, 'B11_DST', '/Game/Sphirus/CharacterLab/B11_20261126/Body/SKM_Sph_B11_BodyMesh')
J = json.load(open(u.Paths.project_dir() + 'Saved/UE59Work/b11/' + getattr(builtins, 'B11_POS', 'b11_pos.json')))
if not E.does_asset_exist(DST): assert E.duplicate_asset(SRC, DST)
a = u.load_asset(DST)
def rd(p):
    dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
    G.copy_mesh_from_skeletal_mesh(u.load_asset(p), dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); return dm
dt = rd(TM); db = rd(SRC)
nt = len(L.convert_vector_list_to_array(Q.get_all_vertex_positions(dt, False)[1])); assert nt == len(J['pos']) == 30455, nt
MB = J['map']; U = set(J['U'])
# positions
PL = L.convert_array_to_vector_list([u.Vector(*p) for p in J['pos']])
u.GeometryScript_MeshEdits.set_all_mesh_vertex_positions(dt, PL); print('B11 positions set', nt)
def nbrs(m, v):
    r = Q.get_vertex_connected_vertices(m, v)
    for e in (r if isinstance(r, tuple) else (r,)):
        if not isinstance(e, u.DynamicMesh): return [int(x) for x in e]
    return []
ring = set(U)
for _ in range(2): ring |= {x for v in list(ring) for x in nbrs(dt, v)}
print('B11 hole verts', len(U), 'with 2 rings', len(ring))
prof = u.GeometryScriptBoneWeightProfile()
def gw(m, v):
    r = BW.get_vertex_bone_weights(m, v, prof)
    for e in (r if isinstance(r, tuple) else (r,)):
        if isinstance(e, (list, tuple, u.Array)) and (len(e) == 0 or isinstance(e[0], u.GeometryScriptBoneWeight)): return list(e)
    return []
# skin weights: B10 values on matched vertices (compare first)
diff = 0; mx = 0.0
for i in range(0, len(MB), 97):
    wb = {w.bone_index: w.weight for w in gw(db, i)}; wt = {w.bone_index: w.weight for w in gw(dt, MB[i])}
    d = max(abs(wb.get(k, 0) - wt.get(k, 0)) for k in set(wb) | set(wt)) if (wb or wt) else 0; mx = max(mx, d); diff += d > 1e-3
print('B11 weight sample: differing', diff, 'of', len(range(0, len(MB), 97)), 'max', round(mx, 4))
if diff:
    for i, j in enumerate(MB): BW.set_vertex_bone_weights(dt, j, gw(db, i), prof)
    print('B11 weights copied from B10', len(MB))
# normals: recompute, then B10 normals outside the hole + 2 rings
N.recompute_normals(dt, u.GeometryScriptCalculateNormalsOptions())
NT = L.convert_vector_list_to_array(N.get_mesh_per_vertex_normals(dt, True)[1]); NB = L.convert_vector_list_to_array(N.get_mesh_per_vertex_normals(db, True)[1])
PB = L.convert_vector_list_to_array(Q.get_all_vertex_positions(db, False)[1]); kept = 0
for i, j in enumerate(MB):
    q = J['pos'][j]; p = PB[i]
    if j not in ring and abs(p.x - q[0]) + abs(p.y - q[1]) + abs(p.z - q[2]) < 0.01: NT[j] = NB[i]; kept += 1
print('B11 normals kept from B10', kept)
N.set_mesh_per_vertex_normals(dt, L.convert_array_to_vector_list(NT)); print('B11 normals set')
wl = u.GeometryScriptMeshWriteLOD(); wl.lod_index = 0; o = u.GeometryScriptCopyMeshToAssetOptions()
for k, vv in (('enable_recompute_normals', False), ('enable_recompute_tangents', True), ('emit_transaction', False), ('remap_bone_indices_to_match_asset', True)):
    try: o.set_editor_property(k, vv)
    except Exception as e: print('B11 opt', k, repr(e)[:100])
print('B11 write', G.copy_mesh_to_skeletal_mesh(dt, a, o, wl))
chk = rd(DST); n2 = len(L.convert_vector_list_to_array(Q.get_all_vertex_positions(chk, False)[1]))
print('B11 readback verts', n2, 'skel', a.skeleton.get_path_name(), 'mats', [x.material_interface.get_name() for x in a.materials])
assert n2 == 30455
print('B11 saved', E.save_loaded_asset(a, False))
