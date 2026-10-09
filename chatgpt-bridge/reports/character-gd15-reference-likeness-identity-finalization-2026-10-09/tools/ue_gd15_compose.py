"""GD15 compose a candidate MetaHumanCharacter from the W9 state + per-region preset blends (MetaHuman region blending via face-model
coefficients; region rigid transforms stay W9's). Creates a NEW saved GD15 MHC, commits, reads the DNA-order Face vertices / landmarks / coefs.
builtins.GD15_CP = {'src': W9-state GD15 MHC, 'dst': new GD15 MHC, 'blend': [[[regions], preset, w], ...], 'coefs': abs preset json, 'out': abs dir, 'tag': str}"""
import unreal as u, builtins, json, array, pathlib, traceback
C = builtins.GD15_CP; S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); EAL = u.EditorAssetLibrary; O = pathlib.Path(C['out']); out = {'tag': C['tag']}
assert C['dst'].startswith('/Game/Sphirus/CharacterLab/GD15_IdentityMaster_') and not EAL.does_asset_exist(C['dst']), 'GD15 guard / exists'
PC = json.load(open(C['coefs']))
try:
    assert EAL.duplicate_asset(C['src'], C['dst']); ch = u.load_asset(C['dst']); assert S.try_add_object_to_edit(ch); base = list(S.get_face_model_coefficients(ch))
    nreg = int(round(base[0])); i = 1; regs = []
    for r in range(nreg): npca = int(round(base[i+8])); regs.append((i, npca)); i = i+9+npca
    c = list(base)
    for rl, p, w in C['blend']:
        for r in rl:
            off, npca = regs[r]
            for k in range(off+9, off+9+npca): c[k] = (1-w)*base[k]+w*PC[p][k]
    S.set_face_model_coefficients(ch, c); S.commit_face_state(ch)
    act = S.spawn_meta_human_actor(ch, True); fc = [x for x in act.get_components_by_class(u.SkeletalMeshComponent) if x.get_name() == 'Face'][0]
    dm = u.DynamicMesh(); u.GeometryScript_SceneUtils.copy_mesh_from_component(fc, dm, u.GeometryScriptCopyMeshFromComponentOptions(), False); a = array.array('f')
    for q in u.GeometryScript_List.convert_vector_list_to_array(u.GeometryScript_MeshQueries.get_all_vertex_positions(dm, False)[1]): a.extend((q.x, q.y, q.z))
    act.destroy_actor(); (O/f"{C['tag']}_verts.f32").write_bytes(a.tobytes())
    (O/f"{C['tag']}_landmarks.json").write_text(json.dumps([[q.x, q.y, q.z] for q in S.get_face_landmarks(ch)])); (O/f"{C['tag']}_coefs.json").write_text(json.dumps(list(S.get_face_model_coefficients(ch))))
    S.remove_object_to_edit(ch); out['saved'] = EAL.save_loaded_asset(ch, False)
except Exception: out['err'] = traceback.format_exc()[-1200:]
print('GD15_CP', json.dumps(out))
