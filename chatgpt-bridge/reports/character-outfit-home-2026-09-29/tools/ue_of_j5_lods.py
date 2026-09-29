"""J5: generate LOD1/LOD2 for the garment meshes with the engine skeletal reduction (LOD1 ~50 %, LOD2 ~25 % of LOD0
triangles), read back per-LOD triangle/vertex counts, save. Reduction settings are written through the LODInfo struct of
the mesh if exposed; otherwise engine defaults (50 % per step) are used and reported."""
import unreal as u, pathlib, json
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/OutfitHome_20260929'
DEST = '/Game/Sphirus/CharacterLab/Outfit_Home_20260929'; SUB = u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem)
q = u.GeometryScript_MeshQueries
def lod_counts(mesh):
    out = []
    for i in range(SUB.get_lod_count(mesh)):
        dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.RENDER_DATA; lod.lod_index = i
        r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(mesh, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod)
        out.append({'lod': i, 'verts': dm.get_vertex_count(), 'tris': dm.get_triangle_count()} if 'SUCCESS' in str(r[-1]) else {'lod': i, 'err': str(r[-1])})
    return out
rep = {}
for name in ['SKM_Home_Henley', 'SKM_Home_Trousers']:
    m = u.load_asset(DEST+'/'+name); before = lod_counts(m)
    # try to set per-LOD reduction percentages through lod_info (may be protected; reported either way)
    applied = None
    try:
        infos = m.get_editor_property('lod_info'); applied = 'lod_info readable: %d entries' % len(infos)
    except Exception as e: applied = 'lod_info not exposed: '+str(e)[:80]
    ok = SUB.regenerate_lod(m, 3, False, False)   # keep imported LOD0/LOD1 (Blender 50 % decimate), generate LOD2 only
    after = lod_counts(m)
    saved = u.EditorAssetLibrary.save_loaded_asset(m, False)
    rep[name] = {'regenerate': ok, 'before': before, 'after': after, 'settings_note': applied, 'saved': saved}
    print(name, json.dumps(rep[name]), flush=True)
rep['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(O/'j5_lods.json').write_text(json.dumps(rep, indent=1)); print(json.dumps(rep))
