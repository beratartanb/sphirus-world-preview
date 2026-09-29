"""J5b probe: SkeletalMeshLODSettings asset with explicit per-LOD reduction (LOD1 50 %, LOD2 25 %) -> assign -> regenerate."""
import unreal as u, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/OutfitHome_20260929'
DEST = '/Game/Sphirus/CharacterLab/Outfit_Home_20260929'; SUB = u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem); AT = u.AssetToolsHelpers.get_asset_tools()
rep = {}
path = DEST+'/LODS_Home_Garments'
if u.EditorAssetLibrary.does_asset_exist(path): ls = u.load_asset(path)
else:
    f = u.DataAssetFactory(); f.set_editor_property('data_asset_class', u.SkeletalMeshLODSettings); ls = AT.create_asset('LODS_Home_Garments', DEST, u.SkeletalMeshLODSettings, f)
rep['created'] = ls is not None
try:
    groups = []
    for i, pct in enumerate([1.0, 0.5, 0.25]):
        g = u.SkeletalMeshLODGroupSettings(); rs = u.SkeletalMeshOptimizationSettings()
        rs.import_text('(TerminationCriterion=SMTC_NumOfTriangles,NumOfTrianglesPercentage=%f,MaxBonesPerVertex=4,bRecalcNormals=True,WeldingThreshold=0.1,NormalsThreshold=60,bImproveTrianglesForCloth=True,BaseLOD=0)' % pct)
        g.set_editor_property('reduction_settings', rs); g.set_editor_property('screen_size', u.PerPlatformFloat(1.0 if i == 0 else (0.45 if i == 1 else 0.22)))
        groups.append(g)
    ls.set_editor_property('lod_groups', groups); rep['groups_set'] = True
except Exception as e: rep['groups_set'] = 'ERR '+str(e)[:300]
rep['group_fields'] = [n for n in dir(u.SkeletalMeshLODGroupSettings()) if not n.startswith('_')][:30]
u.EditorAssetLibrary.save_loaded_asset(ls, False)
def lod_counts(mesh):
    out = []
    for i in range(SUB.get_lod_count(mesh)):
        dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.RENDER_DATA; lod.lod_index = i
        r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(mesh, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); out.append((i, dm.get_vertex_count(), dm.get_triangle_count()))
    return out
m = u.load_asset(DEST+'/SKM_Home_Henley')
try:
    m.set_editor_property('lod_settings', ls); ok = SUB.regenerate_lod(m, 3, True, False); rep['henley'] = {'regen': ok, 'lods': lod_counts(m)}
except Exception as e: rep['henley'] = 'ERR '+str(e)[:300]
u.EditorAssetLibrary.save_loaded_asset(m, False)
(O/'j5b_lodsettings.json').write_text(json.dumps(rep, indent=1, default=str)); print(json.dumps(rep, default=str))
