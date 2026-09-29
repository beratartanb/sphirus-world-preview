import unreal as u, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/OutfitHome_20260929'
res = {}
for n in ['GeometryScript_BoneWeights', 'GeometryScript_Primitives']:
    res[n] = [f for f in dir(getattr(u, n)) if not f.startswith('_')]
for fn in ['GeometryScript_BoneWeights.transfer_bone_weights_from_mesh', 'GeometryScript_BoneWeights.copy_bones_from_mesh', 'GeometryScript_BoneWeights.set_vertex_bone_weights', 'GeometryScript_BoneWeights.get_vertex_bone_weights', 'GeometryScript_BoneWeights.get_all_bones_info', 'GeometryScript_BoneWeights.mesh_create_bone_weights', 'GeometryScript_Primitives.append_buffers_to_mesh', 'GeometryScript_BoneWeights.smooth_bone_weights', 'GeometryScript_BoneWeights.prune_bone_weights', 'GeometryScript_BoneWeights.get_bones_info']:
    c, f = fn.split('.')
    try: res['doc:'+fn] = getattr(getattr(u, c), f).__doc__
    except Exception as e: res['doc:'+fn] = 'ERR '+str(e)
res['SkeletalMeshLODInfo'] = [f for f in dir(u.SkeletalMeshLODInfo()) if not f.startswith('_')]
res['SkeletalMeshOptimizationSettings_props'] = [p for p in dir(u.SkeletalMeshOptimizationSettings()) if not p.startswith('_')]
try:
    s = u.SkeletalMeshOptimizationSettings(); res['opt_export'] = s.export_text()
except Exception as e: res['opt_export'] = str(e)
res['SkeletalMesh_fns'] = [f for f in dir(u.SkeletalMesh) if 'lod' in f.lower() or 'material' in f.lower() or 'post' in f.lower() or 'morph' in f.lower()]
try: res['lod_info_doc'] = u.SkeletalMesh.get_lod_info.__doc__
except Exception as e: res['lod_info_doc'] = str(e)
res['AssetImportTask'] = [f for f in dir(u.AssetImportTask()) if not f.startswith('_')][:40]
res['TextureFactory'] = [f for f in dir(u.TextureFactory) if not f.startswith('_')][:40]
res['EditorSkeletalMeshLibrary'] = [f for f in dir(u.EditorSkeletalMeshLibrary) if not f.startswith('_')] if hasattr(u, 'EditorSkeletalMeshLibrary') else 'MISSING'
(O/'api_probe3.json').write_text(json.dumps(res, indent=1)); print(json.dumps(res, indent=1)[:12000])
