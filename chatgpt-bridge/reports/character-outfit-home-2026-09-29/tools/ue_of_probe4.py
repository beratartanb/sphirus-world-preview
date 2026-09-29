import unreal as u
for c in ['GeometryScript_MeshEdits', 'GeometryScript_MeshBasicEditFunctions']:
    cls = getattr(u, c, None); print(c, [f for f in dir(cls) if 'buffer' in f.lower() or 'append' in f.lower()] if cls else 'MISSING')
try: print(u.GeometryScript_MeshEdits.append_buffers_to_mesh.__doc__)
except Exception as e: print('ERR', e)
print('checkpoint dir sample', u.Paths.project_saved_dir())
import inspect
print([f for f in dir(u.GeometryScript_UVs) if 'set' in f.lower()][:20])
print(u.GeometryScript_UVs.set_mesh_u_vs_from_planar_projection.__doc__[:300] if hasattr(u.GeometryScript_UVs,'set_mesh_u_vs_from_planar_projection') else '')
print('newlods', u.GeometryScript_NewAssetUtils.create_new_skeletal_mesh_asset_from_mesh_lods.__doc__)
print('copyskel', u.GeometryScript_AssetUtils.copy_mesh_to_skeletal_mesh.__doc__)
print([f for f in dir(u.GeometryScriptCopyMeshToAssetOptions()) if not f.startswith('_')])
print('MaterialFactoryNew', hasattr(u, 'MaterialFactoryNew'), 'MaterialInstanceConstantFactoryNew', hasattr(u, 'MaterialInstanceConstantFactoryNew'))
print('mesh set_material?', [f for f in dir(u.SkeletalMesh) if 'material' in f.lower()])
print('SkeletalMaterial', [f for f in dir(u.SkeletalMaterial()) if not f.startswith('_')])
