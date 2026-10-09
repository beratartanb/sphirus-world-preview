"""GD15 regional preset blend (what MetaHuman Creator's Blend tool does, via face-model coefficients): on a THROWAWAY GD15 probe of the W9 state,
for each preset replace (mode 'pca') or interpolate by w the PCA block of the given region(s) with the preset's, commit, read the DNA-order
Face vertices -> <out>/<prefix>_<preset>.f32. Region rigid transforms (quat / scale / trans) stay W9's unless mode 'full'. Nothing is saved.
builtins.GD15_RB = {'probe': GD15 MHC path (W9 state, existing throwaway), 'regions': [13], 'w': 1.0, 'mode': 'pca', 'presets': [...], 'coefs': abs preset_coefs.json, 'out': abs dir, 'prefix': 'nose'}"""
import unreal as u, builtins, json, array, pathlib, traceback
C = builtins.GD15_RB; S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); O = pathlib.Path(C['out']); out = {'done': []}
PC = json.load(open(C['coefs']))
def readv(ch):
    act = S.spawn_meta_human_actor(ch, True); fc = [c for c in act.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Face'][0]
    dm = u.DynamicMesh(); u.GeometryScript_SceneUtils.copy_mesh_from_component(fc, dm, u.GeometryScriptCopyMeshFromComponentOptions(), False); a = array.array('f')
    for p in u.GeometryScript_List.convert_vector_list_to_array(u.GeometryScript_MeshQueries.get_all_vertex_positions(dm, False)[1]): a.extend((p.x, p.y, p.z))
    act.destroy_actor(); return a
try:
    EAL = u.EditorAssetLibrary
    if not EAL.does_asset_exist(C['probe']):   # throwaway probe (never saved): recreate from the saved W9-state GD15 MHC
        assert C['probe'].startswith('/Game/Sphirus/CharacterLab/GD15_IdentityMaster_'); assert EAL.duplicate_asset(C.get('src', '/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/MHC/MHC_GD15_M0'), C['probe'])
    ch = u.load_asset(C['probe']); assert S.try_add_object_to_edit(ch); base = list(S.get_face_model_coefficients(ch))
    nreg = int(round(base[0])); i = 1; regs = []
    for r in range(nreg): npca = int(round(base[i+8])); regs.append((i, npca)); i = i+9+npca
    for p in C['presets']:
        pc = PC[p]; c = list(base); w = C.get('w', 1.0)
        for r in C['regions']:
            off, npca = regs[r]; lo = off if C.get('mode') == 'full' else off+9
            for k in range(lo, off+9+npca): c[k] = (1-w)*base[k]+w*pc[k]
        S.set_face_model_coefficients(ch, c); S.commit_face_state(ch); (O/f"{C['prefix']}_{p}.f32").write_bytes(readv(ch).tobytes()); out['done'].append(p)
    S.set_face_model_coefficients(ch, base); S.commit_face_state(ch); S.remove_object_to_edit(ch)
except Exception: out['err'] = traceback.format_exc()[-1200:]
print('GD15_RB', json.dumps(out)[:2000])
