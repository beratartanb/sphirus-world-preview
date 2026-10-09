"""GD14 MetaHumanCharacter helper job. builtins.GD14 = {'op': 'dup'|'probe'|'move'|'coefs_set', 'src', 'dst', 'out' (dir), 'tag',
'moves': [[landmark_index, dx, dy, dz], ...] (MHC Creator landmark sculpt = FaceState.TranslateLandmark), 'commit': bool, 'save': bool, 'coefs': [...]}.
Every op reads back: face vertices (preview Face component, DNA order) -> <out>/<tag>_verts.f32, landmarks -> <tag>_landmarks.json, coefficients."""
import unreal as u, json, builtins, array, traceback, pathlib
C = builtins.GD14; S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); EAL = u.EditorAssetLibrary; q = u.GeometryScript_MeshQueries; out = {'op': C['op']}
O = pathlib.Path(C['out']); O.mkdir(parents=True, exist_ok=True)
def readc(comp):
    dm = u.DynamicMesh(); u.GeometryScript_SceneUtils.copy_mesh_from_component(comp, dm, u.GeometryScriptCopyMeshFromComponentOptions(), False)
    V = u.GeometryScript_List.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); a = array.array('f')
    for p in V: a.extend((p.x, p.y, p.z))
    return a
ch = None; act = None
try:
    if C['op'] == 'dup':
        assert not EAL.does_asset_exist(C['dst']), 'exists ' + C['dst']
        ch = EAL.duplicate_asset(C['src'], C['dst']); assert ch; out['dup'] = EAL.save_asset(C['dst'], False)
    ch = u.load_asset(C['dst']); assert ch, 'load ' + C['dst']
    assert S.try_add_object_to_edit(ch), 'edit'
    if C['op'] == 'coefs_set': S.set_face_model_coefficients(ch, C['coefs']); S.commit_face_state(ch)
    if C['op'] == 'move':
        idx = [int(m[0]) for m in C['moves']]; d = [u.Vector(m[1], m[2], m[3]) for m in C['moves']]
        S.translate_face_landmarks(ch, idx, d)
        if C.get('commit', True): S.commit_face_state(ch)
    act = S.spawn_meta_human_actor(ch, True)
    fc = [c for c in act.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Face'][0]
    V = readc(fc); (O/f"{C['tag']}_verts.f32").write_bytes(V.tobytes()); out['verts'] = len(V)//3
    L = S.get_face_landmarks(ch); (O/f"{C['tag']}_landmarks.json").write_text(json.dumps([[p.x, p.y, p.z] for p in L])); out['landmarks'] = len(L)
    cf = list(S.get_face_model_coefficients(ch)); (O/f"{C['tag']}_coefs.json").write_text(json.dumps(cf)); out['coefs'] = len(cf)
    if C.get('save'): out['saved'] = EAL.save_asset(C['dst'], False)
except Exception: out['err'] = traceback.format_exc()[-1500:]
finally:
    try:
        if act: act.destroy_actor()
    except Exception: pass
    try:
        if ch and S.is_object_added_for_editing(ch): S.remove_object_to_edit(ch)
    except Exception: pass
print('GD14_MHC', json.dumps(out))
