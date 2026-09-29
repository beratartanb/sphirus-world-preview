import unreal as u, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/BodyRealismArtist_20260929'; O.mkdir(parents=True, exist_ok=True)
res = {}
q = u.GeometryScript_MeshQueries
m = u.load_asset('/Game/Sphirus/CharacterLab/BodyRealism_20260929/SKM_BR_BodyMesh')
dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); res['copy'] = str(r)
res['q'] = [n for n in dir(q) if 'uv' in n.lower() or 'material' in n.lower() or 'group' in n.lower()]
res['uvfns'] = [n for n in dir(u.GeometryScript_UVs) if not n.startswith('_')]
res['num_uv'] = str(q.get_num_uv_sets(dm))
res['animpose'] = [n for n in dir(u.AnimPoseExtensions) if not n.startswith('_')]
sk = m.get_editor_property('skeleton'); res['skeleton'] = sk.get_path_name()
res['skel_fns'] = [n for n in dir(sk) if 'bone' in n.lower() or 'ref' in n.lower()]
res['mesh_fns'] = [n for n in dir(m) if 'bone' in n.lower() or 'ref' in n.lower()]
res['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(O/'probe.json').write_text(json.dumps(res, indent=1)); print(json.dumps(res, indent=1))
