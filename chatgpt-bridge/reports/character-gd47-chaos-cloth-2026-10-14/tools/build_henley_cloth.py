"""GD47: WHOLE-garment runtime Chaos Cloth Henley from the in-game GD46 re-settled mesh (no cut piece). Pattern = ue_cr_cloth_build.py, isolated in
/Game/Sphirus/CharacterLab/GD47_ChaosCloth_20261014 ({Cloth, Materials}). builtins.GD47 = {'tag', 'weights' (json from tools/gd47_weights.py),
'high', 'damping', 'pa_infl' {bone: +cm}, 'pa_drop' [bones], 'props' {node: {prop: text}}}.
1. SKM_GD46_Henley_f5 LOD0 -> DynamicMesh (same order as data/henley_f5_mesh.json.gz) -> MaxDistance weight layer (offline field) -> weld the
   coincident panel seams (front/back/sleeves are separate pieces in the pattern mesh; unwelded they would fall apart in the sim)
2. clothing-enabled MI copies of the g17e MIs (parents = the corrective clothing-enabled textile masters M_CR_Textile(_B))
3. collider PHYS_GD47_HenleyCollider_<tag> = copy of PHYS_CR_HenleyCollider (+ optional capsule inflation / removal)
4. Dataflow Import -> TransferSkinWeights(f5) -> Proxy -> MaxDist -> Backstop -> Tethers -> Damping -> Collision -> SetPA -> terminal
5. section materials set per slot afterwards (matfix) and read back. Writes data/cloth_henley_<tag>.json"""
import unreal as u, json, pathlib, builtins, re
C = builtins.GD47; EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; L = u.DataflowEditorBlueprintLibrary; q = u.GeometryScript_MeshQueries; lst = u.GeometryScript_List
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD47_ChaosCloth_20261014/data'
G = '/Game/Sphirus/CharacterLab/GD47_ChaosCloth_20261014'; F = G+'/Cloth'; MD = G+'/Materials'; TAG = C['tag']; NAME = 'Henley_' + TAG; out = {'cfg': {k: v for k, v in C.items() if k != 'weights'}, 'weights_file': C['weights']}
SKM = '/Game/Sphirus/CharacterLab/GD46_GarmentFit_20261013/Outfit/SKM_GD46_Henley_f5'; CRM = '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Outfit/Materials'
def pick(r, typ):
    r = r if isinstance(r, tuple) else (r,); return [x for x in r if isinstance(x, typ)][0]
Wd = json.load(open(C['weights'])); W = Wd['W']; out['weights_rep'] = Wd['rep']
skm = u.load_asset(SKM); dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(skm, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); assert 'SUCCESS' in str(r[-1]), r
P = lst.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); assert len(P) == len(W), (len(P), len(W)); out['verts_before_weld'] = len(P)
h = pick(u.GeometryScript_WeightMaps.find_or_add_mesh_weight_map(dm, 'MaxDistance'), u.GeometryScriptWeightMapHandle)
u.GeometryScript_WeightMaps.set_mesh_weight_map_values(dm, pick(lst.convert_array_to_scalar_list(W), u.GeometryScriptScalarList), h, False)
wo = u.GeometryScriptWeldEdgesOptions(); wo.set_editor_property('tolerance', 0.01); wo.set_editor_property('only_unique_pairs', True)
u.GeometryScript_MeshRepair.weld_mesh_edges(dm, wo); u.GeometryScript_MeshRepair.compact_mesh(dm)
P2 = lst.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); out['verts_after_weld'] = len(P2)
if C.get('push'):   # hem rest shape pushed outward along the normal (kinematic / backstop target over the shorts waistband)
    PU = C['push']; Nv = lst.convert_vector_list_to_array(pick(u.GeometryScript_Normals.get_mesh_per_vertex_normals(dm), u.GeometryScriptVectorList)); npu = 0
    for i, (p_, n_) in enumerate(zip(P2, Nv)):
        t_ = max(0.0, min(1.0, (PU['z0'] - p_.z) / (PU['z0'] - PU['z1'])))
        if t_ > 0 and abs(p_.x) < 22: o_ = PU['cm'] * t_ * t_ * (3 - 2 * t_); u.GeometryScript_MeshEdits.set_vertex_position(dm, i, u.Vector(p_.x + n_.x*o_, p_.y + n_.y*o_, p_.z + n_.z*o_), True); npu += 1
    out['push_verts'] = npu
