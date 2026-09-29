"""CF J1: duplicate the validated BodyRealism candidate set (meshes + PostProcess ABPs, which already carry the always-on
BR_Neutral curve and the SHCB driver) into /Game/Sphirus/CharacterLab/CharacterFinal_20260929/Body and re-point the
PostProcess references. The v6 neutral morph is baked by cf_ue_br_j2.py afterwards (same morph name, overwrite)."""
import unreal as u, pathlib, json
P = pathlib.Path(u.Paths.project_dir()).resolve(); S = P/'Saved/Codex/CharacterFinal_20260929'
src_d = '/Game/Sphirus/CharacterLab/BodyRealism_20260929'; dst = '/Game/Sphirus/CharacterLab/CharacterFinal_20260929/Body'
EAL = u.EditorAssetLibrary; assert not u.EditorLoadingAndSavingUtils.get_dirty_content_packages(), 'dirty packages before setup'
pairs = {'SKM_BR_BodyMesh': 'SKM_CF_BodyMesh', 'SKM_BR_FaceMesh': 'SKM_CF_FaceMesh', 'ABP_BR_Body_PostProcess': 'ABP_CF_Body_PostProcess', 'ABP_BR_Face_PostProcess': 'ABP_CF_Face_PostProcess'}
out = {}
for a, b in pairs.items():
    if EAL.does_asset_exist(dst+'/'+b): out[b] = 'exists'; continue
    x = EAL.duplicate_asset(src_d+'/'+a, dst+'/'+b); assert x, a; out[b] = x.get_path_name()
bm = u.load_asset(dst+'/SKM_CF_BodyMesh'); fm = u.load_asset(dst+'/SKM_CF_FaceMesh'); bpp = u.load_asset(dst+'/ABP_CF_Body_PostProcess'); fpp = u.load_asset(dst+'/ABP_CF_Face_PostProcess')
for bp in (bpp, fpp): u.BlueprintEditorLibrary.compile_blueprint(bp)
bm.set_editor_property('post_process_anim_blueprint', bpp.generated_class()); fm.set_editor_property('post_process_anim_blueprint', fpp.generated_class())
out['body_pp'] = bm.get_editor_property('post_process_anim_blueprint').get_path_name(); out['face_pp'] = fm.get_editor_property('post_process_anim_blueprint').get_path_name()
out['body_skeleton'] = bm.get_editor_property('skeleton').get_path_name(); out['face_skeleton'] = fm.get_editor_property('skeleton').get_path_name()
out['morphs_body'] = [m.get_name() for m in bm.get_editor_property('morph_targets')]; out['morphs_face'] = [m.get_name() for m in fm.get_editor_property('morph_targets')]
out['lods'] = {'body': u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem).get_lod_count(bm), 'face': u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem).get_lod_count(fm)}
out['saved'] = [EAL.save_loaded_asset(a, False) for a in (bm, fm, bpp, fpp)]
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(S/'cf_body_setup.json').write_text(json.dumps(out, indent=1, default=str)); print(json.dumps(out, indent=1, default=str))
