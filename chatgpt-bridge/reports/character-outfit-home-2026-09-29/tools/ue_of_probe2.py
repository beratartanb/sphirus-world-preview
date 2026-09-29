import unreal as u, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/OutfitHome_20260929'
names = [n for n in dir(u) if any(w in n for w in ('BoneWeight', 'SkinWeight', 'Primitive', 'GeometryScriptSimple', 'MeshBuffers', 'TextureFactory', 'ImportTask', 'SkeletalMeshReduction', 'ReductionSettings', 'LODInfo', 'SkeletalMeshLOD'))]
res = {'names': names}
for n in names:
    cls = getattr(u, n)
    try: res[n] = [f for f in dir(cls) if not f.startswith('_')][:80]
    except Exception as e: res[n] = str(e)
(O/'api_probe2.json').write_text(json.dumps(res, indent=1)); print(json.dumps(names))
for n in ['GeometryScript_MeshBoneWeightFunctions', 'GeometryScript_BoneWeights', 'GeometryScript_PrimitiveFunctions', 'GeometryScript_MeshPrimitiveFunctions']:
    print(n, hasattr(u, n))
