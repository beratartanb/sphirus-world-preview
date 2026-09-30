"""IDENTITY pass: fit a MetaHumanCharacter face state to target vertices (DNA-order head skin 24049 + eyes 770/770 + teeth 4246,
UE cm, from a .npz written by Blender) and export the head geometry into the isolated folder.
builtins.ID_FIT = {'npz_json': <abs path of json {head, eyeL, eyeR, teeth}>, 'name': 'MHC_ID_x', 'export': 'SKM_x', 'adapt_neck': True,
                   'hf': False (disable_high_frequency_delta), 'align': 'SCALING_ROTATION_TRANSLATION' | 'NONE', 'landmarks_json': optional {indices, deltas}}
Writes Saved/Codex/CharacterIdentity_20260930/fit_<name>.json"""
import unreal as u, json, pathlib, builtins, traceback
CFG = builtins.ID_FIT; P = pathlib.Path(u.Paths.project_dir()).resolve()/'Saved/Codex/CharacterIdentity_20260930'; F = '/Game/Sphirus/CharacterLab/CharacterIdentity_20260930/MHC'
S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); EAL = u.EditorAssetLibrary; out = {'cfg': {k: v for k, v in CFG.items()}, 'steps': []}
def step(n, f):
    try: r = f(); out['steps'].append([n, 'ok', str(r)[:200]]); return r
    except Exception: out['steps'].append([n, 'ERR', traceback.format_exc()[-700:]]); return None
name = CFG['name']; path = F+'/'+name
ch = u.load_asset(path) if EAL.does_asset_exist(path) else u.AssetToolsHelpers.get_asset_tools().create_asset(name, F, u.MetaHumanCharacter, u.MetaHumanCharacterFactoryNew())
if S.try_add_object_to_edit(ch):
    try:
        face = u.load_asset('/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Body/SKM_RV_FaceMesh')
        ip = u.ImportFromTemplateParams(); ip.use_eye_meshes = True; ip.use_teeth_mesh = True; ip.match_vertices_by_u_vs = True
        ip.alignment_options = u.MetaHumanAlignmentOptions.SCALING_ROTATION_TRANSLATION
        step('import_from_template', lambda: S.import_from_template(ch, face, None, None, None, ip))   # start from the current identity
        if CFG.get('npz_json'):
            T = json.load(open(CFG['npz_json'])); V = lambda arr: [u.Vector(*p) for p in arr]
            fo = u.FitToTargetOptions(); fo.alignment_options = getattr(u.MetaHumanAlignmentOptions, CFG.get('align', 'SCALING_ROTATION_TRANSLATION'))
            fo.adapt_neck = CFG.get('adapt_neck', True); fo.disable_high_frequency_delta = CFG.get('hf', False)
            fp = u.MetaHumanCharacterFitToVerticesParams(); fp.options = fo; fp.head_vertices = V(T['head'])
            if T.get('eyeL'): fp.left_eye_vertices = V(T['eyeL']); fp.right_eye_vertices = V(T['eyeR'])
            if T.get('teeth'): fp.teeth_vertices = V(T['teeth'])
            step('fit_state_to_target_vertices', lambda: S.fit_state_to_target_vertices(ch, fp))
        if CFG.get('landmarks_json'):
            L = json.load(open(CFG['landmarks_json']))
            step('translate_face_landmarks', lambda: S.translate_face_landmarks(ch, L['indices'], [u.Vector(*d) for d in L['deltas']]))
        lm = step('get_face_landmarks', lambda: S.get_face_landmarks(ch))
        if lm is not None: out['landmarks'] = [[v.x, v.y, v.z] for v in lm]
        step('commit_face_state', lambda: S.commit_face_state(ch))
        gp = u.MetaHumanGeometryExportParams(); gp.project_path = F+'/Export'; gp.head_skeletal_mesh = True; gp.body_skeletal_mesh = False; gp.full_body_skeletal_mesh = False; gp.overwrite_existing_assets = True
        step('export_geometry', lambda: u.MetaHumanCharacterExportBlueprintLibrary.export_geometry(ch, gp))
    finally:
        S.remove_object_to_edit(ch)
EAL.save_loaded_asset(ch, False)
exp = F+f'/Export/{name}_Head'; out['export'] = exp if EAL.does_asset_exist(exp) else None
if out['export']: EAL.save_asset(exp, False)
# read back export LOD positions (UE render-vertex order, identical to SKM_RV_FaceMesh) -> json for Blender
sme = u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem); q = u.GeometryScript_MeshQueries; res = {}
if out['export']:
    m = u.load_asset(exp)
    for L in range(sme.get_lod_count(m)):
        dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = L
        u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod)
        res[L] = [[round(p.x, 5), round(p.y, 5), round(p.z, 5)] for p in u.GeometryScript_List.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1])]
    (P/f'export_{name}.json').write_text(json.dumps(res))
out['export_lod_verts'] = {k: len(v) for k, v in res.items()}
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(P/f'fit_{name}.json').write_text(json.dumps(out, indent=1)); print('ID_FIT', json.dumps({k: v for k, v in out.items() if k != 'landmarks'})[:2500])
