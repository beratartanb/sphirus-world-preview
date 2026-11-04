"""probe2_pfr.py (measure job, read-only): landscape target-layer / material-graph capabilities needed to adopt the Pine Forest Pack
landscape material, plus asset-creation API availability. Writes Saved/Codex/PineForestRedesign_20261104/recon/probe2.json."""
import unreal as u, json, pathlib, time

D = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/PineForestRedesign_20261104/recon'; D.mkdir(parents=True, exist_ok=True)
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None
A = u.get_editor_subsystem(u.EditorActorSubsystem); actors = A.get_all_level_actors()
land = next(a for a in actors if isinstance(a, u.Landscape))
out = {'started': time.strftime('%H:%M:%S')}
out['land_methods'] = sorted(n for n in dir(land) if 'layer' in n.lower() or 'weight' in n.lower() or 'material' in n.lower() or 'target' in n.lower() or 'import' in n.lower() or 'export' in n.lower())
out['unreal_landscape_names'] = sorted(n for n in dir(u) if 'landscape' in n.lower())
for prop in ('target_layers', 'editor_layer_settings', 'landscape_layers', 'TargetLayers', 'layer_info_objs', 'editor_cached_layer_infos'):
    try:
        v = land.get_editor_property(prop); out['prop_' + prop] = str(v)[:600]
    except Exception as ex:
        out['prop_' + prop] = 'NO ' + repr(ex)[:120]
try:
    info = land.get_landscape_info() if hasattr(land, 'get_landscape_info') else None; out['landscape_info'] = str(info)[:200]
except Exception as ex:
    out['landscape_info'] = 'NO ' + repr(ex)[:120]
# landscape editor subsystem?
for nm in ('LandscapeEditorSubsystem', 'LandscapeSubsystem', 'LandscapeEditorObject', 'LandscapeInfo', 'LandscapeLayerInfoObject', 'LandscapeGrassType', 'MaterialExpressionLandscapeLayerBlend', 'MaterialExpressionLandscapeGrassOutput', 'FoliageType_InstancedStaticMesh', 'FoliageType_InstancedStaticMeshFactory', 'InstancedFoliageActor', 'RuntimeVirtualTextureVolume', 'LandscapeTargetLayerSettings'):
    out['has_' + nm] = hasattr(u, nm)
try:
    sub = u.get_editor_subsystem(u.LandscapeEditorSubsystem) if hasattr(u, 'LandscapeEditorSubsystem') else None
    out['landscape_editor_subsystem_methods'] = sorted(n for n in dir(sub) if not n.startswith('_'))[:80] if sub else None
except Exception as ex:
    out['landscape_editor_subsystem_methods'] = 'NO ' + repr(ex)[:120]
try:
    out['layer_info_methods'] = sorted(n for n in dir(u.LandscapeLayerInfoObject) if not n.startswith('_'))[:60]
except Exception as ex:
    out['layer_info_methods'] = repr(ex)[:100]

# ---- material graph walk (from the output pins): expression classes, layer names, texture params, grass output
ML = u.MaterialEditingLibrary


def walk(mat, max_nodes=400):
    seen = {}; order = []; stack = []
    for prop in (u.MaterialProperty.MP_BASE_COLOR, u.MaterialProperty.MP_NORMAL, u.MaterialProperty.MP_ROUGHNESS, u.MaterialProperty.MP_SPECULAR, u.MaterialProperty.MP_WORLD_POSITION_OFFSET, u.MaterialProperty.MP_AMBIENT_OCCLUSION):
        try:
            n = ML.get_material_property_input_node(mat, prop)
            if n: stack.append(n)
        except Exception:
            pass
    while stack and len(seen) < max_nodes:
        n = stack.pop(); k = n.get_name()
        if k in seen: continue
        d = {'cls': n.get_class().get_name()}
        for p in ('parameter_name', 'layers', 'texture', 'desc', 'layer_name', 'grass_types', 'function', 'default_value', 'material_function', 'virtual_texture', 'material_layers'):
            try:
                v = n.get_editor_property(p)
                if p == 'layers':
                    d[p] = [{'name': str(l.get_editor_property('layer_name')), 'blend': str(l.get_editor_property('blend_type')), 'preview_w': l.get_editor_property('preview_weight')} for l in v]
                elif p == 'grass_types':
                    d[p] = [{'name': str(g.get_editor_property('name')), 'grass_type': (g.get_editor_property('grass_type').get_path_name() if g.get_editor_property('grass_type') else None)} for g in v]
                elif hasattr(v, 'get_path_name'):
                    d[p] = v.get_path_name()
                elif v is not None:
                    d[p] = str(v)[:120]
            except Exception:
                pass
        seen[k] = d; order.append(k)
        try:
            for inp in ML.get_inputs_for_material_expression(mat, n):
                if inp: stack.append(inp)
        except Exception as ex:
            d['inputs_err'] = repr(ex)[:80]
    return [dict(seen[k], id=k) for k in order]


res = {}
for p in ('/Game/GraceRanger/Environment/Exterior20260921/Materials/M_EX_Integration_Floor', '/Game/PineForestPack/Materials/Landscape/Masters/M_Landscape_PineForest'):
    m = u.load_asset(p)
    try:
        nodes = walk(m)
        res[p.split('/')[-1]] = {'n': len(nodes), 'classes': sorted(set(n['cls'] for n in nodes)),
                                 'layer_blends': [n for n in nodes if 'LayerBlend' in n['cls'] or 'LayerSwitch' in n['cls'] or 'LayerSample' in n['cls'] or 'LayerWeight' in n['cls']],
                                 'grass': [n for n in nodes if 'Grass' in n['cls']], 'rvt': [n for n in nodes if 'VirtualTexture' in n['cls']],
                                 'tex_params': sorted(set(n.get('parameter_name', '') for n in nodes if n['cls'].startswith('MaterialExpressionTextureSampleParameter'))),
                                 'functions': sorted(set(n.get('material_function', '') for n in nodes if n['cls'] == 'MaterialExpressionMaterialFunctionCall'))}
    except Exception as ex:
        res[p.split('/')[-1]] = 'ERR ' + repr(ex)[:300]
    # expressions property attempts
    for prop in ('expressions', 'expression_collection', 'editor_only_data'):
        try:
            v = m.get_editor_property(prop); res[p.split('/')[-1] + '_' + prop] = str(v)[:200]
        except Exception as ex:
            res[p.split('/')[-1] + '_' + prop] = 'NO'
