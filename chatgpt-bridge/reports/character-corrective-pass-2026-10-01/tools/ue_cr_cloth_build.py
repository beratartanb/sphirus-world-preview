"""CORRECTIVE pass: runtime CHAOS CLOTH asset for one garment (isolated in CharacterCorrective_20261001/Cloth).
1. garment skeletal mesh LOD0 -> DynamicMesh (vertex order known) -> per-vertex MaxDistance weight (region function by 3D position,
   pinned = 0, simulated -> 1 with smooth ramps) as a named weight layer -> static mesh SM_CR_<name>_Sim (weight layer survives
   MeshDescription -> DynamicMesh in StaticMeshImport, which copies weight layers into cloth weight maps: no sim-vertex-order guessing)
2. clothing-enabled material copies (masters duplicated into the corrective folder, never the lookdev originals) on the static mesh
3. Dataflow (copy of the engine empty cloth template): StaticMeshImport -> TransferSkinWeights(garment SKM) -> MaxDistance ->
   LongRangeAttachment (tethers from the kinematic set) -> Damping -> Collision -> SetPhysicsAsset -> ClothAssetTerminal
builtins.CR_CLOTH = {'name', 'skm', 'kind': 'shorts'|'henley', 'high': cm, 'pa': physics asset, 'damping': f, 'props': {node: {prop: text}}}
Writes Saved/Codex/CharacterCorrective_20261001/cloth_<name>.json"""
import unreal as u, json, pathlib, builtins, math
C = builtins.CR_CLOTH; EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; L = u.DataflowEditorBlueprintLibrary; q = u.GeometryScript_MeshQueries; lst = u.GeometryScript_List
G = '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001'; F = G+'/Cloth'; MD = G+'/Outfit/Materials'; NAME = C['name']; out = {'cfg': {k: v for k, v in C.items()}}
def pick(r, typ):
    r = r if isinstance(r, tuple) else (r,); return [x for x in r if isinstance(x, typ)][0]
def ss(x): x = max(0.0, min(1.0, x)); return x*x*(3-2*x)
# ---------------------------------------------------------------- weights
def w_shorts(x, y, z):
    if z >= 97.5: return 0.0                                                      # waistband / band seam: skinned
    t = ss((96.5-z)/18.0)**1.4                                                     # 0 at the band -> 1 at the hem (~76)
    core = 1.0-math.exp(-((x/5.5)**2+((z-77.0)/6.0)**2))                            # crotch core stays pinned
    rise = ss((abs(x)-1.5)/4.0) if z > 80 else 1.0                                 # centre-front / centre-back rise pinned
    side = 1.0+0.35*ss((abs(x)-11.0)/4.0)                                          # outer thigh / dolphin side a little freer
    return max(0.0, min(1.0, t*core*rise*side))
def w_henley(x, y, z):
    if z >= 113.0 or abs(x) > 17.5: return 0.0                                     # upper torso, armholes, sleeves: skinned / corrective
    t = ss((112.0-z)/15.0)**1.5                                                    # 0 at z 112 -> 1 at the hem (~97)
    arm = 1.0-ss((abs(x)-15.0)/2.5)
    plk = 0.75 if (abs(x) < 3.0 and y > 6.0) else 1.0                              # placket a bit steadier
    return max(0.0, min(1.0, t*arm*plk))
def w_henley_lower(x, y, z):   # hybrid Henley: lower torso piece below the cut; the cut rows stay pinned to the skinned / corrective upper garment
    cz = C.get('pin_from', C['keep']['zmax']); return max(0.0, min(1.0, ss((cz-1.5-z)/10.0)**1.3))
WF = {'shorts': w_shorts, 'henley': w_henley, 'henley_lower': w_henley_lower}[C['kind']]
skm = u.load_asset(C['skm']); dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(skm, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); assert 'SUCCESS' in str(r[-1]), r
if C.get('keep'):   # cut the simulated piece: keep only triangles with centroid z < zmax and |x| < xmax (complement of the hidden slot of the skinned garment)
    K = C['keep']; Pv = lst.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); Tr = lst.convert_triangle_list_to_array(q.get_all_triangle_indices(dm, False)[1])
    rm = [i for i, t in enumerate(Tr) if not ((Pv[t.x].z+Pv[t.y].z+Pv[t.z].z)/3.0 < K['zmax'] and abs((Pv[t.x].x+Pv[t.y].x+Pv[t.z].x)/3.0) < K['xmax'])]
    il = pick(lst.convert_array_to_index_list(rm), u.GeometryScriptIndexList); u.GeometryScript_MeshEdits.delete_triangles_from_mesh(dm, il)
    u.GeometryScript_MeshRepair.remove_unused_vertices(dm); u.GeometryScript_MeshRepair.compact_mesh(dm); out['cut_removed_tris'] = len(rm)