h = pick(u.GeometryScript_WeightMaps.find_or_add_mesh_weight_map(dm, 'MaxDistance'), u.GeometryScriptWeightMapHandle)
W2 = lst.convert_scalar_list_to_array(pick(u.GeometryScript_WeightMaps.get_mesh_weight_map_values(dm, h, False), u.GeometryScriptScalarList))
out['weights_after_weld'] = {'n': len(W2), 'max': max(W2), 'pinned': sum(1 for w in W2 if w <= 0.0), 'mean': sum(W2)/len(W2)}
# ---- clothing-enabled MI copies
mats = []
for sm in skm.get_editor_property('materials'):
    mi = sm.get_editor_property('material_interface'); dst = MD+'/'+mi.get_name()+'_cloth'
    if not EAL.does_asset_exist(dst): assert EAL.duplicate_asset(mi.get_path_name().split('.')[0], dst)
    c = u.load_asset(dst); par = mi.get_editor_property('parent').get_name()
    ME.set_material_instance_parent(c, u.load_asset(CRM+'/'+('M_CR_Textile_B' if par.endswith('_B') else 'M_CR_Textile'))); ME.update_material_instance(c); EAL.save_loaded_asset(c, False)
    mats.append((c, sm.get_editor_property('material_slot_name')))
out['materials'] = [(m.get_name(), m.get_editor_property('parent').get_name(), str(s)) for m, s in mats]
# ---- collider
pap = F+'/PHYS_GD47_HenleyCollider_'+TAG
if EAL.does_asset_exist(pap): EAL.delete_asset(pap)
assert EAL.duplicate_asset('/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Cloth/PHYS_CR_HenleyCollider', pap); pa = u.load_asset(pap); rep = {}
for b in u.ObjectIterator(u.BodySetup):
    if b.get_outer() != pa: continue
    bn = str(b.get_editor_property('bone_name')); dx = C.get('pa_infl', {}).get(bn)
    if dx is not None:
        t = b.get_editor_property('agg_geom').export_text(); t2 = re.sub(r'Radius=([0-9.]+)', lambda m: 'Radius=%.6f' % max(0.5, float(m.group(1))+dx), t)
        g2 = u.KAggregateGeom(); assert g2.import_text(t2); b.modify(); b.set_editor_property('agg_geom', g2)
        rep[bn] = [round(s.get_editor_property('radius'), 2) for s in b.get_editor_property('agg_geom').get_editor_property('sphyl_elems')]
pa.modify(); out['pa'] = {'path': pap, 'saved': EAL.save_loaded_asset(pa, False), 'changed': rep}
# ---- static mesh carrying the weight layer
smp = F+f'/SM_GD47_{NAME}_Sim'
if EAL.does_asset_exist(smp): EAL.delete_asset(smp)
o = u.GeometryScriptCreateNewStaticMeshAssetOptions(); o.set_editor_property('enable_recompute_normals', False); o.set_editor_property('enable_recompute_tangents', True); o.set_editor_property('enable_collision', False); o.set_editor_property('use_original_vertex_order', True)
r = u.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(dm, smp, o); sm_ = r[0] if isinstance(r, tuple) else r; assert sm_, r
sms = []
for m, slot in mats: s = u.StaticMaterial(); s.set_editor_property('material_interface', m); s.set_editor_property('material_slot_name', slot); sms.append(s)
sm_.set_editor_property('static_materials', sms); EAL.save_loaded_asset(sm_, False)
# ---- dataflow + cloth asset
cap, dfp = F+f'/CA_GD47_{NAME}', F+f'/DF_GD47_{NAME}'
for src, dst in (('/ChaosClothAsset/CA_Template', cap), ('/ChaosClothAsset/DF_EmptyClothAssetTemplate', dfp)):
    if EAL.does_asset_exist(dst): EAL.delete_asset(dst)
    assert EAL.duplicate_asset(src, dst)