out['materials'] = res
# grass types used by the current material (via the MI static parameters?) - the walk above answers it for the master
# FT creation API
try:
    tools = u.AssetToolsHelpers.get_asset_tools(); out['asset_tools'] = [n for n in dir(tools) if 'create' in n or 'duplicate' in n]
except Exception as ex:
    out['asset_tools'] = repr(ex)[:100]
# existing FT_EX_PineTree01 settings (template for new types)
ft = u.load_asset('/Game/GraceRanger/Environment/Exterior20260921/Foliage/FT_EX_PineTree01')
if ft:
    d = {}
    for k in ('mesh', 'density', 'radius', 'cull_distance', 'scale_x', 'scale_y', 'scale_z', 'scaling', 'align_to_normal', 'random_yaw', 'collision_with_world', 'enable_density_scaling', 'enable_cull_distance_scaling', 'body_instance', 'cast_shadow', 'affect_distance_field_lighting', 'mobility', 'ground_slope_angle', 'z_offset', 'random_pitch_angle', 'enable_static_lighting', 'cast_dynamic_shadow', 'world_position_offset_disable_distance', 'override_materials', 'is_selected', 'enable_discard_on_load', 'cull_distance', 'translucent_sort_priority'):
        try:
            v = ft.get_editor_property(k); d[k] = v.get_path_name() if hasattr(v, 'get_path_name') else str(v)[:120]
        except Exception as ex:
            d[k] = 'n/a'
    out['ft_template'] = d
    try:
        bi = ft.get_editor_property('body_instance'); out['ft_collision_profile'] = str(bi.get_editor_property('collision_profile_name'))
    except Exception as ex:
        out['ft_collision_profile'] = 'n/a ' + repr(ex)[:80]
# a few PFP meshes: collision + nanite + materials (for the palette)
reg = u.AssetRegistryHelpers.get_asset_registry(); lib = {}
for n in ('Trees/SM_PineTree02', 'Trees/SM_PineTree04', 'Trees/SM_PineTree06', 'Trees/SM_PineTree07', 'Trees/SM_PineTreeLow01', 'Trees/SM_PineTreeLowMed01', 'Trees/SM_Pine_Med_Xtree_01', 'Trees/SM_SonoSapling03', 'Trees/SM_SonoTree01',
          'Plants/SM_MossLeaf_01', 'Plants/SM_MossClump01', 'Plants/SM_WeedA_01', 'GroundCover/SM_GroundCover02', 'DeadLeaves/SM_DeadPineNeedle01', 'DeadLeaves/SM_DeadLeaves03', 'DeadLeaves/SM_DeadLeaves04', 'DeadLeaves/SM_FallenBranches01', 'DeadLeaves/SM_PineAcorn01',
          'TerrainPatches/SM_PineGroundPatch01', 'TerrainPatches/SM_RockyGround01', 'TerrainPatches/SM_ForestTrailPatches01', 'TerrainPatches/SM_TrunkPile01', 'TerrainPatches/SM_PineDeadTrunk04', 'Plants/SM_Mushroom01', 'Plants/SM_MushroomHanging01', 'Plants/SM_IvyBed01', 'Plants/SM_Bush_SalixElag02', 'Plants/SM_BushB02', 'Plants/SM_Bush01',
          'Cliffs/SM_PineGroundRock02', 'Cliffs/SM_PineGroundRock04', 'Cliffs/SM_PineGroundRock06', 'Rocks/SM_PineStone02', 'Water/SM_WaterPlane'):
    p = '/Game/PineForestPack/Meshes/' + n; m = u.load_asset(p)
    if not m:
        # search by name anywhere under the pack
        hits = [str(a.package_name) for a in reg.get_assets_by_path('/Game/PineForestPack/Meshes', True) if str(a.asset_name) == n.split('/')[-1]]
        lib[n] = {'missing_at': p, 'found': hits}; continue
    b = m.get_bounds(); bs = m.get_editor_property('body_setup'); ne = m.get_editor_property('nanite_settings')
    lib[n] = {'ext': [round(b.box_extent.x), round(b.box_extent.y), round(b.box_extent.z)], 'org': [round(b.origin.x), round(b.origin.y), round(b.origin.z)], 'nanite': bool(ne.get_editor_property('enabled')) if ne else None,
              'lods': m.get_num_lods(), 'mats': [ (sm.material_interface.get_path_name().split('.')[0] if sm.material_interface else None) for sm in m.get_editor_property('static_materials')],
              'col': (str(bs.get_editor_property('collision_trace_flag')).split('.')[-1][:12] if bs else None)}
out['pfp_lib'] = lib
out['finished'] = time.strftime('%H:%M:%S')
(D / 'probe2.json').write_text(json.dumps(out, indent=1, default=str))
print('PROBE2', json.dumps({k: out[k] for k in ('land_methods', 'prop_target_layers', 'has_LandscapeEditorSubsystem', 'landscape_editor_subsystem_methods')}, default=str)[:1500])
