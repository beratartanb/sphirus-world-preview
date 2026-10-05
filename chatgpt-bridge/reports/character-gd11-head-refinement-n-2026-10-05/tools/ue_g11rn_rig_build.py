"""GUARDIAN-4: new neutral -> MetaHuman AUTO-RIG (Epic service) -> new DNA face.
builtins.GD3_RIG = {'name': 'MHC_GD3_N1', 'coefs': <json with 'coefs'>, 'head_scale': float|None, 'rig_type': 'JOINTS_AND_BLEND_SHAPES',
                    'target_json': optional dense target {head, eyeL, eyeR, teeth} (model space) fitted with fit_state_to_target_vertices after the coefs,
                    'export': True}
Creates the isolated MetaHumanCharacter in CharacterGuardian3/MHC, requests auto-rigging (blocking), exports head DNA (project + .dna on disk) and the
rigged head geometry (skeletal mesh) to CharacterGuardian3/MHC/Export, reads joint positions of the rigged face (component space) and writes
Saved/Codex/GD11_HeadRefinementN_20261005/rig_<name>.json"""
import unreal as u, json, builtins, pathlib, time, traceback
C = builtins.GD3_RIG; P = pathlib.Path(u.Paths.project_dir()).resolve()/'Saved/Codex/GD11_HeadRefinementN_20261005'; F = '/Game/Sphirus/CharacterLab/GD11_HeadRefinementN_20261005/MHC'
S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); EAL = u.EditorAssetLibrary; out = {'cfg': {k: str(v) for k, v in C.items()}, 'steps': []}
def step(n, f):
    t = time.time()
    try: r = f(); out['steps'].append([n, 'ok', round(time.time()-t, 2), str(r)[:200]]); return r
    except Exception: out['steps'].append([n, 'ERR', traceback.format_exc()[-800:]]); return None
name = C['name']; path = F+'/'+name
ch = u.load_asset(path) if EAL.does_asset_exist(path) else u.AssetToolsHelpers.get_asset_tools().create_asset(name, F, u.MetaHumanCharacter, u.MetaHumanCharacterFactoryNew())
JN = ['FACIAL_L_Eye', 'FACIAL_R_Eye', 'FACIAL_C_FacialRoot', 'FACIAL_C_Jaw', 'FACIAL_C_LowerLipRotation', 'FACIAL_C_TeethUpper', 'FACIAL_C_TeethLower', 'FACIAL_L_EyelidUpperA', 'FACIAL_R_EyelidUpperA', 'FACIAL_C_Nose', 'FACIAL_C_NoseTip', 'FACIAL_L_LipCorner', 'FACIAL_R_LipCorner', 'FACIAL_C_MouthUpper', 'FACIAL_C_MouthLower', 'head', 'neck_02', 'neck_01']
def joints(comp):
    res = {}
    for j in JN:
        try:
            if comp.get_bone_index(j) >= 0: t = comp.get_socket_transform(j, u.RelativeTransformSpace.RTS_COMPONENT).translation; res[j] = [round(t.x, 4), round(t.y, 4), round(t.z, 4)]
        except Exception: pass
    res['_n_bones'] = comp.get_num_bones(); return res
