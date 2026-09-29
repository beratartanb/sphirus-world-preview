"""READ-ONLY API probe for the outfit pipeline (GeometryScript skeletal asset creation, bone weights, LOD, materials)."""
import unreal as u, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/OutfitHome_20260929'; O.mkdir(parents=True, exist_ok=True)
res = {}
def fns(cls): return [n for n in dir(cls) if not n.startswith('_') and n not in ('cast', 'static_class', 'get_class', 'get_default_object', 'call_method', 'get_editor_property', 'set_editor_property', 'set_editor_properties', 'get_fname', 'get_full_name', 'get_name', 'get_outer', 'get_outermost', 'get_package', 'get_path_name', 'get_typed_outer', 'get_world', 'is_editor_property_overridden', 'is_package_external', 'modify', 'rename', 'reset_editor_property', 'acquire_editor_element_handle')]
for name in ['GeometryScript_NewAssetUtils', 'GeometryScript_MeshBoneWeightFunctions', 'GeometryScript_PrimitiveFunctions', 'GeometryScript_AssetUtils', 'SkeletalMeshEditorSubsystem', 'MaterialEditingLibrary', 'GeometryScript_MeshTransforms', 'GeometryScript_SceneUtils', 'GeometryScript_Normals', 'GeometryScript_MeshSpatial']:
    cls = getattr(u, name, None); res[name] = fns(cls) if cls else 'MISSING'
for name in ['GeometryScriptCreateNewSkeletalMeshAssetOptions', 'GeometryScriptSimpleMeshBuffers', 'GeometryScriptCopyMeshFromAssetOptions', 'GeometryScriptTransferBoneWeightsOptions', 'GeometryScriptBoneWeight', 'GeometryScriptCopyMorphTargetToAssetOptions', 'SkeletalMeshOptimizationSettings', 'SkeletalMeshBuildSettings']:
    cls = getattr(u, name, None)
    try: res[name] = [p for p in cls.static_struct().get_editor_property('') ] if False else [n for n in dir(cls()) if not n.startswith('_') and n not in fns(u.Object)][:60] if cls else 'MISSING'
    except Exception as e: res[name] = 'ERR '+str(e)
try: res['transfer_doc'] = u.GeometryScript_MeshBoneWeightFunctions.transfer_bone_weights_from_mesh.__doc__
except Exception as e: res['transfer_doc'] = str(e)
try: res['newskel_doc'] = u.GeometryScript_NewAssetUtils.create_new_skeletal_mesh_asset_from_mesh.__doc__
except Exception as e: res['newskel_doc'] = str(e)
try: res['buffers_doc'] = u.GeometryScript_PrimitiveFunctions.append_buffers_to_mesh.__doc__
except Exception as e: res['buffers_doc'] = str(e)
try: res['regen_doc'] = u.SkeletalMeshEditorSubsystem.regenerate_lod.__doc__
except Exception as e: res['regen_doc'] = str(e)
res['skel_exists'] = u.EditorAssetLibrary.does_asset_exist('/Game/Sphirus/CharacterLab/ShoulderFix_20260928/Common/Female/Medium/NormalWeight/Body/metahuman_base_skel')
m = u.load_asset('/Game/Cargopants/Materials/M_fabric_simpler')
if m:
    try:
        res['fabric_material'] = {'scalar': [str(n) for n in u.MaterialEditingLibrary.get_scalar_parameter_names(m)], 'vector': [str(n) for n in u.MaterialEditingLibrary.get_vector_parameter_names(m)], 'texture': [str(n) for n in u.MaterialEditingLibrary.get_texture_parameter_names(m)], 'static_switch': [str(n) for n in u.MaterialEditingLibrary.get_static_switch_parameter_names(m)], 'shading': str(m.get_editor_property('shading_model')), 'two_sided': m.get_editor_property('two_sided')}
    except Exception as e: res['fabric_material'] = str(e)
bm = u.load_asset('/Game/Sphirus/CharacterLab/BodyRealism_20260929/SKM_BR_BodyMesh')
res['body_materials'] = [(str(s.get_editor_property('material_slot_name')), str(s.get_editor_property('material_interface'))) for s in bm.get_editor_property('materials')]
res['body_skeleton'] = bm.get_editor_property('skeleton').get_path_name(); res['body_physics'] = str(bm.get_editor_property('physics_asset'))
res['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(O/'api_probe.json').write_text(json.dumps(res, indent=1, default=str)); print(json.dumps({k: (v if not isinstance(v, list) else v[:80]) for k, v in res.items()}, indent=1, default=str))
