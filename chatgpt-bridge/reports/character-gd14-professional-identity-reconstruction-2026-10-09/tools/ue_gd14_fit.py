"""GD14: transfer a Blender-sculpted head (DNA order npy -> target json {head, eyeL, eyeR, teeth}, project frame) into a NEW MetaHumanCharacter:
duplicates <src> (GD14/MHC, unrigged sculpt asset) -> <dst>, fit_state_to_target_vertices (alignment NONE, high-frequency delta kept), commit,
dumps the resulting Face vertices + landmarks + coefficients (fit fidelity is measured outside), saves. GD14 folder only.
builtins.GD14F = {'src': '/Game/.../MHC/MHC_GD14_W2', 'dst': '/Game/.../MHC/MHC_GD14_W2B1', 'target_json': abs path, 'out': abs dir, 'tag': 'W2B1'}"""
import unreal as u, json, builtins, array, traceback, pathlib
C = builtins.GD14F; S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); EAL = u.EditorAssetLibrary; F = '/Game/Sphirus/CharacterLab/GD14_IdentityMaster_20261009/MHC'
out = {'tag': C['tag']}; O = pathlib.Path(C['out'])
assert C['src'].startswith(F+'/') and C['dst'].startswith(F+'/'), 'GD14 guard'
assert not EAL.does_asset_exist(C['dst']), 'GD14 guard: %s exists (new name per fit)' % C['dst']
assert EAL.duplicate_asset(C['src'], C['dst']); EAL.save_asset(C['dst'], False); ch = u.load_asset(C['dst'])
try:
    assert S.try_add_object_to_edit(ch)
    T = json.load(open(C['target_json'])); V = lambda arr: [u.Vector(*p) for p in arr]
    fo = u.FitToTargetOptions(); fo.alignment_options = u.MetaHumanAlignmentOptions.NONE; fo.adapt_neck = True; fo.disable_high_frequency_delta = False
    fp = u.MetaHumanCharacterFitToVerticesParams(); fp.options = fo; fp.head_vertices = V(T['head']); fp.left_eye_vertices = V(T['eyeL']); fp.right_eye_vertices = V(T['eyeR']); fp.teeth_vertices = V(T['teeth'])
    out['fit'] = str(S.fit_state_to_target_vertices(ch, fp)); S.commit_face_state(ch)
    act = S.spawn_meta_human_actor(ch, True); fc = [c for c in act.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Face'][0]
    dm = u.DynamicMesh(); u.GeometryScript_SceneUtils.copy_mesh_from_component(fc, dm, u.GeometryScriptCopyMeshFromComponentOptions(), False); a = array.array('f')
    for p in u.GeometryScript_List.convert_vector_list_to_array(u.GeometryScript_MeshQueries.get_all_vertex_positions(dm, False)[1]): a.extend((p.x, p.y, p.z))
    (O/f"{C['tag']}_verts.f32").write_bytes(a.tobytes()); act.destroy_actor()
    try: (O/f"{C['tag']}_landmarks.json").write_text(json.dumps([[p.x, p.y, p.z] for p in S.get_face_landmarks(ch)]))
    except Exception as e: out['lm_err'] = str(e)[:200]
    try: (O/f"{C['tag']}_coefs.json").write_text(json.dumps({'coefs': list(S.get_face_model_coefficients(ch))}))
    except Exception as e: out['coef_err'] = str(e)[:200]
except Exception: out['err'] = traceback.format_exc()[-1500:]
finally:
    S.remove_object_to_edit(ch)
out['saved'] = EAL.save_loaded_asset(ch, False); print('GD14_FIT', json.dumps(out))