try:
    assert S.try_add_object_to_edit(ch)
    if C.get('b2'):   # our accepted body (B2 DNA) as a fixed whole-rig body: MHC space == project frame, shared spine/neck/head joints == our body
        D = str(pathlib.Path(u.Paths.project_dir()).resolve()/'Saved/Codex/CharacterShoulderFix_20260928/checkpoint/dna')
        step('import_body_whole_rig', lambda: S.import_body_whole_rig(ch, D+'/MH_B2_PendingNativeWorkflow_Body.dna', D+'/MH_B2_PendingNativeWorkflow_Head.dna'))
    else:
        face = u.load_asset('/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Body/SKM_RV_FaceMesh')
        ip = u.ImportFromTemplateParams(); ip.use_eye_meshes = True; ip.use_teeth_mesh = True; ip.match_vertices_by_u_vs = True; ip.alignment_options = u.MetaHumanAlignmentOptions.SCALING_ROTATION_TRANSLATION
        step('import_from_template', lambda: S.import_from_template(ch, face, None, None, None, ip))
    if C.get('coefs'): step('set_coefs', lambda: S.set_face_model_coefficients(ch, json.load(open(C['coefs']))['coefs']))
    if C.get('target_json'):
        T = json.load(open(C['target_json'])); V = lambda arr: [u.Vector(*p) for p in arr]
        fo = u.FitToTargetOptions(); fo.alignment_options = getattr(u.MetaHumanAlignmentOptions, C.get('align', 'NONE')); fo.adapt_neck = True; fo.disable_high_frequency_delta = False
        fp = u.MetaHumanCharacterFitToVerticesParams(); fp.options = fo; fp.head_vertices = V(T['head']); fp.left_eye_vertices = V(T['eyeL']); fp.right_eye_vertices = V(T['eyeR']); fp.teeth_vertices = V(T['teeth'])
        step('fit_state_to_target_vertices', lambda: S.fit_state_to_target_vertices(ch, fp))
    if C.get('head_scale'):
        es = ch.get_editor_property('face_evaluation_settings'); es.set_editor_property('head_scale', float(C['head_scale'])); step('head_scale', lambda: ch.set_editor_property('face_evaluation_settings', es))
    step('commit_face_state', lambda: S.commit_face_state(ch))
    act = S.spawn_meta_human_actor(ch, True); fc = [c for c in act.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Face'][0]
    out['joints_before_rig'] = joints(fc)
    dm = u.DynamicMesh(); u.GeometryScript_SceneUtils.copy_mesh_from_component(fc, dm, u.GeometryScriptCopyMeshFromComponentOptions(), False)
    import array; a = array.array('f')
    for p in u.GeometryScript_List.convert_vector_list_to_array(u.GeometryScript_MeshQueries.get_all_vertex_positions(dm, False)[1]): a.extend((p.x, p.y, p.z))
    (P/f'{name}_prerig.f32').write_bytes(a.tobytes())
    rp = u.MetaHumanCharacterAutoRiggingRequestParams(); rp.rig_type = getattr(u.MetaHumanRigType, C.get('rig_type', 'JOINTS_AND_BLEND_SHAPES')); rp.blocking = True; rp.report_progress = False
    step('request_auto_rigging', lambda: S.request_auto_rigging(ch, rp))
    out['has_face_dna_blendshapes'] = ch.get_editor_property('has_face_dna_blendshapes')
    fc = [c for c in act.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Face'][0]; out['joints_after_rig'] = joints(fc)
    m = fc.get_editor_property('skeletal_mesh_asset'); ud = m.get_asset_user_data_of_class(u.DNAAssetUserData) if hasattr(m, 'get_asset_user_data_of_class') else None
    dm = u.DynamicMesh(); u.GeometryScript_SceneUtils.copy_mesh_from_component(fc, dm, u.GeometryScriptCopyMeshFromComponentOptions(), False); a = array.array('f')
    for p in u.GeometryScript_List.convert_vector_list_to_array(u.GeometryScript_MeshQueries.get_all_vertex_positions(dm, False)[1]): a.extend((p.x, p.y, p.z))
    (P/f'{name}_postrig.f32').write_bytes(a.tobytes())
    out['face_mesh_has_dna'] = bool(ud); out['face_skeleton'] = m.skeleton.get_path_name() if m and m.skeleton else None
    act.destroy_actor()
    if C.get('export', True):
        dp = u.MetaHumanDNAExportParams(); dp.dna_head = True; dp.dna_body = False; dp.project_path = F+'/DNA'; dp.external_path = str(P/'dna'/name); dp.overwrite_existing_assets = True
        (P/'dna'/name).mkdir(parents=True, exist_ok=True); step('export_dna', lambda: u.MetaHumanCharacterExportBlueprintLibrary.export_dna(ch, dp))
        gp = u.MetaHumanGeometryExportParams(); gp.project_path = F+'/Export'; gp.head_skeletal_mesh = True; gp.body_skeletal_mesh = False; gp.full_body_skeletal_mesh = False; gp.overwrite_existing_assets = True
        step('export_geometry', lambda: u.MetaHumanCharacterExportBlueprintLibrary.export_geometry(ch, gp))
        out['dna_files'] = [str(p.name) for p in (P/'dna'/name).glob('*')]
except Exception: out['err'] = traceback.format_exc()[-1500:]
finally:
    S.remove_object_to_edit(ch)
out['saved'] = EAL.save_loaded_asset(ch, False)
out['exports'] = [a for a in EAL.list_assets(F+'/Export', recursive=False) if name in a] + ([a for a in EAL.list_assets(F+'/DNA', recursive=False)] if EAL.does_directory_exist(F+'/DNA') else [])
for a in out['exports']: EAL.save_asset(a, False)
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(P/f'rig_{name}.json').write_text(json.dumps(out, indent=1)); print('GD3_RIG', json.dumps(out)[:4000])
