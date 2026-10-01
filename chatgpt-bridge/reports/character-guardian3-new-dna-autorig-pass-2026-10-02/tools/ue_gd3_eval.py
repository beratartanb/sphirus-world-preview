"""GUARDIAN-3: evaluate face-model coefficients on an isolated MHC character (set -> commit -> read the 33845 DNA-order verts of the
preview face component; model space). builtins.GD3_EVAL = {'coefs': json path, 'out': f32 path, 'character': optional asset path (default probe),
'commit_asset': bool (save the character with these coefficients)}"""
import unreal as u, json, builtins, array, pathlib, traceback
C = builtins.GD3_EVAL; S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); q = u.GeometryScript_MeshQueries; out = {}
ch = u.load_asset(C.get('character', '/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001/MHC/MHC_GD3_Probe'))
try:
    assert S.try_add_object_to_edit(ch); act = S.spawn_meta_human_actor(ch, True)
    fc = [c for c in act.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Face'][0]
    cf = json.load(open(C['coefs']))['coefs']; S.set_face_model_coefficients(ch, cf); S.commit_face_state(ch)
    dm = u.DynamicMesh(); u.GeometryScript_SceneUtils.copy_mesh_from_component(fc, dm, u.GeometryScriptCopyMeshFromComponentOptions(), False)
    V = u.GeometryScript_List.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); a = array.array('f')
    for p in V: a.extend((p.x, p.y, p.z))
    pathlib.Path(C['out']).write_bytes(a.tobytes()); out['n'] = len(V)
    act.destroy_actor()
    if C.get('commit_asset'): out['saved'] = u.EditorAssetLibrary.save_loaded_asset(ch, False)
except Exception: out['err'] = traceback.format_exc()[-1200:]
finally:
    S.remove_object_to_edit(ch)
print('GD3_EVAL', json.dumps(out))
