"""IDENTITY pass: probe the MetaHumanCharacter identity route in the isolated folder (no production asset is touched).
Creates /Game/Sphirus/CharacterLab/CharacterIdentity_20260930/MHC/MHC_ID_Probe, imports the current candidate face (template
import, UV-matched), reads the face landmarks + model coefficients, and tries a head-only geometry export into the isolated
folder. Writes Saved/Codex/CharacterIdentity_20260930/mhc_probe.json."""
import unreal as u, json, pathlib, traceback
P = pathlib.Path(u.Paths.project_dir()).resolve()/'Saved/Codex/CharacterIdentity_20260930'; F = '/Game/Sphirus/CharacterLab/CharacterIdentity_20260930/MHC'
S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); EAL = u.EditorAssetLibrary; out = {'steps': []}
def step(n, f):
    try: r = f(); out['steps'].append([n, 'ok', str(r)[:300]]); return r
    except Exception as e: out['steps'].append([n, 'ERR', traceback.format_exc()[-600:]]); return None
name = 'MHC_ID_Probe'; path = F+'/'+name
ch = u.load_asset(path) if EAL.does_asset_exist(path) else u.AssetToolsHelpers.get_asset_tools().create_asset(name, F, u.MetaHumanCharacter, u.MetaHumanCharacterFactoryNew())
out['created'] = ch is not None
if ch and S.try_add_object_to_edit(ch):
    try:
        face = u.load_asset('/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Body/SKM_RV_FaceMesh')
        ip = u.ImportFromTemplateParams(); ip.use_eye_meshes = True; ip.use_teeth_mesh = True; ip.match_vertices_by_u_vs = True
        ip.alignment_options = u.MetaHumanAlignmentOptions.SCALING_ROTATION_TRANSLATION
        r = step('import_from_template', lambda: S.import_from_template(ch, face, None, None, None, ip))
        lm = step('get_face_landmarks', lambda: S.get_face_landmarks(ch))
        if lm is not None: out['landmarks'] = [[v.x, v.y, v.z] for v in lm]
        co = step('get_face_model_coefficients', lambda: S.get_face_model_coefficients(ch))
        if co is not None: out['coefficients'] = [float(x) for x in co] if not isinstance(co, tuple) else str(co)[:500]
        step('commit_face_state', lambda: S.commit_face_state(ch))
        gp = u.MetaHumanGeometryExportParams(); gp.project_path = F+'/Export'; gp.head_skeletal_mesh = True; gp.body_skeletal_mesh = False; gp.full_body_skeletal_mesh = False; gp.overwrite_existing_assets = True
        step('export_geometry', lambda: u.MetaHumanCharacterExportBlueprintLibrary.export_geometry(ch, gp))
        out['export_assets'] = [str(a) for a in EAL.list_assets(F+'/Export', recursive=True)] if EAL.does_directory_exist(F+'/Export') else []
    finally:
        S.remove_object_to_edit(ch)
out['saved'] = EAL.save_loaded_asset(ch, False) if ch else False
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(P/'mhc_probe.json').write_text(json.dumps(out, indent=1)); print('MHC_PROBE', json.dumps({k: (v if k in ('steps', 'export_assets', 'dirty', 'created') else (len(v) if isinstance(v, list) else v)) for k, v in out.items()})[:3000])
