"""GD14 Identity Master: AUTO-RIG an EXISTING sculpted MetaHumanCharacter (copy of ue_g11rr_rig_build.py, GD14 folders only, no template import,
no target fit). The sculpt source asset stays unrigged: it is duplicated to <dst> (GD14/MHC) and only the duplicate is auto-rigged (Epic service),
then head DNA (project asset + .dna on disk) and the rigged head skeletal mesh are exported into GD14/MHC/{DNA,Export}.
builtins.GD14R = {'src': '/Game/.../MHC/MHC_GD14_W1', 'dst': 'MHC_GD14_W1R', 'rig_type': 'JOINTS_AND_BLEND_SHAPES'}
-> Saved/Codex/GD14_Identity_20261009/rig/rig_<dst>.json, <dst>_prerig.f32, <dst>_postrig.f32 (DNA vertex order)"""
import unreal as u, json, builtins, pathlib, time, traceback, array
C = builtins.GD14R; P = pathlib.Path(u.Paths.project_dir()).resolve()/'Saved/Codex/GD14_Identity_20261009/rig'; P.mkdir(parents=True, exist_ok=True)
F = '/Game/Sphirus/CharacterLab/GD14_IdentityMaster_20261009/MHC'
S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); EAL = u.EditorAssetLibrary; out = {'cfg': {k: str(v) for k, v in C.items()}, 'steps': []}
def step(n, f):
    t = time.time()
    try: r = f(); out['steps'].append([n, 'ok', round(time.time()-t, 2), str(r)[:200]]); return r
    except Exception: out['steps'].append([n, 'ERR', traceback.format_exc()[-800:]]); return None
name = C['dst']; path = F+'/'+name
assert C['src'].startswith(F+'/') and path.startswith(F+'/'), 'GD14 guard: only GD14 MHC assets'
assert not EAL.does_asset_exist(path), 'GD14 guard: rig target %s exists - never re-rig over an existing asset (new name per rig)' % path
assert EAL.duplicate_asset(C['src'], path), 'duplicate failed'; EAL.save_asset(path, False); ch = u.load_asset(path)
JN = ['FACIAL_L_Eye', 'FACIAL_R_Eye', 'FACIAL_C_FacialRoot', 'FACIAL_C_Jaw', 'FACIAL_L_EyelidUpperA', 'FACIAL_R_EyelidUpperA', 'FACIAL_C_NoseTip', 'FACIAL_L_LipCorner', 'FACIAL_R_LipCorner', 'head', 'neck_02', 'neck_01']
def joints(comp):
    res = {}
    for j in JN:
        try:
            if comp.get_bone_index(j) >= 0: t = comp.get_socket_transform(j, u.RelativeTransformSpace.RTS_COMPONENT).translation; res[j] = [round(t.x, 4), round(t.y, 4), round(t.z, 4)]
        except Exception: pass
    res['_n_bones'] = comp.get_num_bones(); return res
def dump(fc, fn):
    dm = u.DynamicMesh(); u.GeometryScript_SceneUtils.copy_mesh_from_component(fc, dm, u.GeometryScriptCopyMeshFromComponentOptions(), False); a = array.array('f')
    for p in u.GeometryScript_List.convert_vector_list_to_array(u.GeometryScript_MeshQueries.get_all_vertex_positions(dm, False)[1]): a.extend((p.x, p.y, p.z))
    (P/fn).write_bytes(a.tobytes())
try:
    assert S.try_add_object_to_edit(ch)
    act = S.spawn_meta_human_actor(ch, True); fc = [c for c in act.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Face'][0]
    out['joints_before_rig'] = joints(fc); dump(fc, f'{name}_prerig.f32')
    rp = u.MetaHumanCharacterAutoRiggingRequestParams(); rp.rig_type = getattr(u.MetaHumanRigType, C.get('rig_type', 'JOINTS_AND_BLEND_SHAPES')); rp.blocking = True; rp.report_progress = False
    step('request_auto_rigging', lambda: S.request_auto_rigging(ch, rp))
    out['has_face_dna_blendshapes'] = ch.get_editor_property('has_face_dna_blendshapes')
    fc = [c for c in act.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Face'][0]; out['joints_after_rig'] = joints(fc)
    m = fc.get_editor_property('skeletal_mesh_asset'); ud = m.get_asset_user_data_of_class(u.DNAAssetUserData) if hasattr(m, 'get_asset_user_data_of_class') else None
    dump(fc, f'{name}_postrig.f32'); out['face_mesh_has_dna'] = bool(ud); out['face_skeleton'] = m.skeleton.get_path_name() if m and m.skeleton else None
    act.destroy_actor()
    dp = u.MetaHumanDNAExportParams(); dp.dna_head = True; dp.dna_body = False; dp.project_path = F+'/DNA'; dp.external_path = str(P/'dna'/name); dp.overwrite_existing_assets = True
    (P/'dna'/name).mkdir(parents=True, exist_ok=True); step('export_dna', lambda: u.MetaHumanCharacterExportBlueprintLibrary.export_dna(ch, dp))
    gp = u.MetaHumanGeometryExportParams(); gp.project_path = F+'/Export'; gp.head_skeletal_mesh = True; gp.body_skeletal_mesh = False; gp.full_body_skeletal_mesh = False; gp.overwrite_existing_assets = True
    step('export_geometry', lambda: u.MetaHumanCharacterExportBlueprintLibrary.export_geometry(ch, gp))
    out['dna_files'] = [str(p.name) for p in (P/'dna'/name).glob('*')]
except Exception: out['err'] = traceback.format_exc()[-1500:]
finally:
    S.remove_object_to_edit(ch)
out['saved'] = EAL.save_loaded_asset(ch, False)
out['exports'] = [a for a in EAL.list_assets(F+'/Export', recursive=False) if name in a] + ([a for a in EAL.list_assets(F+'/DNA', recursive=False) if name in a] if EAL.does_directory_exist(F+'/DNA') else [])
for a in out['exports']: EAL.save_asset(a, False)
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(P/f'rig_{name}.json').write_text(json.dumps(out, indent=1)); print('GD14_RIG', json.dumps(out)[:4000])
