"""GD11 head refinement: own-model (no HF delta) readout of GD11 E (copy of GUARDIAN-14 explorer) (no auto-rig, no export).
builtins.GD14_NX = {'name': 'MHC_GD14_W', 'target_json': <dense target {head, teeth, eyeL, eyeR}>, 'presets': [names], 'probe': True,
                    'cands': {tag: coefs list}  (optional: evaluate given coefficient vectors)}
1. work MHC (B2 whole-rig body = project frame) fitted to the HS3 sculpt (fit_state_to_target_vertices, align NONE) -> V_fit, coefs C0
2. V(C0) after set_face_model_coefficients (does the fit's high-frequency delta survive a coefficient set?)
3. face-model coefficients of the MetaHuman Creator presets (/MetaHumanCharacter/Optional/Presets/*), read-only (never saved)
4. region probe: C0 with region r's first PCA coefficient +1 -> per-vertex displacement (identifies the nose / nostril regions)
5. optional candidate coefficient vectors -> V
All vertex arrays = preview Face component, DNA order (33845), written to Saved/Codex/GD11_HeadRefinement_20261003/nose/*.f32"""
import unreal as u, json, builtins, pathlib, array, traceback, time
C = builtins.GD14_NX; P = pathlib.Path(u.Paths.project_dir()).resolve()/'Saved/Codex/GD11_HeadRefinement_20261003/nose'; P.mkdir(parents=True, exist_ok=True)
F = '/Game/Sphirus/CharacterLab/GD11_HeadRefinement_20261003/MHC'; S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); EAL = u.EditorAssetLibrary
out = {'steps': []}
def log(*a): out['steps'].append([round(time.time()-T0, 1)]+[str(x)[:300] for x in a])
T0 = time.time()
def readV(ch, tag):
    S.commit_face_state(ch); act = S.spawn_meta_human_actor(ch, True)
    fc = [c for c in act.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Face'][0]
    dm = u.DynamicMesh(); u.GeometryScript_SceneUtils.copy_mesh_from_component(fc, dm, u.GeometryScriptCopyMeshFromComponentOptions(), False); a = array.array('f')
    for p in u.GeometryScript_List.convert_vector_list_to_array(u.GeometryScript_MeshQueries.get_all_vertex_positions(dm, False)[1]): a.extend((p.x, p.y, p.z))
    act.destroy_actor(); (P/f'{tag}.f32').write_bytes(a.tobytes()); return len(a)//3
name = C['name']; path = F+'/'+name
ch = u.load_asset(path) if EAL.does_asset_exist(path) else u.AssetToolsHelpers.get_asset_tools().create_asset(name, F, u.MetaHumanCharacter, u.MetaHumanCharacterFactoryNew())
try:
    assert S.try_add_object_to_edit(ch)
    if C.get('fit', True):
        D = str(pathlib.Path(u.Paths.project_dir()).resolve()/'Saved/Codex/CharacterShoulderFix_20260928/checkpoint/dna')
        log('whole_rig', S.import_body_whole_rig(ch, D+'/MH_B2_PendingNativeWorkflow_Body.dna', D+'/MH_B2_PendingNativeWorkflow_Head.dna'))
        T = json.load(open(C['target_json'])); V = lambda arr: [u.Vector(*p) for p in arr]
        fo = u.FitToTargetOptions(); fo.alignment_options = u.MetaHumanAlignmentOptions.NONE; fo.adapt_neck = True; fo.disable_high_frequency_delta = False
        fp = u.MetaHumanCharacterFitToVerticesParams(); fp.options = fo; fp.head_vertices = V(T['head']); fp.left_eye_vertices = V(T['eyeL']); fp.right_eye_vertices = V(T['eyeR']); fp.teeth_vertices = V(T['teeth'])
        log('fit', S.fit_state_to_target_vertices(ch, fp))
        log('V_fit', readV(ch, 'V_fit'))
    C0 = list(S.get_face_model_coefficients(ch)); out['n_coefs'] = len(C0); json.dump({'coefs': C0}, open(P/'C0.json', 'w'))
    if C.get('c0_eval', True):
        log('set C0', S.set_face_model_coefficients(ch, C0)); log('V_c0', readV(ch, 'V_c0'))
    presets = {}
    for n in C.get('presets', []):
        try:
            pr = u.load_asset('/MetaHumanCharacter/Optional/Presets/'+n)
            added = S.try_add_object_to_edit(pr); cf = list(S.get_face_model_coefficients(pr)); S.remove_object_to_edit(pr)
            presets[n] = cf
            if C.get('transplant') and len(cf) == len(C0):   # region transplant: our coefs, preset's PCA for the given regions (x alpha)
                for alpha in C.get('alphas', [1.0]):
                    cc = list(C0)
                    for (a0, a1) in C['transplant']: cc[a0:a1] = [c0+alpha*(cp-c0) for c0, cp in zip(C0[a0:a1], cf[a0:a1])]
                    S.set_face_model_coefficients(ch, cc); readV(ch, 'tp_%s_%03d' % (n, int(alpha*100)))
                S.set_face_model_coefficients(ch, C0)
        except Exception: log('preset ERR', n, traceback.format_exc()[-300:])
    json.dump(presets, open(P/'presets_coefs.json', 'w')); out['presets_read'] = {k: len(v) for k, v in presets.items()}
    if C.get('probe'):   # region layout: c[0] = n regions; per region [quat4, scale, trans3, n_pca, pca...]
        i = 1; regs = []
        for r in range(int(C0[0])):
            q = i; npca = int(round(C0[i+8])); regs.append({'r': r, 'start': i, 'pca0': i+9, 'n_pca': npca}); i += 9+npca
        out['regions'] = regs; out['layout_end'] = i
        for rg in regs:
            cc = list(C0); cc[rg['pca0']] += float(C.get('probe_delta', 1.0)); S.set_face_model_coefficients(ch, cc); readV(ch, 'probe_r%02d' % rg['r'])
        S.set_face_model_coefficients(ch, C0)
    for tag, cf in C.get('cands', {}).items():
        S.set_face_model_coefficients(ch, cf); log('cand', tag, readV(ch, 'cand_'+tag))
    if C.get('cands'): S.set_face_model_coefficients(ch, C0)
except Exception: out['err'] = traceback.format_exc()[-1500:]
finally:
    S.remove_object_to_edit(ch)
out['saved'] = EAL.save_loaded_asset(ch, False)
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(P/f'explore_{name}.json').write_text(json.dumps(out, indent=1)); print('GD14_NX', json.dumps(out)[:3000])