if C.get('overlap_from') is not None:   # overlap band (pinned) over the skinned garment's visible edge: pushed out along the normal so it covers the seam
    Nv = lst.convert_vector_list_to_array(pick(u.GeometryScript_Normals.get_mesh_per_vertex_normals(dm), u.GeometryScriptVectorList)); Pv = lst.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); nb = 0
    for i, (p_, n_) in enumerate(zip(Pv, Nv)):
        if p_.z > C['overlap_from']-0.5:
            o_ = C.get('overlap_push', 0.08)*min(1.0, (p_.z-C['overlap_from']+0.5)/0.5); u.GeometryScript_MeshEdits.set_vertex_position(dm, i, u.Vector(p_.x+n_.x*o_, p_.y+n_.y*o_, p_.z+n_.z*o_), True); nb += 1
    out['overlap_verts'] = nb
if C.get('flare'):   # hem ease ("more hem fabric", corrective pass): the rest shape of the simulated piece widens / drops toward the hem so the cloth forms soft folds over the waistband
    FL = C['flare']; Pv = lst.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); nf = 0
    for i, p_ in enumerate(Pv):
        if p_.z < FL['z0']:
            t_ = ss((FL['z0']-p_.z)/(FL['z0']-FL['z1'])); sc_ = 1.0+FL['radial']*t_; yc = FL.get('yc', 1.0)
            u.GeometryScript_MeshEdits.set_vertex_position(dm, i, u.Vector(p_.x*sc_, yc+(p_.y-yc)*sc_, p_.z-FL.get('drop', 0.0)*t_), True); nf += 1
    out['flare_verts'] = nf
P = lst.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); W = [WF(p.x, p.y, p.z) for p in P]
out['verts'] = len(P); out['weights'] = {'pinned(0)': sum(1 for w in W if w <= 0.0), 'partial': sum(1 for w in W if 0 < w < 0.6), 'free(>=0.6)': sum(1 for w in W if w >= 0.6)}
h = pick(u.GeometryScript_WeightMaps.find_or_add_mesh_weight_map(dm, 'MaxDistance'), u.GeometryScriptWeightMapHandle)
sl = pick(lst.convert_array_to_scalar_list(W), u.GeometryScriptScalarList); u.GeometryScript_WeightMaps.set_mesh_weight_map_values(dm, sl, h, False)
chk = lst.convert_scalar_list_to_array(pick(u.GeometryScript_WeightMaps.get_mesh_weight_map_values(dm, h, False), u.GeometryScriptScalarList)); out['weight_roundtrip_max_err'] = max(abs(a-b) for a, b in zip(chk, W))
# ---------------------------------------------------------------- clothing-enabled materials (corrective copies)
SRCM = '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Outfit/Materials'
for src, dst in (('M_LK_Textile_B', 'M_CR_Textile_B'), ('M_LK_Textile', 'M_CR_Textile')):
    if not EAL.does_asset_exist(MD+'/'+dst): assert EAL.duplicate_asset(SRCM+'/'+src, MD+'/'+dst)
    m = u.load_asset(MD+'/'+dst)
    if not m.get_editor_property('used_with_clothing'):
        m.set_editor_property('used_with_clothing', True); m.set_editor_property('used_with_skeletal_mesh', True); ME.recompile_material(m)
    EAL.save_loaded_asset(m, False)
mats = []
for sm in skm.get_editor_property('materials'):
    mi = sm.get_editor_property('material_interface'); dst = MD+'/'+mi.get_name()+'_cloth'
    if not EAL.does_asset_exist(dst): assert EAL.duplicate_asset(mi.get_path_name().split('.')[0], dst)
    c = u.load_asset(dst); par = c.get_editor_property('parent').get_name()
    ME.set_material_instance_parent(c, u.load_asset(MD+'/'+('M_CR_Textile_B' if par.endswith('_B') else 'M_CR_Textile'))); ME.update_material_instance(c); EAL.save_loaded_asset(c, False)
    mats.append((c, sm.get_editor_property('material_slot_name')))