ca = u.load_asset(cap); df = u.load_asset(dfp); di = ca.get_editor_property('dataflow_instance'); di.set_editor_property('dataflow_asset', df); ca.set_editor_property('dataflow_instance', di)
chain = [('FChaosClothAssetStaticMeshImportNode_v2', 'Import', {'StaticMesh': f"/Script/Engine.StaticMesh'{smp}.{smp.split('/')[-1]}'", 'bImportSimMesh': 'True', 'bImportRenderMesh': 'True', 'UVChannel': '0', 'SimMeshSection': '0'}),
         ('FChaosClothAssetTransferSkinWeightsNode', 'Skin', {'SkeletalMesh': f"/Script/Engine.SkeletalMesh'{SKM}.{SKM.split('/')[-1]}'", 'TargetMeshType': 'All'}),
         ('FChaosClothAssetProxyDeformerNode_v3', 'Proxy', {}),
         ('FChaosClothAssetSimulationMaxDistanceConfigNode', 'MaxDist', {'MaxDistance': f'(bIsAnimatable=True,Low=0.000000,High={C["high"]:.6f},WeightMap="MaxDistance")'}),
         ('FChaosClothAssetSimulationBackstopConfigNode', 'Backstop', {'BackstopDistance': f'(bIsAnimatable=True,Low={C.get("bs_dist", 0.0):.6f},High={C.get("bs_dist", 0.0):.6f},WeightMap="BackstopDistance")',
                                                                     'BackstopRadius': f'(bIsAnimatable=True,Low={C.get("bs_rad", 40.0):.6f},High={C.get("bs_rad", 40.0):.6f},WeightMap="BackstopRadius")'}),
         ('FChaosClothAssetSimulationLongRangeAttachmentConfigNode_v2', 'Tethers', {}),
         ('FChaosClothAssetSimulationDampingConfigNode', 'Damping', {'DampingCoefficientWeighted': f'(bIsAnimatable=True,Low={C.get("damping", 0.1):.6f},High={C.get("damping", 0.1):.6f},WeightMap="DampingCoefficient")'}),
         ('FChaosClothAssetSimulationCollisionConfigNode', 'Collision', {}),
         ('FChaosClothAssetSetPhysicsAssetNode', 'SetPA', {'PhysicsAsset': f"/Script/Engine.PhysicsAsset'{pap}.{pap.split('/')[-1]}'"})]
names, props, conns = [], {}, []
for i, (typ, base, pr) in enumerate(chain):
    n = str(L.add_dataflow_node(df, typ, base, u.Vector2D(-1600+i*250, 0))); names.append(n)
    for k, v in {**pr, **C.get('props', {}).get(base, {})}.items(): props[f'{base}.{k}'] = L.set_dataflow_node_property(df, n, k, v)
for a_, b_ in zip(names[:-1], names[1:]): conns.append(L.connect_dataflow_nodes(df, a_, 'Collection', b_, 'Collection'))
conns.append(L.connect_dataflow_nodes(df, names[-1], 'Collection', 'ClothAssetTerminal', 'CollectionLods[0]'))
out['nodes'] = names; out['props'] = props; out['connections'] = conns
out['regen'] = u.DataflowBlueprintLibrary.regenerate_asset_from_dataflow(ca, False)
# ---- section materials (the build assigns the first MI to every render section)
before = [m.get_editor_property('material_interface').get_name() if m.get_editor_property('material_interface') else None for m in ca.get_editor_property('materials')]
new = []
for m, slot in mats: s = u.SkeletalMaterial(); s.set_editor_property('material_interface', m); s.set_editor_property('material_slot_name', slot); new.append(s)
ca.set_editor_property('materials', new)
for x in (df, ca): out.setdefault('saved', []).append(EAL.save_loaded_asset(x, False))
out['ca_materials'] = {'before': before, 'after': [m.get_editor_property('material_interface').get_name() for m in u.load_asset(cap).get_editor_property('materials')]}
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(O/f'cloth_henley_{TAG}.json').write_text(json.dumps(out, indent=1, default=str)); print('GD47_BUILD', json.dumps(out, default=str)[:1500], flush=True)
