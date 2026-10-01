"""GUARDIAN-3: Jacobian of the MetaHumanCharacter parametric face model (face_model_coefficients -> DNA-order vertices, all 33845 head
verts incl. eyes / teeth) by forward differences on an isolated probe character (MHC_GD3_Probe, imported from the template face).
Writes Saved/Codex/CharacterGuardian3_20261001/jac/{base.f32, coef.json, J_<k0>_<k1>.f32 (float32 [k][v][3] deltas per unit coef)}.
builtins.GD3_JAC = {'k0': int, 'k1': int, 'h': step, 'base_coefs': optional list (evaluate around these)}"""
import unreal as u, json, time, pathlib, builtins, array, traceback
C = builtins.GD3_JAC; P = pathlib.Path(u.Paths.project_dir()).resolve()/'Saved/Codex/CharacterGuardian3_20261001/jac'; P.mkdir(parents=True, exist_ok=True)
S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); q = u.GeometryScript_MeshQueries; out = {}
ch = u.load_asset('/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001/MHC/MHC_GD3_Probe')
def readc(comp):
    dm = u.DynamicMesh(); u.GeometryScript_SceneUtils.copy_mesh_from_component(comp, dm, u.GeometryScriptCopyMeshFromComponentOptions(), False)
    V = u.GeometryScript_List.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); a = array.array('f')
    for p in V: a.extend((p.x, p.y, p.z))
    return a
try:
    assert S.try_add_object_to_edit(ch); act = S.spawn_meta_human_actor(ch, True)
    fc = [c for c in act.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Face'][0]
    c0 = list(C.get('base_coefs') or S.get_face_model_coefficients(ch)); S.set_face_model_coefficients(ch, c0); S.commit_face_state(ch); B = readc(fc)
    if C['k0'] == 0: (P/'base.f32').write_bytes(B.tobytes()); (P/'coef.json').write_text(json.dumps(c0))
    h = C.get('h', 0.1); J = array.array('f'); t = time.time()
    for k in range(C['k0'], min(C['k1'], len(c0))):
        c2 = list(c0); c2[k] += h; S.set_face_model_coefficients(ch, c2); S.commit_face_state(ch); V = readc(fc)
        J.extend([(a-b)/h for a, b in zip(V, B)])
    S.set_face_model_coefficients(ch, c0); S.commit_face_state(ch)
    (P/f"J_{C['k0']:04d}_{C['k1']:04d}.f32").write_bytes(J.tobytes()); out = {'n': len(c0), 'k': [C['k0'], C['k1']], 'sec': time.time()-t, 'verts': len(B)//3}
    act.destroy_actor()
except Exception: out['err'] = traceback.format_exc()[-1200:]
finally:
    S.remove_object_to_edit(ch)
print('GD3_JAC', json.dumps(out))