out['materials'] = [m.get_name() for m, _ in mats]
# ---------------------------------------------------------------- static mesh carrying the weight layer
smp = F+f'/SM_CR_{NAME}_Sim'
if EAL.does_asset_exist(smp): EAL.delete_asset(smp)
o = u.GeometryScriptCreateNewStaticMeshAssetOptions(); o.set_editor_property('enable_recompute_normals', False); o.set_editor_property('enable_recompute_tangents', True); o.set_editor_property('enable_collision', False); o.set_editor_property('use_original_vertex_order', True)
r = u.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(dm, smp, o); sm_ = r[0] if isinstance(r, tuple) else r; assert sm_, r
sms = []
for m, slot in mats: s = u.StaticMaterial(); s.set_editor_property('material_interface', m); s.set_editor_property('material_slot_name', slot); sms.append(s)
sm_.set_editor_property('static_materials', sms); EAL.save_loaded_asset(sm_, False)
# ---------------------------------------------------------------- physics asset
pa = u.load_asset(C['pa']); out['pa'] = pa.get_path_name()
# ---------------------------------------------------------------- dataflow graph + cloth asset
cap, dfp = F+f'/CA_CR_{NAME}', F+f'/DF_CR_{NAME}'
for src, dst in (('/ChaosClothAsset/CA_Template', cap), ('/ChaosClothAsset/DF_EmptyClothAssetTemplate', dfp)):
    if EAL.does_asset_exist(dst): EAL.delete_asset(dst)
    assert EAL.duplicate_asset(src, dst)
ca = u.load_asset(cap); df = u.load_asset(dfp); di = ca.get_editor_property('dataflow_instance'); di.set_editor_property('dataflow_asset', df); ca.set_editor_property('dataflow_instance', di)
chain = [('FChaosClothAssetStaticMeshImportNode_v2', 'Import', {'StaticMesh': f"/Script/Engine.StaticMesh'{smp}.{smp.split('/')[-1]}'", 'bImportSimMesh': 'True', 'bImportRenderMesh': 'True', 'UVChannel': '0', 'SimMeshSection': str(C.get('sim_section', 0))}),   # sim = main fabric only; trims / cord render-only
         ('FChaosClothAssetTransferSkinWeightsNode', 'Skin', {'SkeletalMesh': f"/Script/Engine.SkeletalMesh'{C['skm']}.{C['skm'].split('/')[-1]}'", 'TargetMeshType': 'All'}),
         ('FChaosClothAssetProxyDeformerNode_v3', 'Proxy', {}),   # render sections (incl. trims / cord) follow the simulated fabric
         ('FChaosClothAssetSimulationMaxDistanceConfigNode', 'MaxDist', {'MaxDistance': f'(bIsAnimatable=True,Low=0.000000,High={C["high"]:.6f},WeightMap="MaxDistance")'}),
         ('FChaosClothAssetSimulationBackstopConfigNode', 'Backstop', {'BackstopDistance': f'(bIsAnimatable=True,Low={C.get("bs_dist", 0.0):.6f},High={C.get("bs_dist", 0.0):.6f},WeightMap="BackstopDistance")',
                                                                     'BackstopRadius': f'(bIsAnimatable=True,Low={C.get("bs_rad", 40.0):.6f},High={C.get("bs_rad", 40.0):.6f},WeightMap="BackstopRadius")'}),   # cloth cannot go behind its skinned (body-hugging) position
         ('FChaosClothAssetSimulationLongRangeAttachmentConfigNode_v2', 'Tethers', {}),
         ('FChaosClothAssetSimulationDampingConfigNode', 'Damping', {'DampingCoefficientWeighted': f'(bIsAnimatable=True,Low={C.get("damping", 0.08):.6f},High={C.get("damping", 0.08):.6f},WeightMap="DampingCoefficient")'}),
         ('FChaosClothAssetSimulationCollisionConfigNode', 'Collision', {}),
         ('FChaosClothAssetSetPhysicsAssetNode', 'SetPA', {'PhysicsAsset': f"/Script/Engine.PhysicsAsset'{pa.get_path_name()}'"})]
names, props, conns = [], {}, []
for i, (typ, base, pr) in enumerate(chain):
    n = str(L.add_dataflow_node(df, typ, base, u.Vector2D(-1600+i*250, 0))); names.append(n)
    for k, v in {**pr, **C.get('props', {}).get(base, {})}.items(): props[f'{base}.{k}'] = L.set_dataflow_node_property(df, n, k, v)
for a, b in zip(names[:-1], names[1:]): conns.append(L.connect_dataflow_nodes(df, a, 'Collection', b, 'Collection'))
conns.append(L.connect_dataflow_nodes(df, names[-1], 'Collection', 'ClothAssetTerminal', 'CollectionLods[0]'))
out['nodes'] = names; out['props'] = props; out['connections'] = conns
out['regen'] = u.DataflowBlueprintLibrary.regenerate_asset_from_dataflow(ca, False)
for x in (df, ca): EAL.save_loaded_asset(x, False)
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
pathlib.Path(u.Paths.project_dir(), f'Saved/Codex/CharacterCorrective_20261001/cloth_{NAME}.json').write_text(json.dumps(out, indent=1, default=str)); print('CR_CLOTH', json.dumps(out, default=str)[:2500])
