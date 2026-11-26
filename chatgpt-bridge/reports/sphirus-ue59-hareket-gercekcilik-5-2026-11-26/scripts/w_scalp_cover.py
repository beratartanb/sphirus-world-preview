# w_scalp_cover.py (write, gated): scalp cover under the bun. The crown showed pale scalp through the strands (no-hair capture: scalp is
# light beige in this light). Cover = the Sph8 face triangles under the strand roots (scalp_region.py: roots within 0.7 cm, eroded 1.6 cm
# from the hairline so the edge stays under hair), pushed 0.12 cm out along the normal, in head-bone space, as a static mesh with a dark
# copper root-colour material, attached to the Face component at socket 'head'. Face mesh untouched.
import unreal as u, json
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
E = u.EditorAssetLibrary; G = u.GeometryScript_AssetUtils; Q = u.GeometryScript_MeshQueries; Lb = u.GeometryScript_List; ME = u.GeometryScript_MeshEdits; N = u.GeometryScript_Normals; BW = u.GeometryScript_BoneWeights
DST = '/Game/Sphirus/CharacterLab/B13_20261126/Hair/'; SMP = DST + 'SM_Sph8_ScalpCover'; MP = DST + 'M_Sph8_ScalpCover'
R = json.load(open(u.Paths.project_dir() + 'Saved/UE59Work/b11/scalp_region.json')); keep = set(R['v'])
FD = json.load(open(u.Paths.project_dir() + 'Saved/UE59Work/b4/dump_face.json'))['lods']['0']['v']
face = u.load_asset('/Game/Sphirus/CharacterLab/Sph_20261108/Built/MHC_Sph8/Face/SKM_MHC_Sph8_FaceMesh')
dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL
G.copy_mesh_from_skeletal_mesh(face, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod)
P = Lb.convert_vector_list_to_array(Q.get_all_vertex_positions(dm, False)[1]); assert len(P) == len(FD), (len(P), len(FD))
err = max(abs(P[i].x - FD[i][0]) + abs(P[i].y - FD[i][1]) + abs(P[i].z - FD[i][2]) for i in range(0, len(P), 37)); assert err < 0.01, err
# head bone component transform from the bone hierarchy
def pick(r, cls):
    for x in (r if isinstance(r, (tuple, list)) else [r]):
        if isinstance(x, (list, tuple, u.Array)) and len(x) and isinstance(x[0], cls): return list(x)
bones = pick(BW.get_all_bones_info(dm), u.GeometryScriptBoneInfo); comp = {}
for b in bones:
    t = b.local_transform; comp[b.index] = t if b.parent_index < 0 else u.MathLibrary.compose_transforms(t, comp[b.parent_index])
hb = [b for b in bones if str(b.name) == 'head'][0]; HT = comp[hb.index]; print('SC head comp', HT.translation)
NL = Lb.convert_vector_list_to_array(N.get_mesh_per_vertex_normals(dm, True)[1])
r_ = Q.get_all_triangle_indices(dm, False); tl = next(x for x in (r_ if isinstance(r_, tuple) else (r_,)) if isinstance(x, u.GeometryScriptTriangleList)); TRI = Lb.convert_triangle_list_to_array(tl)
drop = [i for i, t in enumerate(TRI) if not (t.x in keep and t.y in keep and t.z in keep)]
ME.delete_triangles_from_mesh(dm, Lb.convert_array_to_index_list(drop), True); u.GeometryScript_MeshRepair.remove_unused_vertices(dm)
for v in keep:
    n = NL[v]; p = P[v] + u.Vector(n.x * 0.12, n.y * 0.12, n.z * 0.12)
    ME.set_vertex_position(dm, v, u.MathLibrary.inverse_transform_location(HT, p), True)
N.recompute_normals(dm, u.GeometryScriptCalculateNormalsOptions())
print('SC verts', len(Lb.convert_vector_list_to_array(Q.get_all_vertex_positions(dm, True)[1])), 'tris kept', len(TRI) - len(drop))
# material: dark copper (hair root tone), rough, non-metal
if E.does_asset_exist(MP): mat = u.load_asset(MP)
else:
    mat = u.AssetToolsHelpers.get_asset_tools().create_asset('M_Sph8_ScalpCover', DST.rstrip('/'), u.Material, u.MaterialFactoryNew()); ML = u.MaterialEditingLibrary
    c = ML.create_material_expression(mat, u.MaterialExpressionConstant3Vector, -300, 0); c.set_editor_property('constant', u.LinearColor(0.085, 0.03, 0.012, 1.0))
    r = ML.create_material_expression(mat, u.MaterialExpressionConstant, -300, 200); r.set_editor_property('r', 0.75)
    s = ML.create_material_expression(mat, u.MaterialExpressionConstant, -300, 300); s.set_editor_property('r', 0.2)
    ML.connect_material_property(c, '', u.MaterialProperty.MP_BASE_COLOR); ML.connect_material_property(r, '', u.MaterialProperty.MP_ROUGHNESS); ML.connect_material_property(s, '', u.MaterialProperty.MP_SPECULAR)
    ML.recompile_material(mat); E.save_loaded_asset(mat, False)
o = u.GeometryScriptCreateNewStaticMeshAssetOptions()
for k, v in (('enable_recompute_normals', False), ('enable_recompute_tangents', True), ('enable_collision', False), ('use_original_vertex_order', False)):
    try: o.set_editor_property(k, v)
    except Exception: pass
if E.does_asset_exist(SMP):
    sm = u.load_asset(SMP); G.copy_mesh_to_static_mesh(dm, sm, u.GeometryScriptCopyMeshToAssetOptions(), u.GeometryScriptMeshWriteLOD())
else:
    r_ = u.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(dm, SMP, o); sm = next(x for x in (r_ if isinstance(r_, tuple) else (r_,)) if isinstance(x, u.StaticMesh)); print('SC created', r_)
sm.set_material(0, mat); print('SC sm saved', E.save_loaded_asset(sm, False))
# attach to the player
bp = u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); sub = u.get_engine_subsystem(u.SubobjectDataSubsystem); L = u.SubobjectDataBlueprintFunctionLibrary
def comps():
    out = {}
    for h in sub.k2_gather_subobject_data_for_blueprint(bp):
        ob = L.get_object(sub.k2_find_subobject_data_from_handle(h))
        if ob: out[ob.get_name().split('_GEN')[0]] = (h, ob)
    return out
cs = comps()
if 'HairScalp' not in cs:
    nh, fail = sub.add_new_subobject(u.AddNewSubobjectParams(parent_handle=cs['Face'][0], new_class=u.StaticMeshComponent, blueprint_context=bp)); sub.rename_subobject(nh, u.Text('HairScalp')); cs = comps()
sc = cs['HairScalp'][1]; sc.set_editor_property('static_mesh', sm); sc.set_editor_property('attach_socket_name', 'head') if False else None
try: sc.set_editor_property('cast_shadow', False)
except Exception as e: print('SC shadow', e)
sc.set_collision_enabled(u.CollisionEnabled.NO_COLLISION) if hasattr(sc, 'set_collision_enabled') else None
# socket: SCS node attach socket
try:
    nd = None
    for n in bp.get_editor_property('simple_construction_script').get_all_nodes():
        if n.get_editor_property('component_template') == sc: nd = n
    nd.set_editor_property('attach_to_name', 'head'); print('SC socket', nd.get_editor_property('attach_to_name'))
except Exception as e: print('SC socket err', repr(e)[:200])
u.BlueprintEditorLibrary.compile_blueprint(bp)
print('SC player saved', E.save_loaded_asset(bp, False)); print('DIRTY', [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
