"""GD14: iterative MetaHuman Creator landmark sculpt toward absolute landmark targets. builtins.GD14T = {'dst', 'out', 'tag', 'targets': {idx: [x,y,z]},
'iters': n, 'gain': 1.0, 'save': bool, 'start_coefs': optional path}. Each iteration translates every targeted landmark by gain*(target - current),
commits, and logs the remaining distance. Reads back vertices / landmarks / coefficients at the end."""
import unreal as u, json, builtins, array, traceback, pathlib
C = builtins.GD14T; S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); EAL = u.EditorAssetLibrary; q = u.GeometryScript_MeshQueries; out = {'tag': C['tag'], 'log': []}
O = pathlib.Path(C['out']); ch = None; act = None
def readc(comp):
    dm = u.DynamicMesh(); u.GeometryScript_SceneUtils.copy_mesh_from_component(comp, dm, u.GeometryScriptCopyMeshFromComponentOptions(), False)
    V = u.GeometryScript_List.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); a = array.array('f')
    for p in V: a.extend((p.x, p.y, p.z))
    return a
try:
    ch = u.load_asset(C['dst']); assert ch and S.try_add_object_to_edit(ch)
    if C.get('start_coefs'): S.set_face_model_coefficients(ch, json.load(open(C['start_coefs']))); S.commit_face_state(ch)
    T = {int(k): v for k, v in C['targets'].items()}; idx = sorted(T)
    for it in range(C.get('iters', 6)):
        L = S.get_face_landmarks(ch); d = [[T[i][j]-[L[i].x, L[i].y, L[i].z][j] for j in range(3)] for i in idx]
        res = max((x*x+y*y+z*z)**0.5 for x, y, z in d); out['log'].append(round(res*10, 3))
        g = C.get('gain', 1.0); S.translate_face_landmarks(ch, idx, [u.Vector(g*x, g*y, g*z) for x, y, z in d]); S.commit_face_state(ch)
    L = S.get_face_landmarks(ch); out['final_max_mm'] = round(max(sum((T[i][j]-[L[i].x, L[i].y, L[i].z][j])**2 for j in range(3))**0.5 for i in idx)*10, 3)
    act = S.spawn_meta_human_actor(ch, True); fc = [c for c in act.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Face'][0]
    (O/f"{C['tag']}_verts.f32").write_bytes(readc(fc).tobytes()); (O/f"{C['tag']}_landmarks.json").write_text(json.dumps([[p.x, p.y, p.z] for p in L]))
    (O/f"{C['tag']}_coefs.json").write_text(json.dumps(list(S.get_face_model_coefficients(ch))))
    if C.get('save'): out['saved'] = EAL.save_asset(C['dst'], False)
except Exception: out['err'] = traceback.format_exc()[-1500:]
finally:
    try:
        if act: act.destroy_actor()
    except Exception: pass
    try:
        if ch and S.is_object_added_for_editing(ch): S.remove_object_to_edit(ch)
    except Exception: pass
print('GD14_TGT', json.dumps(out))
