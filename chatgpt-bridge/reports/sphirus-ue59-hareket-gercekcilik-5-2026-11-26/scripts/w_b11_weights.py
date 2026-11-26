# w_b11_weights.py (write, gated): B11 skin-weight continuity at the closed region. Matched vertices carry B10 (Sph8 build) weights,
# the 744 closed-region vertices carry template weights; the two differ (sample max 0.115). Correction field (B10 - template) on the
# matched vertices is continued harmonically into the region (Jacobi, boundary fixed) and added to the template weights there;
# result clamped >= 0, top 8 influences, normalised. Positions/normals/UVs untouched.
import unreal as u, json, builtins
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
G = u.GeometryScript_AssetUtils; Q = u.GeometryScript_MeshQueries; BW = u.GeometryScript_BoneWeights
DST = getattr(builtins, 'B11_DST', '/Game/Sphirus/CharacterLab/B11_20261126/Body/SKM_Sph_B11_BodyMesh'); TM = '/MetaHumanCharacter/Body/IdentityTemplate/SKM_Body'
J = json.load(open(u.Paths.project_dir() + 'Saved/UE59Work/b11/b11_pos.json')); U = sorted(J['U']); US = set(U)
def rd(p):
    dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
    G.copy_mesh_from_skeletal_mesh(u.load_asset(p), dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); return dm
a = u.load_asset(DST); dm = rd(DST); dt = rd(TM); prof = u.GeometryScriptBoneWeightProfile()
def gw(m, v):
    r = BW.get_vertex_bone_weights(m, v, prof)
    for e in (r if isinstance(r, tuple) else (r,)):
        if isinstance(e, (list, tuple, u.Array)) and (len(e) == 0 or isinstance(e[0], u.GeometryScriptBoneWeight)): return {w.bone_index: w.weight for w in e}
    return {}
def nbrs(m, v):
    r = Q.get_vertex_connected_vertices(m, v)
    for e in (r if isinstance(r, tuple) else (r,)):
        if not isinstance(e, u.DynamicMesh): return [int(x) for x in e]
    return []
NB = {v: nbrs(dm, v) for v in U}
B = sorted({x for v in U for x in NB[v] if x not in US})
corr = {}
for b in B:
    wb = gw(dm, b); wt = gw(dt, b); corr[b] = {k: wb.get(k, 0.0) - wt.get(k, 0.0) for k in set(wb) | set(wt)}
for v in U: corr[v] = {}
for it in range(300):
    new = {}
    for v in U:
        acc = {}
        for x in NB[v]:
            for k, d in corr[x].items(): acc[k] = acc.get(k, 0.0) + d
        n = float(len(NB[v])); new[v] = {k: d / n for k, d in acc.items() if abs(d / n) > 1e-5}
    corr.update(new)
mx = 0.0; out = 0
for v in U:
    w = gw(dt, v)
    for k, d in corr[v].items(): w[k] = w.get(k, 0.0) + d
    top = sorted(((k, x) for k, x in w.items() if x > 1e-4), key=lambda t: -t[1])[:8]; s = sum(x for _, x in top) or 1.0
    old = gw(dm, v); mx = max(mx, max(abs(old.get(k, 0) - x / s) for k, x in top))
    L = []
    for k, x in top:
        b = u.GeometryScriptBoneWeight(); b.bone_index = k; b.weight = x / s; L.append(b)
    BW.set_vertex_bone_weights(dm, v, L, prof); out += 1
print('B11W boundary', len(B), 'region', out, 'max weight change', round(mx, 4))
wl = u.GeometryScriptMeshWriteLOD(); wl.lod_index = 0; o = u.GeometryScriptCopyMeshToAssetOptions()
for k, vv in (('enable_recompute_normals', False), ('enable_recompute_tangents', True), ('emit_transaction', False), ('remap_bone_indices_to_match_asset', True)):
    try: o.set_editor_property(k, vv)
    except Exception as e: print('B11W opt', k, repr(e)[:100])
print('B11W write', G.copy_mesh_to_skeletal_mesh(dm, a, o, wl)[1]); print('B11W saved', u.EditorAssetLibrary.save_loaded_asset(a, False))
